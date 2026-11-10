"""One simulator session: market + client flow + book + risk + P&L ledger + log.

P&L ledger (USD, exact by construction):
* every tick:  MTM change from the market move = Taylor Greek terms
  (delta, gamma, vega by tenor, theta, vanna, volga, rho) + carry + unexplained
* every trade: MTM jump at execution = client edge (client trades) or hedging
  cost (spot hedges, interdealer trades, closes and rolls)
So total P&L = edge + hedging costs + carry + Greek P&L + unexplained.
Limit-breach penalties are tracked separately and deducted in the score.
"""
from __future__ import annotations

from dataclasses import asdict
from typing import Optional

import numpy as np

from engine.config import load_config
from engine.fx_conventions import TENOR_LIST, TENORS, get_pair, usd_per_base, usd_per_quote
from engine.fx_pricer import price
from engine.market_sim import MarketSim
from engine.pnl_attribution import attribute_legs
from engine.structures import SingleMarket, bucket_for, build
from simulator.book import Book
from simulator.clients import CLIENT_LABEL, RFQ, ClientFlow, client_decides, competitive_levels, metric_and_vega

TERMS = ["delta", "gamma", "vega", "theta", "vanna", "volga", "rho", "edge", "hedge_cost", "carry", "unexplained"]
IDB_POINTS = {"10P": -0.10, "25P": -0.25, "ATM": None, "25C": 0.25, "10C": 0.10}


def _zero_terms() -> dict:
    d = {k: 0.0 for k in TERMS}
    d["vega_by_tenor"] = {}
    return d


