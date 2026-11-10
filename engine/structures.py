"""Option structures, single-underlying scenario markets and desk-unit exposures.

A :class:`Structure` is a list of :class:`Leg` objects. Each leg is an option,
or a spot position (used for delta hedges and collars). Valuation and Greeks
are sums over legs, priced off a :class:`SingleMarket`.

Desk units (per base notional ``N`` signed, + = long):

* delta        : base-ccy notional (dV/dS * N)
* delta_pa     : premium-adjusted delta in base notional
* gamma_1pct   : change in delta (base notional) for a +1% spot move
* vega         : quote-ccy P&L per +1 vol point
* theta        : quote-ccy P&L per calendar day
* vanna        : change in delta (base notional) per +1 vol point
* volga        : change in vega (quote ccy per vol pt) per +1 vol point
* charm        : change in delta (base notional) per calendar day
* rho_d/rho_f  : quote-ccy P&L per +1bp in domestic/foreign rate
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Callable, Optional

import numpy as np

from engine.fx_conventions import TENORS, FXPair, delta as conv_delta, atm_dns_strike, strike_from_delta
from engine.fx_pricer import forward, greeks, price

VolFn = Callable[[float, float], float]  # (K, tau) -> vol


# ---------------------------------------------------------------------------
# Market for one underlying (FX pair or equity index)
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class SingleMarket:
    """Spot, flat rates and a vol function for one underlying.

    ``t`` is "now" in years from inception, so a leg's time to expiry is
    ``leg.expiry - t``. ``vol_fn(K, tau)`` gives implied vol.
    """

    name: str
    spot: float
    rd: float
    rf: float
    vol_fn: VolFn
    pair: Optional[FXPair] = None
    t: float = 0.0

    def vol(self, K: float, tau: float) -> float:
        return float(self.vol_fn(K, max(tau, 1e-6)))

    def forward(self, tau: float) -> float:
        return float(forward(self.spot, tau, self.rd, self.rf))

    @property
    def premium_adjusted(self) -> bool:
        return bool(self.pair and self.pair.premium_adjusted)

    def convention(self, tau: float) -> str:
        return self.pair.delta_convention(tau) if self.pair else "spot"

    # -- strikes ------------------------------------------------------------
    def atm_strike(self, tau: float) -> float:
        """ATM: DNS for FX (convention-aware), ATM-forward DNS for equity."""
        K = self.forward(tau)
        for _ in range(30):
            v = self.vol(K, tau)
            K_new = atm_dns_strike(self.forward(tau), tau, v, self.premium_adjusted)
            if abs(K_new - K) < 1e-12 * K:
                break
            K = K_new
        return K

    def strike_for_delta(self, tau: float, target_delta: float) -> float:
        """Smile-consistent strike for a signed market-convention delta."""
        cp = "C" if target_delta > 0 else "P"
        conv = self.convention(tau)
        v = self.vol(self.forward(tau), tau)
        K = self.forward(tau)
        for _ in range(60):
            K_new = strike_from_delta(target_delta, self.spot, tau, self.rd, self.rf, v, cp, conv)
            v_new = self.vol(K_new, tau)
            if abs(K_new - K) < 1e-12 * K and abs(v_new - v) < 1e-12:
                break
            K, v = K_new, v_new
        return K_new

    # -- scenario bumps -----------------------------------------------------
    def bump_spot(self, pct: float, sticky: str = "strike") -> "SingleMarket":
        """Spot move of ``pct`` percent. sticky='strike' keeps vol(K) fixed;
        sticky='delta' keeps vol at the same moneyness K/S."""
        S1 = self.spot * (1 + pct / 100)
        if sticky == "strike":
            return replace(self, spot=S1)
        ratio = self.spot / S1
        f = self.vol_fn
        return replace(self, spot=S1, vol_fn=lambda K, tau: f(K * ratio, tau))

    def bump_vol(self, points: float, tenor_weight: Optional[Callable[[float], float]] = None
                 ) -> "SingleMarket":
        """Add ``points`` vol points (times an optional weight by tau)."""
        f = self.vol_fn
        w = tenor_weight or (lambda tau: 1.0)
        return replace(self, vol_fn=lambda K, tau: max(f(K, tau) + points / 100 * w(tau), 1e-4))

    def bump_skew(self, rr_points: float) -> "SingleMarket":
        """Steepen the skew: adds roughly ``rr_points`` to the 25d RR at every tenor
        (vol shift proportional to standardised moneyness, puts up if negative)."""
        f, S, rd, rf = self.vol_fn, self.spot, self.rd, self.rf

        def g(K: float, tau: float) -> float:
            v0 = f(K, tau)
            F = S * np.exp((rd - rf) * tau)
            x = np.log(K / F) / (v0 * np.sqrt(tau))
            # 25d strikes sit near x = +/-0.674; scale so RR moves by rr_points
            return max(v0 + rr_points / 100 * np.clip(x, -2.5, 2.5) / (2 * 0.674), 1e-4)

        return replace(self, vol_fn=g)

    def invert_term(self, points: float) -> "SingleMarket":
        """Front end up, back end down: +points at ON fading to -points/2 at 1Y."""
        def w(tau: float) -> float:
            x = np.clip(np.log(tau / TENORS["ON"]) / np.log(1.0 / TENORS["ON"]), 0, 1)
            return 1.0 - 1.5 * x
        return self.bump_vol(points, w)

    def pass_time(self, days: float) -> "SingleMarket":
        """Calendar time passes (vol function in tau unchanged: the smile 'rolls')."""
        return replace(self, t=self.t + days / 365)

    def bump_rate(self, which: str, bp: float) -> "SingleMarket":
        if which == "rd":
            return replace(self, rd=self.rd + bp * 1e-4)
        return replace(self, rf=self.rf + bp * 1e-4)


def market_from_surface(surface, t: float = 0.0) -> SingleMarket:
    """Wrap a :class:`engine.surface.VolSurface` (flat rates at 3M) as a SingleMarket."""
    return SingleMarket(name=surface.pair.name, spot=surface.spot, rd=surface.rd(0.25),
                        rf=surface.rf(0.25), vol_fn=lambda K, tau: surface.vol(K, tau),
                        pair=surface.pair, t=t)


def equity_market(spot: float, r: float, q: float, atm_vol: float,
                  skew_per_10pct: float, name: str = "SPX") -> SingleMarket:
    """Equity index market with a linear-in-log-moneyness skew (vol pts per 10%)."""
    def vf(K: float, tau: float) -> float:
        F = spot * np.exp((r - q) * tau)
        return max(atm_vol + skew_per_10pct / 100 * np.log(K / F) / 0.10, 0.03)
    return SingleMarket(name=name, spot=spot, rd=r, rf=q, vol_fn=vf, pair=None)


def flat_market(pair: FXPair, spot: float, rd: float, rf: float, vol: float) -> SingleMarket:
    """Flat-vol FX market (handy for tests and clean drills)."""
    return SingleMarket(pair.name, spot, rd, rf, lambda K, tau: vol, pair)


# ---------------------------------------------------------------------------
# Legs and structures
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Leg:
    """One leg. kind: 'option' or 'spot'. notional: signed base units."""

    kind: str
    notional: float
    K: float = 0.0
    expiry: float = 0.0
    cp: str = "C"
    label: str = ""


@dataclass(frozen=True)
class Exposure:
    """Aggregated exposures in desk units (see module docstring)."""

    value: float
    delta: float
    delta_pa: float
    gamma_1pct: float
    vega: float
    theta: float
    vanna: float
    volga: float
    charm: float
    rho_d: float
    rho_f: float
    vega_by_tenor: dict = field(default_factory=dict)

    def signs(self, tol_rel: float = 0.02, scale: Optional[dict] = None) -> dict[str, int]:
        """Sign of each Greek, with values small relative to ``scale`` treated as 0."""
        out = {}
        for k in ("delta", "gamma_1pct", "theta", "vega", "vanna", "volga", "charm"):
            v = getattr(self, k)
            s = (scale or {}).get(k, 0.0)
            out[k] = 0 if abs(v) <= tol_rel * s else int(np.sign(v))
        return out


def bucket_for(tau: float) -> str:
    """Nearest pillar tenor (in log time) for vega bucketing."""
    names = list(TENORS)
    ts = np.array([TENORS[n] for n in names])
    return names[int(np.argmin(np.abs(np.log(ts) - np.log(max(tau, 1e-6)))))]


def leg_greeks(leg: Leg, mkt: SingleMarket):
    """Raw per-unit Greeks for an option leg (None for spot legs)."""
    tau = leg.expiry - mkt.t
    v = mkt.vol(leg.K, tau) if tau > 0 else 0.2
    return greeks(mkt.spot, leg.K, tau, mkt.rd, mkt.rf, v, leg.cp), tau


@dataclass(frozen=True)
class Structure:
    """A named collection of legs."""

    name: str
    legs: tuple[Leg, ...]
    description: str = ""

    def value(self, mkt: SingleMarket) -> float:
        tot = 0.0
        for leg in self.legs:
            if leg.kind == "spot":
                tot += leg.notional * (mkt.spot - leg.K)
            else:
                tau = leg.expiry - mkt.t
                v = mkt.vol(leg.K, tau) if tau > 0 else 0.2
                tot += leg.notional * float(price(mkt.spot, leg.K, tau, mkt.rd, mkt.rf, v, leg.cp))
        return tot

    def exposure(self, mkt: SingleMarket) -> Exposure:
        S = mkt.spot
        acc = dict(value=0.0, delta=0.0, delta_pa=0.0, gamma_1pct=0.0, vega=0.0, theta=0.0,
                   vanna=0.0, volga=0.0, charm=0.0, rho_d=0.0, rho_f=0.0)
        vbt: dict[str, float] = {}
        for leg in self.legs:
            N = leg.notional
            if leg.kind == "spot":
                acc["value"] += N * (S - leg.K)
                acc["delta"] += N
                acc["delta_pa"] += N
                continue
            g, tau = leg_greeks(leg, mkt)
            acc["value"] += N * g.price
            acc["delta"] += N * g.delta
            acc["delta_pa"] += N * g.delta_pa
            acc["gamma_1pct"] += N * g.gamma * S * 0.01
            acc["vega"] += N * g.vega * 0.01
            acc["theta"] += N * g.theta / 365
            acc["vanna"] += N * g.vanna * 0.01
            acc["volga"] += N * g.volga * 1e-4
            acc["charm"] += N * g.charm / 365
            acc["rho_d"] += N * g.rho_d * 1e-4
            acc["rho_f"] += N * g.rho_f * 1e-4
            if tau > 0:
                b = bucket_for(tau)
                vbt[b] = vbt.get(b, 0.0) + N * g.vega * 0.01
        return Exposure(vega_by_tenor=vbt, **acc)

    def scaled(self, k: float) -> "Structure":
        return replace(self, legs=tuple(replace(l, notional=l.notional * k) for l in self.legs))

    def delta_hedged(self, mkt: SingleMarket, use_pa: bool = False) -> "Structure":
        """Add a spot leg that flattens delta (PA delta if ``use_pa``)."""
        e = self.exposure(mkt)
        d = e.delta_pa if use_pa else e.delta
        hedge = Leg("spot", -d, K=mkt.spot, label="delta hedge")
        return Structure(self.name + " (delta-hedged)", self.legs + (hedge,), self.description)


STRUCTURE_KINDS = ["call", "put", "straddle", "strangle", "risk_reversal", "call_spread",
                   "put_spread", "butterfly", "calendar", "collar", "ratio_spread"]


def build(kind: str, mkt: SingleMarket, tenor: str | float, notional: float = 1.0,
          side: int = 1, wing_delta: float = 0.25, moneyness_delta: Optional[float] = None,
          far_tenor: str | float = "3M", hedged: bool = False) -> Structure:
    """Build a standard structure.

    side: +1 long, -1 short. For RR, long = long call / short put.
    moneyness_delta: for single calls/puts, the absolute delta of the strike
    (None = ATM).
    """
    tau = TENORS[tenor] if isinstance(tenor, str) else float(tenor)
    T = mkt.t + tau
    N = side * notional
    atm = mkt.atm_strike(tau)
    kc = lambda d: mkt.strike_for_delta(tau, abs(d))
    kp = lambda d: mkt.strike_for_delta(tau, -abs(d))
    L = lambda cp, K, n, lab="", exp=T: Leg("option", n, K, exp, cp, lab)
    if kind == "call":
        K = atm if moneyness_delta is None else kc(moneyness_delta)
        legs = (L("C", K, N, "call"),)
    elif kind == "put":
        K = atm if moneyness_delta is None else kp(moneyness_delta)
        legs = (L("P", K, N, "put"),)
    elif kind == "straddle":
        legs = (L("C", atm, N, "ATM call"), L("P", atm, N, "ATM put"))
    elif kind == "strangle":
        legs = (L("C", kc(wing_delta), N, "OTM call"), L("P", kp(wing_delta), N, "OTM put"))
    elif kind == "risk_reversal":
        legs = (L("C", kc(wing_delta), N, "long call"), L("P", kp(wing_delta), -N, "short put"))
    elif kind == "call_spread":
        legs = (L("C", atm, N, "long ATM call"), L("C", kc(wing_delta), -N, "short OTM call"))
    elif kind == "put_spread":
        legs = (L("P", atm, N, "long ATM put"), L("P", kp(wing_delta), -N, "short OTM put"))
    elif kind == "butterfly":
        k1, k3 = kp(wing_delta), kc(wing_delta)
        legs = (L("C", k1, N, "low wing"), L("C", atm, -2 * N, "body x2"), L("C", k3, N, "high wing"))
    elif kind == "calendar":
        tau_far = TENORS[far_tenor] if isinstance(far_tenor, str) else float(far_tenor)
        legs = (L("C", atm, -N, "short near call"), L("C", atm, N, "long far call", mkt.t + tau_far))
    elif kind == "collar":
        legs = (Leg("spot", N, mkt.spot, 0.0, "C", "long spot"),
                L("P", kp(wing_delta), N, "long put"), L("C", kc(wing_delta), -N, "short call"))
    elif kind == "ratio_spread":
        legs = (L("C", atm, N, "long 1x ATM call"), L("C", kc(wing_delta), -2 * N, "short 2x OTM call"))
    else:
        raise ValueError(f"Unknown structure {kind!r}")
    s = Structure(kind, legs)
    return s.delta_hedged(mkt) if hedged else s


def describe(kind: str, side: int, tenor: str, name: str, hedged: bool = False,
             wing_delta: float = 0.25, moneyness_delta: Optional[float] = None) -> str:
    """Plain-English description of a structure for question text."""
    s = "long" if side > 0 else "short"
    wd = int(round(wing_delta * 100))
    names = {
        "call": (f"{'ATM' if moneyness_delta is None else str(int(round(moneyness_delta*100)))+'-delta'} call"),
        "put": (f"{'ATM' if moneyness_delta is None else str(int(round(moneyness_delta*100)))+'-delta'} put"),
        "straddle": "ATM straddle", "strangle": f"{wd}-delta strangle",
        "risk_reversal": f"{wd}-delta risk reversal (call over put)",
        "call_spread": f"ATM/{wd}-delta call spread", "put_spread": f"ATM/{wd}-delta put spread",
        "butterfly": f"{wd}-delta call butterfly (1x2x1)", "calendar": "ATM call calendar (short near, long 3M)",
        "collar": f"collar (long spot, long {wd}d put, short {wd}d call)",
        "ratio_spread": f"1x2 call ratio spread (long ATM, short 2x {wd}d)",
    }
    h = ", delta-hedged" if hedged else ""
    return f"{s} a {tenor} {name} {names[kind]}{h}"
