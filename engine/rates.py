"""Rates engine: bonds, duration/convexity, curves, swaps, Bachelier swaptions,
bond futures (conversion factor, CTD), carry/roll, OIS meeting probabilities.

Sign conventions
----------------
* Yields/rates are decimals (0.04 = 4%).
* ``dv01`` follows the desk convention that LONG DURATION = POSITIVE DV01:
  dv01 = P&L for a 1bp FALL in yields = -dPV/dy * 1bp.
  A long bond, a receiver swap and a receiver swaption all have dv01 > 0.
* Bond prices are per 100 face, settlement on a coupon date (no accrued).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm

BP = 1e-4


# ---------------------------------------------------------------------------
# Bonds from yield
# ---------------------------------------------------------------------------
def _cashflows(coupon: float, maturity: float, freq: int, face: float = 100.0):
    n = int(round(maturity * freq))
    if n < 1:
        raise ValueError("maturity too short for the frequency")
    t = np.arange(1, n + 1) / freq
    cf = np.full(n, face * coupon / freq)
    cf[-1] += face
    return t, cf


def bond_price(y: float, coupon: float, maturity: float, freq: int = 2, face: float = 100.0) -> float:
    """Price per 100 from yield ``y`` compounded ``freq`` times a year."""
    t, cf = _cashflows(coupon, maturity, freq, face)
    return float(np.sum(cf / (1 + y / freq) ** (t * freq)))


def bond_yield(P: float, coupon: float, maturity: float, freq: int = 2, face: float = 100.0) -> float:
    """Yield to maturity from price."""
    return float(brentq(lambda y: bond_price(y, coupon, maturity, freq, face) - P, -0.5, 2.0, xtol=1e-14))


@dataclass(frozen=True)
class BondRisk:
    """Price and risk for 100 face."""

    price: float
    macaulay: float
    modified: float
    convexity: float
    dv01: float  # per 100 face, positive for a long bond


def bond_risk(y: float, coupon: float, maturity: float, freq: int = 2, face: float = 100.0) -> BondRisk:
    """Macaulay/modified duration, convexity (in years^2) and DV01."""
    t, cf = _cashflows(coupon, maturity, freq, face)
    disc = (1 + y / freq) ** (-(t * freq))
    pv = cf * disc
    P = float(pv.sum())
    mac = float((t * pv).sum() / P)
    mod = mac / (1 + y / freq)
    conv = float((pv * t * (t + 1 / freq)).sum() / (P * (1 + y / freq) ** 2))
    return BondRisk(P, mac, mod, conv, mod * P * BP)


def price_change_approx(P: float, mod_dur: float, convexity: float, dy: float) -> dict[str, float]:
    """dP ~ -D P dy + 0.5 C P dy^2 (returns the duration and convexity terms)."""
    dur = -mod_dur * P * dy
    cvx = 0.5 * convexity * P * dy * dy
    return {"duration_term": dur, "convexity_term": cvx, "total": dur + cvx}


def zero_coupon_price(y: float, maturity: float, freq: int = 1, face: float = 100.0) -> float:
    """Zero-coupon bond price (annual compounding by default)."""
    return face / (1 + y / freq) ** (maturity * freq)


# ---------------------------------------------------------------------------
# Curves
# ---------------------------------------------------------------------------
class ZeroCurve:
    """Piecewise-linear continuously compounded zero curve."""

    def __init__(self, points: dict[float, float]) -> None:
        ts = sorted(float(k) for k in points)
        self.t = np.array(ts)
        self.z = np.array([float(points[k] if k in points else points[str(k)]) for k in ts])

    @classmethod
    def flat(cls, r: float) -> "ZeroCurve":
        return cls({0.01: r, 50.0: r})

    @classmethod
    def from_pct(cls, points: dict) -> "ZeroCurve":
        return cls({float(k): float(v) / 100 for k, v in points.items()})

    def zero(self, T):
        return np.interp(T, self.t, self.z)

    def df(self, T):
        T = np.asarray(T, dtype=float)
        return np.exp(-self.zero(T) * T)

    def fwd(self, t1: float, t2: float) -> float:
        """Simple-compounded forward rate between t1 and t2."""
        return float((self.df(t1) / self.df(t2) - 1) / (t2 - t1))

    def shifted(self, bp: float) -> "ZeroCurve":
        return ZeroCurve({t: z + bp * BP for t, z in zip(self.t, self.z)})

    def key_rate_bumped(self, pillar: float, bp: float, pillars: list[float]) -> "ZeroCurve":
        """Triangular bump of ``bp`` centred at ``pillar`` (zero at neighbouring pillars)."""
        ps = sorted(pillars)
        i = ps.index(pillar)
        lo = ps[i - 1] if i > 0 else None
        hi = ps[i + 1] if i < len(ps) - 1 else None
        grid = sorted(set(list(self.t) + ps))

        def w(t: float) -> float:
            if t == pillar:
                return 1.0
            if t < pillar:
                return 1.0 if lo is None else max(0.0, (t - lo) / (pillar - lo))
            return 1.0 if hi is None else max(0.0, (hi - t) / (hi - pillar))

        return ZeroCurve({t: float(self.zero(t)) + bp * BP * w(t) for t in grid})


# ---------------------------------------------------------------------------
# Swaps (single curve)
# ---------------------------------------------------------------------------
def annuity(curve: ZeroCurve, start: float, end: float, freq: int = 1) -> float:
    """PV01-style annuity: sum of accrual * DF over fixed payment dates."""
    n = int(round((end - start) * freq))
    pay = start + np.arange(1, n + 1) / freq
    return float(np.sum(curve.df(pay) / freq))


def par_swap_rate(curve: ZeroCurve, start: float, end: float, freq: int = 1) -> float:
    """Par rate of a (forward-starting if start > 0) swap."""
    return float((curve.df(start) - curve.df(end)) / annuity(curve, start, end, freq))


def swap_pv(curve: ZeroCurve, fixed_rate: float, start: float, end: float, notional: float,
            direction: str = "receive", freq: int = 1) -> float:
    """PV of a swap. direction='receive' (receive fixed) or 'pay'."""
    A = annuity(curve, start, end, freq)
    S = par_swap_rate(curve, start, end, freq)
    sgn = 1 if direction == "receive" else -1
    return sgn * notional * (fixed_rate - S) * A


def swap_dv01(curve: ZeroCurve, fixed_rate: float, start: float, end: float, notional: float,
              direction: str = "receive", freq: int = 1) -> float:
    """DV01 by central parallel bump; positive = long duration (receiver)."""
    up = swap_pv(curve.shifted(1), fixed_rate, start, end, notional, direction, freq)
    dn = swap_pv(curve.shifted(-1), fixed_rate, start, end, notional, direction, freq)
    return float((dn - up) / 2)


def floater_dv01(curve: ZeroCurve, notional: float, next_reset: float = 0.25) -> float:
    """DV01 of a floating-rate note that resets at ``next_reset``: it behaves like
    a zero-coupon bond to the next reset, so duration is roughly the time to reset."""
    pv = lambda c: notional * float(c.df(next_reset)) * (1 + curve.fwd(0.0, next_reset) * next_reset)
    return float((pv(curve.shifted(-1)) - pv(curve.shifted(1))) / 2)


def key_rate_dv01s(pv_fn, curve: ZeroCurve, pillars: list[float]) -> dict[float, float]:
    """Key-rate DV01s (positive = long duration at that pillar)."""
    out = {}
    for p in pillars:
        up = pv_fn(curve.key_rate_bumped(p, 1, pillars))
        dn = pv_fn(curve.key_rate_bumped(p, -1, pillars))
        out[p] = float((dn - up) / 2)
    return out


# ---------------------------------------------------------------------------
# Swaptions: Bachelier (normal vol)
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class SwaptionRisk:
    """Swaption price and Greeks w.r.t. the forward swap rate, per notional.

    delta_rate: dPV/dF (per 1.00 of rate). dv01: positive = long duration.
    gamma: d2PV/dF2 per (1bp)^2 scaled to "change in dv01 per 1bp".
    vega_bp: PV change per +1bp of normal vol.
    """

    price: float
    delta_rate: float
    dv01: float
    gamma_dv01_per_bp: float
    vega_bp: float


def bachelier_swaption(F: float, K: float, T: float, normal_vol: float, A: float,
                       kind: str = "payer", notional: float = 1.0) -> SwaptionRisk:
    """Bachelier swaption. ``normal_vol`` in absolute rate (0.0085 = 85bp)."""
    sd = normal_vol * np.sqrt(T)
    d = (F - K) / sd
    if kind == "payer":
        pv = A * ((F - K) * norm.cdf(d) + sd * norm.pdf(d))
        dlt = A * norm.cdf(d)
    elif kind == "receiver":
        pv = A * ((K - F) * norm.cdf(-d) + sd * norm.pdf(d))
        dlt = -A * norm.cdf(-d)
    else:
        raise ValueError(kind)
    gamma = A * norm.pdf(d) / sd
    vega = A * np.sqrt(T) * norm.pdf(d)
    N = notional
    return SwaptionRisk(float(N * pv), float(N * dlt), float(-N * dlt * BP),
                        float(N * gamma * BP * BP), float(N * vega * BP))


# ---------------------------------------------------------------------------
# Bond futures (simplified)
# ---------------------------------------------------------------------------
def conversion_factor(coupon: float, maturity: float, notional_coupon: float = 0.06,
                      freq: int = 2) -> float:
    """CF = price of the bond at the notional yield / 100."""
    return bond_price(notional_coupon, coupon, maturity, freq) / 100


def ctd_analysis(basket: list[tuple[float, float]], y: float, futures_price: Optional[float] = None,
                 notional_coupon: float = 0.06) -> list[dict]:
    """Cheapest-to-deliver illustration with a flat yield ``y`` for every bond.

    For each bond (coupon, maturity): price, CF, price/CF and gross basis
    (P - F*CF). If ``futures_price`` is None it is set to min(P/CF), the
    zero-carry fair value, so the CTD has zero basis.
    """
    rows = []
    for c, m in basket:
        P = bond_price(y, c, m)
        cf = conversion_factor(c, m, notional_coupon)
        rows.append({"coupon": c, "maturity": m, "price": P, "cf": cf, "p_over_cf": P / cf,
                     "mod_dur": bond_risk(y, c, m).modified})
    F = futures_price if futures_price is not None else min(r["p_over_cf"] for r in rows)
    for r in rows:
        r["gross_basis"] = r["price"] - F * r["cf"]
    best = min(rows, key=lambda r: r["gross_basis"])
    for r in rows:
        r["ctd"] = r is best
    return rows


# ---------------------------------------------------------------------------
# Carry, roll-down, central-bank pricing
# ---------------------------------------------------------------------------
def receiver_carry_rolldown(curve: ZeroCurve, tenor: float, horizon: float = 0.25,
                            funding_tenor: float = 0.25, freq: int = 1) -> dict[str, float]:
    """Carry and roll-down (in bp of rate over the horizon) for receiving a spot-starting
    swap of ``tenor`` years, on an unchanged curve.

    carry   = (fixed rate - short floating rate) * horizon
    rolldown= (par rate of tenor - par rate of (tenor - horizon)) : the swap 'rolls'
              to a shorter, lower-yielding point if the curve is upward sloping.
    Breakeven = (carry + roll) in bp: how far the rate can rise before you lose.
    """
    S = par_swap_rate(curve, 0.0, tenor, freq)
    fl = curve.fwd(0.0, funding_tenor)
    carry_bp = (S - fl) / BP * horizon
    S_short = par_swap_rate(curve, 0.0, tenor - horizon, freq) if tenor - horizon >= 1 / freq else S
    roll_bp = (S - S_short) / BP
    return {"par_rate": S, "float_rate": fl, "carry_bp": carry_bp, "roll_bp": roll_bp,
            "total_bp": carry_bp + roll_bp,
            "breakeven_bp_over_horizon": carry_bp + roll_bp}


def implied_move_probability(priced_change_bp: float, step_bp: float = 25.0) -> dict[str, float]:
    """Implied probability of a full step at a meeting from OIS pricing.

    Assuming only 'no change' or 'one step' are possible:
    p = |priced| / step. If |priced| > step, the extra is the probability of a
    second step on top of a certain first step.
    """
    a = abs(priced_change_bp)
    k = int(a // step_bp)
    rem = a - k * step_bp
    return {"full_steps_certain": k, "prob_next_step": rem / step_bp,
            "direction": "cut" if priced_change_bp < 0 else "hike"}


def dv01_hedge_ratio(dv01_a: float, dv01_b: float) -> float:
    """Notional of leg B per 1 notional of leg A that makes the pair DV01-neutral."""
    return dv01_a / dv01_b