class SimSession:
    def __init__(self, seed: int, level: int, use_live: bool = False, regime: Optional[str] = None,
                 pairs: Optional[list[str]] = None, inherit: Optional[bool] = None) -> None:
        self.cfg = load_config()
        self.sc = self.cfg["simulator"]
        self.seed, self.level = seed, level
        self.lv = self.sc["levels"][level]
        self.market = MarketSim(seed, level, regime, pairs, use_live, self.cfg)
        m = self.market
        self.pairs = m.pairs
        self.flow = ClientFlow(seed, self.lv, self.sc, self.pairs, m.ticks_per_day, m.regime)
        self.book = Book()
        self.rfqs: list[RFQ] = []
        self.log: list[dict] = []
        self.news: list[dict] = []
        self.paused = False
        self.pnl_usd = 0.0
        self.prev_pnl_quote: dict[str, float] = {}
        self.pnl_hist: list[tuple[float, float]] = [(0.0, 0.0)]
        self.day_terms = _zero_terms()
        self.total_terms = _zero_terms()
        self.debriefs: list[dict] = []
        self.penalty_usd = 0.0
        self.breach_ticks: dict[str, int] = {}
        self.in_breach: dict[str, bool] = {}
        self.counters = {"rfqs": 0, "quoted": 0, "traded": 0, "no_trade": 0, "passed": 0, "missed": 0}
        self.trades: list[dict] = []
        self.risk: dict = {}
        self.delta_util: list[float] = []
        self.flushed = 0
        mult = self.lv["limit_mult"]
        L = self.sc["limits"]
        self.limits = {"delta": L["delta_usd_per_pair"] * mult, "gamma": L["gamma_usd_per_pct"] * mult,
                       "vega": L["vega_usd_per_pair"] * mult, "total_vega": L["total_vega_usd"] * mult}
        self._log("session_start", seed=seed, level=level, regime=m.regime, pairs=self.pairs, spot_source=m.source,
                  spots={p: m.spot(p) for p in self.pairs}, limits=self.limits,
                  events=m.upcoming_events() if self.lv["news_preannounced"] else "calendar shown on screen",
                  client_mix=self.flow.mix)
        rng = np.random.default_rng([seed, 3])
        if inherit is None:
            inherit = rng.random() < (0.35 if level == 1 else 0.6)
        if inherit:
            self._inherit(rng)
        self._mark()
        self._update_risk()

    # ------------------------------------------------------------------ helpers
    def _log(self, _kind: str, **data) -> None:
        entry = {"t": round(self.market.day_float, 4), "day": self.market.day + 1, "kind": _kind}
        for k, v in data.items():
            entry["sub_kind" if k == "kind" else k] = v
        self.log.append(entry)

    def mkt(self, pair: str) -> SingleMarket:
        return self.market.single(pair)

    def usdq(self, pair: str) -> float:
        return usd_per_quote(pair, self.market.spots())

    def usdb(self, pair: str) -> float:
        return usd_per_base(pair, self.market.spots())

    def stress_mult(self) -> float:
        return 1 + (self.sc["stress_spread_mult"] - 1) * self.market.stress()

    def idb_half_spread(self, tenor: str, point: str = "ATM") -> float:
        """Half bid/offer in vol points on the interdealer screen."""
        w = self.sc["idb_vol_spread"][tenor] * self.stress_mult() / 2
        return w * (1.5 if point.startswith("10") else 1.0)

    def spot_half_spread(self, pair: str) -> float:
        p = get_pair(pair)
        return self.sc["spot_spread_pips"][pair] / 2 * p.pip * self.stress_mult()

    def _mark(self) -> float:
        """Re-mark the book; returns the USD P&L change since the last mark."""
        inc = 0.0
        for pair in set(self.book.pairs()) | set(self.prev_pnl_quote):
            m = self.mkt(pair)
            now = self.book.pnl_quote(pair, m)
            d = now - self.prev_pnl_quote.get(pair, 0.0)
            self.prev_pnl_quote[pair] = now
            inc += d * self.usdq(pair)
        self.pnl_usd += inc
        return inc

    def _add(self, key: str, v: float) -> None:
        self.day_terms[key] = self.day_terms.get(key, 0.0) + v
        self.total_terms[key] = self.total_terms.get(key, 0.0) + v

    def _add_vega_bucket(self, b: str, v: float) -> None:
        for d in (self.day_terms, self.total_terms):
            d["vega_by_tenor"][b] = d["vega_by_tenor"].get(b, 0.0) + v

    def _inherit(self, rng) -> None:
        choices = [("straddle", "1M"), ("risk_reversal", "3M"), ("strangle", "2W"), ("call", "6M"), ("put", "1M")]
        for _ in range(int(rng.integers(1, 4))):
            pair = str(rng.choice(self.pairs))
            kind, tenor = choices[int(rng.integers(len(choices)))]
            side = int(rng.choice([1, -1]))
            N = float(rng.choice([20e6, 30e6, 50e6]))
            m = self.mkt(pair)
            s = build(kind, m, tenor, N, side=side)
            for l in s.legs:
                pu = float(price(m.spot, l.K, l.expiry - m.t, m.rd, m.rf, m.vol(l.K, l.expiry - m.t), l.cp))
                self.book.add(pair, "option", l.notional, l.K, l.expiry, l.cp, pu, tenor=tenor, source="inherited",
                              label=f"inherited {kind}", open_t=0.0)
            self._log("inherited_position", pair=pair, structure=kind, tenor=tenor, side="long" if side > 0 else "short",
                      notional=N)

    # ------------------------------------------------------------------ tick
    def step(self) -> list[dict]:
        m = self.market
        if self.paused or m.finished:
            return []
        dt = 1.0 / m.ticks_per_day / 365.0
        active = set(self.book.pairs()) | set(self.pairs)
        m0 = {p: self.mkt(p) for p in active}
        legs0 = {p: self.book.legs(p) for p in active}
        news = m.step()
        explained = 0.0
        for p in active:
            if not legs0[p]:
                continue
            m1 = self.mkt(p)
            att = attribute_legs(legs0[p], m0[p], m1)
            fx = self.usdq(p)
            for k, v in att.terms.items():
                self._add(k, v * fx)
                explained += v * fx
            for b, v in att.vega_by_tenor.items():
                self._add_vega_bucket(b, v * fx)
            c = self.book.carry(p, m1, dt) * fx
            self._add("carry", c)
            explained += c
        expiries = self.book.settle_expiries(m.t, m.spots())
        for e in expiries:
            self._log("expiry", **e)
        inc = self._mark()
        self._add("unexplained", inc - explained)

        for n in news:
            self.news.append(n)
            self._log("news", **n)
        for r in self.rfqs:
            if r.status == "open" and m.tick >= r.expires_tick:
                r.status = "missed"
                self.counters["missed"] += 1
                self._log("rfq_missed", rfq=r.id, desc=r.describe())
        for r in self.flow.maybe_generate(m.tick, m):
            self.rfqs.append(r)
            self.counters["rfqs"] += 1
            self._log("rfq", rfq=r.id, desc=r.describe(), pair=r.pair, kind=r.kind, tenor=r.tenor,
                      notional=r.notional, expires_in_ticks=r.expires_tick - m.tick)
        self._update_risk()
        self._check_limits()
        self.pnl_hist.append((m.day_float, self.pnl_usd))
        if m.tick % m.ticks_per_day == 0:
            self._end_of_day(m.tick // m.ticks_per_day)
            if self.level == 1 and self.lv.get("pause"):
                self.paused = True  # level 1: stop at each day end so you can read the debrief
        if m.finished:
            self._log("session_end", pnl_usd=self.pnl_usd, penalty_usd=self.penalty_usd)
        return news

    # ------------------------------------------------------------------ risk and limits
    def _update_risk(self) -> None:
        out = {}
        total_vega = 0.0
        for p in sorted(set(self.book.pairs()) | set(self.pairs)):
            legs = self.book.legs(p)
            m = self.mkt(p)
            if legs:
                e = self.book.exposure(p, m)
                fb, fq = self.usdb(p), self.usdq(p)
                out[p] = {"delta_base": e.delta, "delta_pa_base": e.delta_pa, "delta_usd": e.delta * fb,
                          "gamma_usd": e.gamma_1pct * fb, "vega_usd": e.vega * fq, "theta_usd": e.theta * fq,
                          "vanna_usd": e.vanna * fb, "volga_usd": e.volga * fq,
                          "vega_by_tenor_usd": {k: v * fq for k, v in e.vega_by_tenor.items()},
                          "pnl_quote": self.prev_pnl_quote.get(p, 0.0)}
            else:
                out[p] = {"delta_base": 0.0, "delta_pa_base": 0.0, "delta_usd": 0.0, "gamma_usd": 0.0, "vega_usd": 0.0,
                          "theta_usd": 0.0, "vanna_usd": 0.0, "volga_usd": 0.0, "vega_by_tenor_usd": {}, "pnl_quote": 0.0}
            total_vega += abs(out[p]["vega_usd"])
        self.risk = out
        self.total_vega = total_vega

    def limit_status(self) -> list[dict]:
        rows = []
        for p, r in self.risk.items():
            for key, lim_key, val in (("delta", "delta", r["delta_usd"]), ("gamma", "gamma", r["gamma_usd"]),
                                      ("vega", "vega", r["vega_usd"])):
                lim = self.limits[lim_key]
                rows.append({"pair": p, "limit": key, "value_usd": val, "limit_usd": lim, "used": abs(val) / lim,
                             "breach": abs(val) > lim})
        rows.append({"pair": "ALL", "limit": "total vega", "value_usd": self.total_vega,
                     "limit_usd": self.limits["total_vega"], "used": self.total_vega / self.limits["total_vega"],
                     "breach": self.total_vega > self.limits["total_vega"]})
        return rows

    def _check_limits(self) -> None:
        pen = self.sc["limits"]["breach_penalty_usd_per_tick"]
        util = []
        for row in self.limit_status():
            key = f"{row['pair']}:{row['limit']}"
            if row["limit"] == "delta":
                util.append(row["used"])
            if row["breach"]:
                self.penalty_usd += pen
                self.breach_ticks[key] = self.breach_ticks.get(key, 0) + 1
                if not self.in_breach.get(key):
                    self._log("limit_breach", limit=key, value_usd=row["value_usd"], limit_usd=row["limit_usd"])
                self.in_breach[key] = True
            elif self.in_breach.get(key):
                self.in_breach[key] = False
                self._log("limit_cleared", limit=key)
        if util:
            self.delta_util.append(float(np.mean(util)))

    # ------------------------------------------------------------------ trader actions
    def open_rfqs(self) -> list[RFQ]:
        return [r for r in self.rfqs if r.status == "open"]

    def quote(self, rfq_id: int, bid: float, offer: float) -> dict:
        r = next((x for x in self.rfqs if x.id == rfq_id), None)
        if r is None or r.status != "open":
            return {"ok": False, "msg": "RFQ is no longer open."}
        if offer <= bid:
            return {"ok": False, "msg": "Offer must be above bid."}
        m = self.mkt(r.pair)
        fair, dvdq, mid_val = metric_and_vega(r, m)
        half = self.idb_half_spread(r.tenor)
        r.bid, r.offer, r.fair_at_quote = bid, offer, fair
        self.counters["quoted"] += 1
        traded = client_decides(r, bid, offer, fair, half)
        cb, co = competitive_levels(r, fair, half)
        if not traded:
            r.status = "no_trade"
            self.counters["no_trade"] += 1
            self._log("quote_no_trade", rfq=r.id, desc=r.describe(), bid=bid, offer=offer, fair=round(fair, 3),
                      client_side="buy" if r.client_side > 0 else "sell",
                      competitive=(round(cb, 3), round(co, 3)), client=CLIENT_LABEL[r.client_type])
            return {"ok": True, "traded": False, "msg": "Nothing done: client traded elsewhere."}
        q = offer if r.client_side > 0 else bid
        our = -r.client_side
        from simulator.clients import _bump_weights
        from engine.fx_pricer import greeks
        w = _bump_weights(r.kind, r.legs)
        tid = len(self.trades) + 1
        for l, wi in zip(r.legs, w):
            tau = l.expiry - m.t
            v = m.vol(l.K, tau)
            g = greeks(m.spot, l.K, tau, m.rd, m.rf, v, l.cp)
            pu = g.price + (q - fair) * wi * g.vega * 0.01
            self.book.add(r.pair, "option", our * r.notional * l.notional, l.K, l.expiry, l.cp, pu, tenor=r.tenor,
                          source="client", trade_id=tid, client_type=r.client_type, label=f"{r.kind} {l.label}",
                          open_t=m.t)
        edge = self._mark()
        self._add("edge", edge)
        r.status, r.trade_id, r.edge_quote_ccy = "traded", tid, edge
        self.counters["traded"] += 1
        rec = {"trade_id": tid, "rfq": r.id, "desc": r.describe(), "client": r.client_type, "informed": r.informed,
               "we": "sell" if our < 0 else "buy", "price": q, "fair": fair, "edge_usd": edge, "t": self.market.day_float,
               "pair": r.pair}
        self.trades.append(rec)
        self._log("trade", **rec, client_label=CLIENT_LABEL[r.client_type])
        self._update_risk()
        return {"ok": True, "traded": True, "msg": f"Done: you {'sold' if our < 0 else 'bought'} at {q:.2f} "
                                                   f"({CLIENT_LABEL[r.client_type]}). Edge {edge:,.0f} USD."}

    def pass_rfq(self, rfq_id: int) -> None:
        r = next((x for x in self.rfqs if x.id == rfq_id), None)
        if r and r.status == "open":
            r.status = "passed"
            self.counters["passed"] += 1
            self._log("rfq_passed", rfq=r.id, desc=r.describe())

    def spot_hedge(self, pair: str, amount_base: float) -> dict:
        if abs(amount_base) < 1:
            return {"ok": False, "msg": "Amount too small."}
        S = self.market.spot(pair)
        px = S + np.sign(amount_base) * self.spot_half_spread(pair)
        self.book.add(pair, "spot", amount_base, px, source="spot_hedge", label="spot hedge", open_t=self.market.t)
        cost = self._mark()
        self._add("hedge_cost", cost)
        self._log("spot_hedge", pair=pair, amount_base=amount_base, price=px, cost_usd=cost)
        self._update_risk()
        p = get_pair(pair)
        return {"ok": True, "msg": f"{'Bought' if amount_base > 0 else 'Sold'} {p.base} {abs(amount_base)/1e6:,.1f}m "
                                   f"at {px:.{p.decimals}f} (cost {cost:,.0f} USD)."}

    def delta_hedge(self, pair: str) -> dict:
        d = self.risk.get(pair, {}).get("delta_base", 0.0)
        amt = -round(d / 1e5) * 1e5
        if abs(amt) < 1e5:
            return {"ok": False, "msg": "Delta already flat."}
        return self.spot_hedge(pair, amt)

    def idb_screen(self, pair: str, tenors: Optional[list[str]] = None) -> list[dict]:
        s = self.market.surface(pair)
        rows = []
        for t in tenors or TENOR_LIST:
            sm = s.smiles[t]
            row = {"Tenor": t}
            for pt, d in IDB_POINTS.items():
                K = sm.pillar_strikes["ATM"] if d is None else sm.pillar_strikes[pt]
                v = float(sm.vol(K)) * 100
                h = self.idb_half_spread(t, pt)
                row[pt] = (v - h, v + h, K)
            rows.append(row)
        return rows

    def idb_trade(self, pair: str, tenor: str, point: str, side: int, notional: float, straddle: bool = False) -> dict:
        m = self.mkt(pair)
        sm = self.market.surface(pair).smiles[tenor]
        K = sm.pillar_strikes["ATM"] if point == "ATM" else sm.pillar_strikes[point]
        tau = TENORS[tenor]
        mid = m.vol(K, tau)
        h = self.idb_half_spread(tenor, point) / 100
        vexec = mid + side * h
        cps = ["C", "P"] if straddle else (["P"] if point.endswith("P") else ["C"])
        for cp in cps:
            pu = float(price(m.spot, K, tau, m.rd, m.rf, vexec, cp))
            self.book.add(pair, "option", side * notional, K, m.t + tau, cp, pu, tenor=tenor, source="idb",
                          label=f"IDB {tenor} {point}{' straddle' if straddle else ''}", open_t=m.t)
        cost = self._mark()
        self._add("hedge_cost", cost)
        self._log("idb_trade", pair=pair, tenor=tenor, point=point, side="buy" if side > 0 else "sell",
                  notional=notional, straddle=straddle, vol=vexec * 100, strike=K, cost_usd=cost)
        self._update_risk()
        return {"ok": True, "msg": f"{'Bought' if side > 0 else 'Sold'} {tenor} {point}{' straddle' if straddle else ''} "
                                   f"{notional/1e6:,.0f}m at {vexec*100:.2f} vol (cost {cost:,.0f} USD)."}

    def close_position(self, pid: int) -> dict:
        pos = next((p for p in self.book.positions if p.id == pid), None)
        if pos is None:
            return {"ok": False, "msg": "Position not found."}
        m = self.mkt(pos.pair)
        if pos.kind == "spot":
            px = m.spot - np.sign(pos.notional) * self.spot_half_spread(pos.pair)
        else:
            tau = pos.expiry - m.t
            b = bucket_for(tau)
            v = m.vol(pos.K, tau) - np.sign(pos.notional) * self.idb_half_spread(b) / 100
            px = float(price(m.spot, pos.K, tau, m.rd, m.rf, v, pos.cp))
        self.book.remove(pid, px)
        cost = self._mark()
        self._add("hedge_cost", cost)
        self._log("close", position=pid, pair=pos.pair, label=pos.label, cost_usd=cost)
        self._update_risk()
        return {"ok": True, "msg": f"Closed position {pid} (cost {cost:,.0f} USD)."}

    def roll_position(self, pid: int, new_tenor: str) -> dict:
        pos = next((p for p in self.book.positions if p.id == pid), None)
        if pos is None or pos.kind != "option":
            return {"ok": False, "msg": "Only options can be rolled."}
        info = dict(pair=pos.pair, K=pos.K, cp=pos.cp, N=pos.notional)
        self.close_position(pid)
        m = self.mkt(info["pair"])
        tau = TENORS[new_tenor]
        v = m.vol(info["K"], tau) + np.sign(info["N"]) * self.idb_half_spread(new_tenor) / 100
        pu = float(price(m.spot, info["K"], tau, m.rd, m.rf, v, info["cp"]))
        self.book.add(info["pair"], "option", info["N"], info["K"], m.t + tau, info["cp"], pu, tenor=new_tenor,
                      source="idb", label=f"rolled to {new_tenor}", open_t=m.t)
        cost = self._mark()
        self._add("hedge_cost", cost)
        self._log("roll", position=pid, new_tenor=new_tenor, cost_usd=cost)
        self._update_risk()
        return {"ok": True, "msg": f"Rolled position {pid} to {new_tenor}."}

    def toggle_pause(self) -> None:
        if self.lv.get("pause"):
            self.paused = not self.paused

    # ------------------------------------------------------------------ analysis
    def scenario_grid(self, pair: str, spots=(-3, -2, -1, 0, 1, 2, 3), vols=(-3, -2, -1, 0, 1, 2, 3)):
        s = self.book.structure(pair)
        if not s.legs:
            return None
        m = self.mkt(pair)
        v0 = s.value(m)
        fx = self.usdq(pair)
        grid = []
        for dv in vols:
            row = []
            for ds in spots:
                mm = m.bump_spot(ds).bump_vol(dv)
                row.append((s.value(mm) - v0) * fx)
            grid.append(row)
        return {"spots": list(spots), "vols": list(vols), "pnl": grid}

    def _end_of_day(self, day: int) -> None:
        from simulator.debrief import day_takeaway
        d = {k: (dict(v) if isinstance(v, dict) else v) for k, v in self.day_terms.items()}
        total = sum(v for k, v in d.items() if k != "vega_by_tenor")
        rec = {"day": day, "terms": d, "total": total, "takeaway": day_takeaway(d, self)}
        self.debriefs.append(rec)
        self._log("day_end", day=day, pnl_day_usd=total, breakdown={k: round(v, 0) for k, v in d.items()
                                                                     if k != "vega_by_tenor"},
                  vega_by_tenor={k: round(v, 0) for k, v in d["vega_by_tenor"].items()},
                  takeaway=rec["takeaway"], cum_pnl_usd=self.pnl_usd, penalty_usd=self.penalty_usd)
        self.day_terms = _zero_terms()

    def informed_pnl(self) -> float:
        mk = {p: self.mkt(p) for p in self.book.pairs()}
        tot = 0.0
        for t in self.trades:
            if t["informed"] or t["client"] == "macro_hf":
                tot += self.book.trade_pnl(t["trade_id"], {**mk, t["pair"]: self.mkt(t["pair"])}) * self.usdq(t["pair"])
        return tot

    def new_log_entries(self) -> list[dict]:
        out = self.log[self.flushed:]
        self.flushed = len(self.log)
        return out
