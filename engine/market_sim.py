"""Market simulator for the FX vol trading game.

Spot
----
Each non-USD currency has a USD value. Per tick its log change is
    drift + sigma * sqrt(dt) * z  + jumps + event moves + informed-flow alpha
with z correlated across currencies (``simulator.ccy_corr``). Every pair,
crosses included, is USD(base)/USD(quote), so crosses are always consistent.
Diffusive vol = the pair's current 1M ATM implied x a realised/implied ratio
drawn per session from the regime, so realised vol is stochastic (it moves
with implied) and can sit above or below it.

Vol
---
Per pair an ATM 'level' (vol points) follows an OU process whose shocks are
correlated with the pair's own spot return (``spot_vol_corr`` x a session
multiplier; e.g. USDJPY negative: yen strength with higher vol). Level moves
hit the front end more (weight sqrt(1M/T)). RRs move with the level
(``rr_beta``) plus a skew factor pushed by regime and jumps; BFs scale with
the level. Scheduled events add their variance to every tenor that covers
them (pre-event bid) and are removed when the event prints (crush). ATM
calendar arbitrage is enforced every tick; smiles are butterfly-checked when
calibrated (see :class:`engine.surface.LazyVolSurface`).

Sessions are compressed: 10 days of a stressed market are made eventful by the
regime's per-session jump counts and the level's exaggeration multiplier.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from engine.config import load_config
from engine.fx_conventions import (PAIRS, TENOR_LIST, TENORS, USD_PAIRS, forward_points, get_pair,
                                   usd_values_from_usd_pairs)
from engine.market_data import build_market, rate_curves
from engine.smile import SmileQuotes
from engine.structures import SingleMarket
from engine.surface import LazyVolSurface, atm_calendar_ok

NON_USD = ["EUR", "JPY", "GBP", "AUD", "NZD", "CAD", "CHF"]
# direction of each currency (vs USD) in a risk-off shock
RISK_OFF_CCY = {"EUR": -0.2, "JPY": 1.0, "GBP": -0.6, "AUD": -1.0, "NZD": -1.0, "CAD": -0.6, "CHF": 0.8}
TIME_COMPRESSION = 10.0  # mean reversion speed-up so a 10-day session shows regime dynamics
L1_PAIRS = ["EURUSD", "USDJPY", "GBPUSD", "AUDUSD"]
L2_POOLS = [["EURUSD", "USDJPY", "EURJPY"], ["EURUSD", "GBPUSD", "EURGBP"], ["USDJPY", "AUDUSD"],
            ["EURUSD", "USDCHF", "EURCHF"], ["USDJPY", "USDCAD", "AUDUSD"]]

HEADLINES = {
    ("JPY", 1): ["Japan's top currency official warns of 'excessive' moves", "Carry unwind: yen surges as equities slide",
                 "BoJ hawkish leak lifts yen"],
    ("JPY", -1): ["Yen slides as BoJ signals patience", "Carry trades back in vogue, yen weakens"],
    ("CHF", 1): ["Haven demand lifts franc", "SNB silent as franc firms"],
    ("CHF", -1): ["SNB said to be active in FX markets", "Franc weakens as risk appetite returns"],
    ("AUD", 1): ["China stimulus hopes lift Aussie", "Iron ore rally boosts AUD"],
    ("AUD", -1): ["Aussie hit by China growth scare", "Risk-off: AUD drops with equities"],
    ("NZD", 1): ["Kiwi jumps on dairy auction"], ("NZD", -1): ["Kiwi slides on dovish RBNZ remarks"],
    ("EUR", 1): ["Euro bid on German fiscal headlines", "ECB speaker pushes back on cuts"],
    ("EUR", -1): ["Euro falls on weak PMIs", "Political risk weighs on euro"],
    ("GBP", 1): ["Sterling up on strong wage data"], ("GBP", -1): ["Gilt selloff drags sterling lower", "Fiscal worries hit the pound"],
    ("CAD", 1): ["Oil spike lifts loonie"], ("CAD", -1): ["Oil slump weighs on CAD"],
    ("USD", 1): ["Dollar surges after hawkish Fed comments", "US yields jump, dollar bid across the board"],
    ("USD", -1): ["Dollar slides on soft US data", "Treasury rally drags the dollar lower"],
}


@dataclass
class Event:
    day: float           # session day (fraction) when it prints
    ccy: str
    name: str
    sd_pct: float        # priced 1-sd move
    done: bool = False
    outcome_pct: Optional[float] = None


@dataclass
class Alpha:
    pair: str
    kind: str            # 'spot' | 'vol'
    per_tick: float      # pct of spot, or vol pts, per tick
    ticks_left: int


@dataclass
class PairState:
    base_quotes: dict
    level: float = 0.0          # vol points added to ATM (front-weighted)
    skew: float = 0.0           # vols added to 25d RR (front-weighted)
    rv_ratio: float = 1.0
    corr: float = 0.0
    rr_beta: float = 0.0
    risk_off_dir: int = -1
    open_spot: float = 0.0
    day_open_quotes: dict = field(default_factory=dict)


def _nearest_psd(C: np.ndarray) -> np.ndarray:
    w, V = np.linalg.eigh((C + C.T) / 2)
    w = np.clip(w, 1e-6, None)
    C2 = V @ np.diag(w) @ V.T
    d = np.sqrt(np.diag(C2))
    return C2 / np.outer(d, d)


class MarketSim:
    """Seeded market for one session."""

    def __init__(self, seed: int, level: int, regime: Optional[str] = None, pairs: Optional[list[str]] = None,
                 use_live: bool = False, cfg: Optional[dict] = None) -> None:
        self.cfg = cfg or load_config()
        sc = self.cfg["simulator"]
        self.sc = sc
        self.seed = seed
        self.level = level
        self.lv = sc["levels"][level]
        self.rng = np.random.default_rng([seed, 1])
        self.ticks_per_day = int(sc["ticks_per_day"])
        self.days = int(sc["days"])
        self.total_ticks = self.ticks_per_day * self.days
        self.tick = 0
        self.exag = float(self.lv["exaggeration"])

        self.regime = regime or str(self.rng.choice(list(sc["regimes"])))
        self.rp = sc["regimes"][self.regime]
        if pairs is None:
            interv = self.regime == "intervention"
            if level == 1:
                pairs = [str(self.rng.choice(["USDJPY", "USDCHF"] if interv else L1_PAIRS))]
            elif level == 2:
                pools = [pl for pl in L2_POOLS if any(("JPY" in x or "CHF" in x) for x in pl)] if interv else L2_POOLS
                pairs = list(pools[int(self.rng.integers(len(pools)))])
            else:
                pairs = list(PAIRS)
        self.pairs = pairs

        static = build_market(use_live=use_live, cfg=self.cfg)
        self.source = static.source
        usd_spots = {p: static.spots[p] for p in USD_PAIRS}
        self.usd_val = usd_values_from_usd_pairs(usd_spots)
        self.curves = rate_curves(self.cfg)
        corr_cfg = sc["ccy_corr"]
        C = np.eye(len(NON_USD))
        for i, a in enumerate(NON_USD):
            for j, b in enumerate(NON_USD):
                if i != j:
                    C[i, j] = corr_cfg.get(a, {}).get(b, corr_cfg.get(b, {}).get(a, 0.0))
        self.chol = np.linalg.cholesky(_nearest_psd(C))

        self.state: dict[str, PairState] = {}
        lo, hi = self.rp["rv_iv_ratio"]
        clo, chi = self.rp["corr_mult"]
        for p in PAIRS:
            pdyn = sc["pair_dynamics"][p]
            st = PairState(base_quotes=static.quotes[p])
            st.rv_ratio = float(self.rng.uniform(lo, hi))
            st.corr = float(np.clip(pdyn["spot_vol_corr"] * self.rng.uniform(clo, chi), -0.95, 0.95))
            st.rr_beta = float(pdyn["rr_beta"])
            st.risk_off_dir = int(pdyn["risk_off_dir"])
            st.level = 0.6 * float(self.rp["vol_mean_shift"])
            st.skew = 0.6 * float(self.rp["skew_shift"]) * st.risk_off_dir
            self.state[p] = st
        self.kappa_day = sc["pair_dynamics"]["EURUSD"]["vol_mean_rev"] / 365 * TIME_COMPRESSION

        # trend / intervention set-up
        self.trend_ccy, self.trend_dir = None, 0
        if self.regime == "trending":
            self.trend_ccy = str(self.rng.choice([get_pair(p).base if get_pair(p).base != "USD" else get_pair(p).quote
                                                  for p in self.pairs]))
            self.trend_dir = int(self.rng.choice([-1, 1]))
        self.intervention = None
        if self.regime == "intervention":
            have = {c for p in self.pairs for c in (get_pair(p).base, get_pair(p).quote)}
            opts = [c for c in ("JPY", "CHF") if c in have] or ["JPY"]
            ccy = "JPY" if ("JPY" in opts and (len(opts) == 1 or self.rng.random() < 0.7)) else opts[-1]
            self.trend_ccy, self.trend_dir = ccy, -1   # weakening into intervention
            day = float(self.rng.uniform(3.0, 8.0))
            self.intervention = {"ccy": ccy, "day": day, "done": False,
                                 "size": float(self.rng.uniform(2.0, 3.5)) * (1.0 if ccy == "JPY" else 0.6)}
        # scheduled events
        self.events = self._schedule_events()
        # correlation episode (levels 2-3): one pair's spot/vol relationship changes mid-session
        self.episode = None
        if level >= 2 and self.rng.random() < 0.6:
            p = str(self.rng.choice(self.pairs))
            self.episode = {"pair": p, "day": float(self.rng.uniform(2, 7)), "mult": float(self.rng.choice([-0.3, 0.3, 1.6])),
                            "done": False}
        self.alphas: list[Alpha] = []
        for p in PAIRS:
            self.state[p].open_spot = self.spot(p)
            self.state[p].day_open_quotes = self.quotes(p)
        self._surf_cache: dict[str, LazyVolSurface] = {}
        self._prev_surf: dict[str, LazyVolSurface] = {}
        self.arb_log: list[str] = []
        self.day_open_spot = {p: self.spot(p) for p in PAIRS}

    # ------------------------------------------------------------------
    def _schedule_events(self) -> list[Event]:
        ccys = set()
        for p in self.pairs:
            ccys.update([get_pair(p).base, get_pair(p).quote])
        pool = [(c, n, sd) for c in ccys for n, sd in self.sc["events"].get(c, [])]
        k = int(self.sc["events_per_session"][self.regime])
        if self.regime == "cb_week":
            pool = [x for x in pool if "decision" in x[1]] or pool
        out = []
        idx = self.rng.permutation(len(pool))[:k]
        for i in idx:
            c, n, sd = pool[int(i)]
            day = float(self.rng.integers(1, self.days)) + float(self.rng.choice([0.25, 0.5, 0.75]))
            out.append(Event(day, c, n, float(sd)))
        return sorted(out, key=lambda e: e.day)

    @property
    def t(self) -> float:
        """Years since session start."""
        return self.tick / self.ticks_per_day / 365.0

    @property
    def day(self) -> int:
        return min(self.tick // self.ticks_per_day, self.days - 1)

    @property
    def day_float(self) -> float:
        return self.tick / self.ticks_per_day

    @property
    def finished(self) -> bool:
        return self.tick >= self.total_ticks

    def spot(self, pair: str) -> float:
        p = get_pair(pair)
        return self.usd_val[p.base] / self.usd_val[p.quote]

    def spots(self) -> dict[str, float]:
        return {p: self.spot(p) for p in PAIRS}

    def rd(self, pair: str, T: float = 0.25) -> float:
        return self.curves[get_pair(pair).quote](T)

    def rf(self, pair: str, T: float = 0.25) -> float:
        return self.curves[get_pair(pair).base](T)

    # ------------------------------------------------------------------
    @staticmethod
    def _w(T: float) -> float:
        return float(np.clip(np.sqrt(TENORS["1M"] / T), 0.45, 1.8))

    def event_var(self, pair: str, T: float) -> float:
        """Total event variance priced into expiry T (years from now)."""
        p = get_pair(pair)
        v = 0.0
        for e in self.events:
            if e.done or e.ccy not in (p.base, p.quote):
                continue
            te = (e.day - self.day_float) / 365.0
            if 0 <= te <= T:
                v += (e.sd_pct / 100) ** 2
        return v

    def quotes(self, pair: str) -> dict[str, SmileQuotes]:
        st = self.state[pair]
        out = {}
        prev_w = 0.0
        sd = self.cfg["smile_defaults"]
        for t in TENOR_LIST:
            b = st.base_quotes[t]
            T = TENORS[t]
            w = self._w(T)
            atm = max(b.atm + st.level / 100 * w, 0.3 * b.atm)
            ev = self.event_var(pair, T)
            if ev > 0:
                atm = float(np.sqrt(atm ** 2 + ev / T))
            # ATM calendar arbitrage: total variance must not fall
            if atm ** 2 * T < prev_w:
                atm = float(np.sqrt(prev_w / T)) + 1e-7
            prev_w = atm ** 2 * T
            drr = (st.rr_beta * st.level + st.skew) / 100 * w
            rr25 = b.rr25 + drr
            rr10 = b.rr10 + drr * sd["rr10_mult"]
            scale = float(np.clip(1 + 0.05 * st.level, 0.5, 2.5))
            out[t] = SmileQuotes(atm, rr25, b.bf25 * scale, rr10, b.bf10 * scale)
        return out

    def surface(self, pair: str) -> LazyVolSurface:
        if pair not in self._surf_cache:
            p = get_pair(pair)
            warm = self._prev_surf.get(pair)
            s = LazyVolSurface(p, self.spot(pair), self.curves[p.quote], self.curves[p.base], self.quotes(pair),
                               beta=self.cfg["smile_defaults"]["sabr_beta"],
                               tol=self.cfg["smile_defaults"]["sabr_tol_vol"] / 100, warm=warm,
                               fast=(self.tick % 5 != 0))  # full refit + arbitrage check every 5th tick
            self._surf_cache[pair] = s
        return self._surf_cache[pair]

    def single(self, pair: str) -> SingleMarket:
        s = self.surface(pair)
        return SingleMarket(pair, s.spot, self.rd(pair), self.rf(pair), lambda K, tau, s=s: s.vol(K, tau),
                            get_pair(pair), self.t)

    def forward_points(self, pair: str) -> dict[str, float]:
        p = get_pair(pair)
        S = self.spot(pair)
        return {t: forward_points(S, TENORS[t], self.rd(pair, TENORS[t]), self.rf(pair, TENORS[t]), p.pip)
                for t in TENOR_LIST}

    def stress(self) -> float:
        """0 (calm) to 1 (crisis) from regime and the vol level of active pairs."""
        base = {"calm": 0.0, "trending": 0.15, "risk_off": 0.5, "cb_week": 0.15, "intervention": 0.3}[self.regime]
        lvl = np.mean([max(self.state[p].level, 0) for p in self.pairs]) / 5.0
        return float(np.clip(base + lvl, 0, 1))

    # ------------------------------------------------------------------
    def add_alpha(self, pair: str, kind: str, total: float, ticks: int) -> None:
        """Informed flow: a move of ``total`` (% of spot, or vol pts) spread over ``ticks``."""
        self.alphas.append(Alpha(pair, kind, total / max(ticks, 1), max(ticks, 1)))

    def _ccy_move_for_pair(self, pair: str, pct: float) -> dict[str, float]:
        """Log move per currency that moves ``pair`` by ``pct`` %."""
        p = get_pair(pair)
        if p.base != "USD":
            return {p.base: pct / 100}
        return {p.quote: -pct / 100}

    def step(self) -> list[dict]:
        """Advance one tick. Returns news items generated this tick."""
        if self.finished:
            return []
        news: list[dict] = []
        self._prev_surf = dict(self._surf_cache)
        self._surf_cache = {}
        dt_days = 1.0 / self.ticks_per_day
        dt = dt_days / 365.0
        rng = self.rng
        pre_spot = self.spots()
        new_day = (self.tick % self.ticks_per_day == 0) and self.tick > 0

        # 1) currency diffusion
        z = self.chol @ rng.standard_normal(len(NON_USD))
        dlog = {}
        for i, c in enumerate(NON_USD):
            usd_pair = next(p for p in USD_PAIRS if c in p)
            st = self.state[usd_pair]
            sig = st.base_quotes["1M"].atm + st.level / 100
            sig = max(sig, 0.02) * st.rv_ratio
            dlog[c] = -0.5 * sig * sig * dt + sig * np.sqrt(dt) * z[i]
        diffusive = dict(dlog)

        # 2) trend drift
        if self.trend_ccy:
            dlog[self.trend_ccy] += self.trend_dir * self.rp["drift_pct_session"] * self.exag / 100 / self.total_ticks

        # 3) jumps
        lam = self.rp["jumps_per_session"] * self.exag / self.total_ticks
        for c in NON_USD + ["USD"]:
            if rng.random() < lam / (1 if c != "USD" else 2):
                size = self.rp["jump_size_pct"] * self.exag * (0.5 + rng.exponential(0.7))
                if self.regime == "risk_off" and c != "USD":
                    sgn = 1 if RISK_OFF_CCY[c] > 0 else -1
                    if abs(RISK_OFF_CCY[c]) < 0.5 and rng.random() < 0.4:
                        sgn = -sgn
                else:
                    sgn = int(rng.choice([-1, 1]))
                self._apply_ccy_jump(c, sgn * size, dlog, news, kind="jump")

        # 4) intervention
        if self.intervention and not self.intervention["done"]:
            iv = self.intervention
            if self.day_float >= iv["day"]:
                iv["done"] = True
                size = iv["size"] * self.exag
                self.trend_ccy = None
                c = iv["ccy"]
                dlog[c] += size / 100
                text = ("Japan's MoF confirms yen-buying intervention" if c == "JPY"
                        else "SNB intervenes to weaken the franc")
                if c == "CHF":
                    dlog[c] -= 2 * size / 100
                    size = -size
                self._vol_jump_for_ccy(c, abs(size) * 1.5, np.sign(size))
                news.append({"kind": "intervention", "ccy": c, "move_pct": size, "text": text})
            elif rng.random() < 0.6 / self.ticks_per_day and self.day_float > 1:
                news.append({"kind": "headline", "ccy": iv["ccy"], "move_pct": 0.0,
                             "text": ("Japan's top currency official: 'watching FX with urgency'" if iv["ccy"] == "JPY"
                                      else "SNB: 'ready to intervene if necessary'")})
                for p in PAIRS:
                    if iv["ccy"] in p:
                        self.state[p].level += 0.3

        # 5) scheduled events
        for e in self.events:
            if not e.done and self.day_float >= e.day:
                e.done = True
                surprise = float(rng.normal(0, e.sd_pct)) * float(rng.uniform(0.6, 1.4)) * self.exag
                e.outcome_pct = surprise
                move = {}
                if e.ccy == "USD":
                    for c in NON_USD:
                        dlog[c] -= surprise / 100 * float(rng.uniform(0.7, 1.0))
                else:
                    dlog[e.ccy] += surprise / 100
                if abs(surprise) > 1.3 * e.sd_pct:
                    self._vol_jump_for_ccy(e.ccy, abs(surprise) * 0.8, np.sign(surprise))
                news.append({"kind": "event", "ccy": e.ccy, "move_pct": surprise,
                             "text": f"{e.name}: {'hawkish/strong' if surprise > 0 else 'dovish/weak'} surprise, "
                                     f"{e.ccy} {'up' if surprise > 0 else 'down'} {abs(surprise):.2f}% vs USD; event vol crushed"})

        # 6) informed alpha
        for a in self.alphas:
            if a.ticks_left <= 0:
                continue
            a.ticks_left -= 1
            if a.kind == "spot":
                for c, v in self._ccy_move_for_pair(a.pair, a.per_tick).items():
                    dlog[c] += v
            else:
                self.state[a.pair].level += a.per_tick
        self.alphas = [a for a in self.alphas if a.ticks_left > 0]

        for c in NON_USD:
            self.usd_val[c] *= float(np.exp(dlog[c]))

        # 7) vol dynamics, correlated with each pair's own diffusive spot return
        if self.episode and not self.episode["done"] and self.day_float >= self.episode["day"]:
            ep = self.episode
            ep["done"] = True
            st = self.state[ep["pair"]]
            st.corr = float(np.clip(st.corr * ep["mult"], -0.95, 0.95))
            news.append({"kind": "regime", "ccy": "", "move_pct": 0.0, "pair": ep["pair"],
                         "text": (f"{ep['pair']}: spot/vol correlation regime shift "
                                  f"({'the usual relationship has flipped' if ep['mult'] < 0 else 'weaker than usual' if ep['mult'] < 1 else 'much stronger than usual'})")})
        vov = self.rp["vol_of_vol_pts_day"] * self.exag
        target = self.rp["vol_mean_shift"]
        skew_target = self.rp["skew_shift"]
        for p in PAIRS:
            st = self.state[p]
            pp = get_pair(p)
            r = diffusive.get(pp.base, 0.0) - diffusive.get(pp.quote, 0.0)
            sig = max(st.base_quotes["1M"].atm + st.level / 100, 0.02) * st.rv_ratio
            zs = r / (sig * np.sqrt(dt))
            zv = st.corr * zs + np.sqrt(1 - st.corr ** 2) * rng.standard_normal()
            st.level += self.kappa_day * (target - st.level) * dt_days + vov * np.sqrt(dt_days) * zv
            st.level = float(np.clip(st.level, -0.6 * st.base_quotes["1M"].atm * 100, 25))
            st.skew += self.kappa_day * (skew_target * st.risk_off_dir - st.skew) * dt_days
        if new_day:
            for p in PAIRS:
                self.state[p].day_open_quotes = self.quotes(p)
            self.day_open_spot = dict(pre_spot)
        self.tick += 1
        for p in self.pairs:
            if not atm_calendar_ok(self.quotes(p)):  # pragma: no cover - enforced in quotes()
                self.arb_log.append(f"tick {self.tick}: {p} ATM calendar arbitrage")
        for n in news:
            n["t"] = self.day_float
            n["day"] = self.day
        return news

    def _vol_jump_for_ccy(self, ccy: str, pts: float, sign: float) -> None:
        for p in PAIRS:
            pp = get_pair(p)
            if ccy in (pp.base, pp.quote) or ccy == "USD":
                st = self.state[p]
                st.level += pts
                base_up = sign if ccy == pp.base else -sign
                if ccy == "USD":
                    base_up = sign if pp.base == "USD" else -sign
                st.skew += 0.35 * pts * base_up

    def _apply_ccy_jump(self, c: str, pct: float, dlog: dict, news: list, kind: str) -> None:
        if c == "USD":
            for x in NON_USD:
                dlog[x] -= pct / 100
        else:
            dlog[c] += pct / 100
        self._vol_jump_for_ccy(c, abs(pct) * 1.2, np.sign(pct))
        texts = HEADLINES.get((c, 1 if pct > 0 else -1), [f"{c} moves sharply"])
        news.append({"kind": kind, "ccy": c, "move_pct": pct,
                     "text": f"{texts[int(self.rng.integers(len(texts)))]} ({c} {pct:+.2f}% vs USD)"})

    def upcoming_events(self) -> list[dict]:
        return [{"day": e.day, "ccy": e.ccy, "name": e.name, "priced_sd_pct": e.sd_pct}
                for e in self.events if not e.done]
