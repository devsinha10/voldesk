"""Rates instruments priced off a :class:`engine.rates.ZeroCurve`, so every
scenario (parallel, twist, key-rate) is a full revaluation.

Signs: notional > 0 means long the bond / long the option / receive fixed
(for swaps use ``direction``). DV01 > 0 means long duration.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache


import numpy as np

from engine.config import load_config
from engine.rates import BP, ZeroCurve, annuity, bachelier_swaption, par_swap_rate


@lru_cache(maxsize=4)
def base_curve(name: str = "SONIA") -> ZeroCurve:
    return ZeroCurve.from_pct(load_config()["rates_engine"]["curves"][name])


def move_curve(curve: ZeroCurve, moves_bp: dict[float, float]) -> ZeroCurve:
    """Shift zero rates by tenor-dependent amounts (bp), linear between given tenors,
    flat beyond. ``{0: 50}`` or ``{2: 50, 10: 50}`` = parallel +50bp."""
    ts = sorted(moves_bp)
    vals = [moves_bp[t] for t in ts]
    return ZeroCurve({t: z + float(np.interp(t, ts, vals)) * BP for t, z in zip(curve.t, curve.z)})


class Instrument:
    name: str = ""

    def pv(self, curve: ZeroCurve) -> float:  # pragma: no cover - interface
        raise NotImplementedError


@dataclass
class Bond(Instrument):
    coupon: float
    maturity: float
    notional: float  # face, signed
    freq: int = 2
    name: str = "bond"

    def pv(self, curve: ZeroCurve) -> float:
        n = int(round(self.maturity * self.freq))
        t = np.arange(1, n + 1) / self.freq
        cf = np.full(n, self.coupon / self.freq)
        cf[-1] += 1.0
        return float(self.notional * np.sum(cf * curve.df(t)))


@dataclass
class Swap(Instrument):
    start: float
    end: float
    fixed: float
    notional: float  # positive
    direction: str = "receive"
    freq: int = 1
    name: str = "swap"

    def pv(self, curve: ZeroCurve) -> float:
        A = annuity(curve, self.start, self.end, self.freq)
        S = par_swap_rate(curve, self.start, self.end, self.freq)
        sgn = 1 if self.direction == "receive" else -1
        return sgn * self.notional * (self.fixed - S) * A


@dataclass
class FRN(Instrument):
    notional: float
    next_reset: float
    coupon: float  # current fixed coupon until next reset
    name: str = "floating-rate note"

    def pv(self, curve: ZeroCurve) -> float:
        return float(self.notional * (1 + self.coupon * self.next_reset) * curve.df(self.next_reset))


@dataclass
class Swaption(Instrument):
    expiry: float
    tenor: float
    strike: float
    normal_vol: float
    kind: str  # 'payer' | 'receiver'
    notional: float  # signed: + long
    name: str = "swaption"

    def pv(self, curve: ZeroCurve) -> float:
        F = par_swap_rate(curve, self.expiry, self.expiry + self.tenor)
        A = annuity(curve, self.expiry, self.expiry + self.tenor)
        return bachelier_swaption(F, self.strike, self.expiry, self.normal_vol, A, self.kind,
                                  self.notional).price


@dataclass
class BondFuture(Instrument):
    """Long/short futures ~ CTD bond scaled by 1/CF, zero upfront value."""

    ctd: Bond
    cf: float
    curve0: ZeroCurve
    name: str = "bond future"

    def pv(self, curve: ZeroCurve) -> float:
        return (self.ctd.pv(curve) - self.ctd.pv(self.curve0)) / self.cf


@dataclass
class Composite(Instrument):
    parts: list
    name: str = "composite"

    def pv(self, curve: ZeroCurve) -> float:
        return float(sum(p.pv(curve) for p in self.parts))


def callable_bond(coupon: float, maturity: float, call_in: float, face: float, normal_vol: float,
                  curve: ZeroCurve) -> Composite:
    """Callable bond = bullet bond + SHORT receiver swaption (the issuer's right to
    refinance when rates fall). Long duration, SHORT convexity near the strike."""
    b = Bond(coupon, maturity, face, freq=1)
    opt = Swaption(call_in, maturity - call_in, coupon, normal_vol, "receiver", -face)
    return Composite([b, opt], name="callable bond")


@dataclass
class Risk:
    pv: float
    dv01: float           # + = long duration
    convexity_pnl: float  # P&L of a symmetric +/- 25bp move (sum of the two): + = long convexity
    dv01_up50: float      # DV01 after a +50bp parallel move
    dv01_dn50: float


def risk(inst: Instrument, curve: ZeroCurve, h_bp: float = 25.0) -> Risk:
    pv0 = inst.pv(curve)
    up, dn = inst.pv(curve.shifted(1)), inst.pv(curve.shifted(-1))
    dv01 = (dn - up) / 2
    cx = inst.pv(curve.shifted(h_bp)) + inst.pv(curve.shifted(-h_bp)) - 2 * pv0

    def dv(c):
        return (inst.pv(c.shifted(-1)) - inst.pv(c.shifted(1))) / 2
    return Risk(pv0, dv01, cx, dv(curve.shifted(50)), dv(curve.shifted(-50)))


def pnl(inst: Instrument, curve: ZeroCurve, moved: ZeroCurve) -> float:
    return inst.pv(moved) - inst.pv(curve)


def sign_word(x: float, ref: float, tol: float = 0.05) -> str:
    if abs(x) < tol * abs(ref):
        return "0"
    return "+" if x > 0 else "-"


def fmt_ccy(x: float, ccy: str = "GBP") -> str:
    a = abs(x)
    s = "-" if x < 0 else "+"
    if a >= 1e6:
        return f"{s}{ccy} {a/1e6:,.2f}m"
    if a >= 1e3:
        return f"{s}{ccy} {a/1e3:,.1f}k"
    return f"{s}{ccy} {a:,.0f}"
