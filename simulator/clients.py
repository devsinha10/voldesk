"""Client flow: RFQ generation, quote metrics and the client's trade decision.

Quote conventions (what you type as bid/offer):
* vanilla, straddle: the option vol (%)
* strangle: one vol for both wings (%)
* risk reversal: RR in vols = vol(call) - vol(put), for long call / short put
* butterfly: fly in vols = average wing vol - ATM vol (long wings, short ATM)

The client trades if your price beats a hidden competitive level:
fair mid +/- competitive half-spread + noise. Informed clients add their
private edge, and the market then drifts their way (see MarketSim.add_alpha).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from engine.fx_conventions import TENORS, get_pair
from engine.structures import Leg, SingleMarket, build

CLIENT_LABEL = {"corporate": "Corporate hedger", "real_money": "Real money", "macro_hf": "Macro hedge fund",
                "leveraged": "Leveraged / spec"}

KIND_LABEL = {"vanilla": "vanilla", "straddle": "ATM straddle", "strangle": "25d strangle",
              "risk_reversal": "25d risk reversal", "butterfly": "25d butterfly"}

CLIENT_PROFILES = {
    # kinds and weights, tenors and weights, probability the client BUYS
    "corporate": ([("vanilla", 0.6), ("risk_reversal", 0.4)], [("1M", 1), ("2M", 1), ("3M", 2), ("6M", 2), ("1Y", 1)], 0.8),
    "real_money": ([("vanilla", 0.5), ("risk_reversal", 0.3), ("strangle", 0.2)], [("3M", 2), ("6M", 2), ("1Y", 1)], 0.5),
    "macro_hf": ([("straddle", 0.3), ("strangle", 0.2), ("risk_reversal", 0.3), ("vanilla", 0.1), ("butterfly", 0.1)],
                 [("1W", 2), ("2W", 1), ("1M", 2), ("2M", 1), ("3M", 1)], 0.65),
    "leveraged": ([("vanilla", 0.6), ("straddle", 0.2), ("risk_reversal", 0.2)], [("1W", 2), ("2W", 1), ("1M", 2)], 0.55),
}


@dataclass
class RFQ:
    id: int
    created_tick: int
    expires_tick: int
    pair: str
    kind: str
    tenor: str
    notional: float           # base units
    client_type: str
    client_side: int          # +1 client buys the structure, -1 sells (hidden)
    legs: tuple               # long-structure legs, notional 1 unit each
    cp: str = ""
    vanilla_delta: float = 0.0
    half_width_mult: float = 1.0
    noise: float = 0.0        # vol pts
    info_edge: float = 0.0    # vol pts the informed client is willing to give up
    status: str = "open"      # open | traded | no_trade | passed | missed
    bid: Optional[float] = None
    offer: Optional[float] = None
    fair_at_quote: Optional[float] = None
    edge_quote_ccy: float = 0.0
    trade_id: Optional[int] = None
    informed: bool = False
    detail: dict = field(default_factory=dict)

    def describe(self) -> str:
        p = get_pair(self.pair)
        if self.kind == "vanilla":
            d = "ATM" if abs(self.vanilla_delta - 0.5) < 1e-9 else f"{int(round(self.vanilla_delta * 100))}d"
            what = f"{d} {p.base} {'call' if self.cp == 'C' else 'put'}"
        else:
            what = KIND_LABEL[self.kind]
        return f"{self.pair} {self.tenor} {what}, {p.base} {self.notional / 1e6:,.0f}m"

    def quote_unit(self) -> str:
        return {"vanilla": "vol %", "straddle": "vol %", "strangle": "strangle vol %",
                "risk_reversal": "RR vols (call - put)", "butterfly": "fly vols"}[self.kind]


def _legs_for(kind: str, mkt: SingleMarket, tenor: str, cp: str, vdelta: float) -> tuple:
    if kind == "vanilla":
        md = None if abs(vdelta - 0.5) < 1e-9 else vdelta
        s = build("call" if cp == "C" else "put", mkt, tenor, 1.0, moneyness_delta=md)
    elif kind == "butterfly":
        s = build("fx_butterfly", mkt, tenor, 1.0)
    else:
        s = build(kind, mkt, tenor, 1.0)
    return s.legs


def _bump_weights(kind: str, legs: tuple) -> list[float]:
    """d(leg vol)/d(quote metric) for each leg (legs of the LONG structure)."""
    if kind in ("vanilla", "straddle", "strangle"):
        return [1.0] * len(legs)
    if kind == "risk_reversal":
        return [0.5 if l.cp == "C" else -0.5 for l in legs]
    if kind == "butterfly":
        return [1.0 if "wing" in l.label else 0.0 for l in legs]
    raise ValueError(kind)


def metric_and_vega(rfq: RFQ, mkt: SingleMarket) -> tuple[float, float, float]:
    """(fair metric in vol pts, dV/d(metric) per vol pt per unit, mid value per unit) for the LONG structure."""
    from engine.fx_pricer import greeks

    vols, vegas, value = [], [], 0.0
    for l in rfq.legs:
        tau = l.expiry - mkt.t
        v = mkt.vol(l.K, tau)
        g = greeks(mkt.spot, l.K, tau, mkt.rd, mkt.rf, v, l.cp)
        vols.append(v)
        vegas.append(g.vega * 0.01 * l.notional)
        value += l.notional * g.price
    w = _bump_weights(rfq.kind, rfq.legs)
    if rfq.kind in ("vanilla", "straddle"):
        metric = vols[0]
    elif rfq.kind == "strangle":
        metric = float(np.average(vols, weights=np.abs(vegas)))
    elif rfq.kind == "risk_reversal":
        vc = [v for v, l in zip(vols, rfq.legs) if l.cp == "C"][0]
        vp = [v for v, l in zip(vols, rfq.legs) if l.cp == "P"][0]
        metric = vc - vp
    else:
        wing = [v for v, l in zip(vols, rfq.legs) if "wing" in l.label]
        atm = [v for v, l in zip(vols, rfq.legs) if "ATM" in l.label][0]
        metric = float(np.mean(wing)) - atm
    dvdq = float(sum(vg * wi for vg, wi in zip(vegas, w)))
    return metric * 100, dvdq, value


class ClientFlow:
    """Seeded RFQ generator (own RNG stream, independent of trader actions)."""

    def __init__(self, seed: int, level_cfg: dict, sim_cfg: dict, pairs: list[str], ticks_per_day: int,
                 regime: str) -> None:
        self.rng = np.random.default_rng([seed, 2])
        self.lv = level_cfg
        self.sc = sim_cfg
        self.pairs = pairs
        self.tpd = ticks_per_day
        self.regime = regime
        self.next_id = 1
        cl = sim_cfg["clients"]
        names = list(cl)
        w = np.array([cl[n]["weight"] for n in names], dtype=float)
        mix = self.rng.dirichlet(w / w.sum() * 12)  # client mix varies by session
        self.mix = dict(zip(names, mix))

    def maybe_generate(self, tick: int, market) -> list[RFQ]:
        rate = self.lv["rfq_rate_per_day"] / self.tpd * (1.4 if self.regime == "risk_off" else 1.0)
        n = int(self.rng.poisson(rate))
        if self.rng.random() < self.lv["burst_prob"]:
            n += int(self.rng.integers(3, 6))
        return [self._one(tick, market) for _ in range(n)]

    def _one(self, tick: int, market) -> RFQ:
        rng = self.rng
        names = list(self.mix)
        ctype = str(rng.choice(names, p=np.array(list(self.mix.values()))))
        kinds, tenors, p_buy = CLIENT_PROFILES[ctype]
        kind = str(rng.choice([k for k, _ in kinds], p=np.array([w for _, w in kinds]) / sum(w for _, w in kinds)))
        tw = np.array([w for _, w in tenors], dtype=float)
        tenor = str(rng.choice([t for t, _ in tenors], p=tw / tw.sum()))
        pair = str(rng.choice(self.pairs))
        cfg_c = self.sc["clients"][ctype]
        notional = float(rng.choice(self.sc["base_notional_musd"])) * cfg_c["size_mult"] * 1e6
        notional = round(notional / 5e6) * 5e6 or 5e6
        side = 1 if rng.random() < p_buy else -1
        cp = str(rng.choice(["C", "P"]))
        vdelta = float(rng.choice([0.5, 0.25, 0.25, 0.10]))
        timeout = rng.uniform(*self.sc["quote_timeout_s"]) / self.sc["tick_seconds"]
        mkt = market.single(pair)
        legs = _legs_for(kind, mkt, tenor, cp, vdelta)
        informed = rng.random() < cfg_c["informed"]
        rfq = RFQ(self.next_id, tick, tick + int(np.ceil(timeout)), pair, kind, tenor, notional, ctype, side, legs,
                  cp, vdelta, half_width_mult=float(rng.uniform(0.5, 1.1)),
                  noise=float(rng.normal(0, cfg_c["noise_vol"])), informed=informed)
        self.next_id += 1
        if informed:
            # the informed client knows where the market is going: push it their way
            exag = market.exag
            ticks = int(rng.integers(self.tpd // 2, 2 * self.tpd))
            if kind in ("straddle", "strangle", "butterfly"):
                pts = float(rng.uniform(0.8, 2.0)) * exag * side * (-1 if kind == "butterfly" else 1)
                market.add_alpha(pair, "vol", pts, ticks)
                rfq.info_edge = abs(pts) * 0.3
                rfq.detail["alpha"] = {"kind": "vol", "total_pts": pts, "ticks": ticks}
            else:
                direction = side * (1 if (kind == "risk_reversal" or cp == "C") else -1)
                pct = float(rng.uniform(0.4, 1.0)) * exag * direction
                market.add_alpha(pair, "spot", pct, ticks)
                rfq.info_edge = 0.4
                rfq.detail["alpha"] = {"kind": "spot", "total_pct": pct, "ticks": ticks}
        return rfq


def competitive_levels(rfq: RFQ, fair: float, idb_half: float) -> tuple[float, float]:
    """Hidden (bid, offer) the client would get elsewhere, in quote-metric vol pts."""
    hw = idb_half * rfq.half_width_mult
    if rfq.kind in ("risk_reversal", "butterfly"):
        hw *= 0.6
    mid = fair + rfq.noise * (0.5 if rfq.kind in ("risk_reversal", "butterfly") else 1.0)
    return mid - hw - rfq.info_edge * (rfq.client_side < 0), mid + hw + rfq.info_edge * (rfq.client_side > 0)


def client_decides(rfq: RFQ, bid: float, offer: float, fair: float, idb_half: float) -> bool:
    """True if the client trades on our two-way price."""
    if offer <= bid:
        return False
    cb, co = competitive_levels(rfq, fair, idb_half)
    if rfq.client_side > 0:
        return offer <= co
    return bid >= cb
