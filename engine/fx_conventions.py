"""FX market conventions: pairs, pips, tenors, forwards, delta conventions,
ATM definition and strike-from-delta.

Delta conventions used (G10, tenors up to and including 1Y use SPOT delta):

* ``spot``     : phi e^{-rf T} N(phi d1)
* ``spot_pa``  : premium-adjusted spot delta = phi (K/F) e^{-rf T} N(phi d2)
* ``fwd``      : phi N(phi d1)                (used beyond 1Y)
* ``fwd_pa``   : phi (K/F) N(phi d2)          (used beyond 1Y)

Premium-adjusted delta is used when the premium is paid in the BASE currency,
which for G10 is the case for USD-based pairs (USDJPY, USDCHF, USDCAD) and for
the EUR crosses (EURJPY, EURGBP, EURCHF: premium in EUR).

ATM is the delta-neutral straddle (DNS):
* unadjusted delta: K_ATM = F exp(+0.5 vol^2 T)
* premium-adjusted: K_ATM = F exp(-0.5 vol^2 T)
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Union

import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm

from engine.fx_pricer import cp_sign, d1_d2, forward, price

_N, _n, _Ninv = norm.cdf, norm.pdf, norm.ppf

TENORS: dict[str, float] = {
    "ON": 1 / 365, "1W": 7 / 365, "2W": 14 / 365, "1M": 1 / 12, "2M": 2 / 12,
    "3M": 3 / 12, "6M": 6 / 12, "9M": 9 / 12, "1Y": 1.0,
}
TENOR_LIST = list(TENORS.keys())


@dataclass(frozen=True)
class FXPair:
    """A currency pair quoted as BASE/QUOTE (units of QUOTE per 1 BASE)."""

    name: str
    base: str
    quote: str
    pip: float
    premium_ccy: str

    @property
    def premium_adjusted(self) -> bool:
        """True when the premium is paid in the base currency."""
        return self.premium_ccy == self.base

    def delta_convention(self, T: float) -> str:
        """Market delta convention for an expiry ``T`` (years)."""
        pa = "_pa" if self.premium_adjusted else ""
        return ("spot" if T <= 1.0 + 1e-9 else "fwd") + pa

    def convention_label(self, T: float = 0.25) -> str:
        """Human-readable convention for on-screen display."""
        c = self.delta_convention(T)
        base = "Spot delta" if c.startswith("spot") else "Forward delta"
        if self.premium_adjusted:
            return f"{base}, premium-adjusted (premium in {self.base}); ATM = DNS"
        return f"{base}, unadjusted (premium in {self.quote}); ATM = DNS"

    @property
    def decimals(self) -> int:
        return 3 if self.pip == 0.01 else 5


def _pair(name: str, premium_ccy: str) -> FXPair:
    base, quote = name[:3], name[3:]
    pip = 0.01 if quote == "JPY" else 0.0001
    return FXPair(name, base, quote, pip, premium_ccy)


PAIRS: dict[str, FXPair] = {
    "EURUSD": _pair("EURUSD", "USD"),
    "USDJPY": _pair("USDJPY", "USD"),
    "GBPUSD": _pair("GBPUSD", "USD"),
    "AUDUSD": _pair("AUDUSD", "USD"),
    "NZDUSD": _pair("NZDUSD", "USD"),
    "USDCAD": _pair("USDCAD", "USD"),
    "USDCHF": _pair("USDCHF", "USD"),
    "EURJPY": _pair("EURJPY", "EUR"),
    "EURGBP": _pair("EURGBP", "EUR"),
    "EURCHF": _pair("EURCHF", "EUR"),
}
USD_PAIRS = ["EURUSD", "USDJPY", "GBPUSD", "AUDUSD", "NZDUSD", "USDCAD", "USDCHF"]
CROSSES = ["EURJPY", "EURGBP", "EURCHF"]
CURRENCIES = ["USD", "EUR", "JPY", "GBP", "AUD", "NZD", "CAD", "CHF"]


def get_pair(name: str) -> FXPair:
    """Look up a pair by name (case-insensitive)."""
    return PAIRS[name.upper().replace("/", "")]


# ---------------------------------------------------------------------------
# Spot construction (crosses consistent with USD legs)
# ---------------------------------------------------------------------------
def usd_values_from_usd_pairs(usd_spots: dict[str, float]) -> dict[str, float]:
    """USD value of one unit of each currency from the 7 USD pairs."""
    v = {"USD": 1.0}
    for name, s in usd_spots.items():
        p = get_pair(name)
        if p.quote == "USD":
            v[p.base] = s
        elif p.base == "USD":
            v[p.quote] = 1.0 / s
    return v


def spot_from_usd_values(pair: str, usd_value: dict[str, float]) -> float:
    """Spot of any pair from per-currency USD values: S = USD(base)/USD(quote)."""
    p = get_pair(pair)
    return usd_value[p.base] / usd_value[p.quote]


def all_spots(usd_spots: dict[str, float]) -> dict[str, float]:
    """All 10 pair spots from the 7 USD legs (crosses triangulated)."""
    v = usd_values_from_usd_pairs(usd_spots)
    return {name: spot_from_usd_values(name, v) for name in PAIRS}


def usd_per_quote(pair: str, spots: dict[str, float]) -> float:
    """USD value of 1 unit of the pair's QUOTE currency (for P&L conversion)."""
    q = get_pair(pair).quote
    if q == "USD":
        return 1.0
    for name in USD_PAIRS:
        p = get_pair(name)
        if p.base == "USD" and p.quote == q:
            return 1.0 / spots[name]
        if p.quote == "USD" and p.base == q:
            return spots[name]
    raise KeyError(q)


def usd_per_base(pair: str, spots: dict[str, float]) -> float:
    """USD value of 1 unit of the pair's BASE currency."""
    return spots[pair] * usd_per_quote(pair, spots)


# ---------------------------------------------------------------------------
# Forwards and premium display
# ---------------------------------------------------------------------------
def forward_points(S: float, T: float, rd: float, rf: float, pip: float) -> float:
    """Forward points in pips: (F - S) / pip."""
    return (forward(S, T, rd, rf) - S) / pip


def premium_pips(premium_quote_per_base: float, pip: float) -> float:
    """Premium in quote-currency pips per unit of base."""
    return premium_quote_per_base / pip


def premium_pct_base(premium_quote_per_base: float, S: float) -> float:
    """Premium as % of base notional (premium converted to base at spot)."""
    return 100.0 * premium_quote_per_base / S


# ---------------------------------------------------------------------------
# Deltas
# ---------------------------------------------------------------------------
def delta(S: float, K: float, T: float, rd: float, rf: float, vol: float,
          call_put: Union[str, int], convention: str = "spot") -> float:
    """Delta under a named convention (spot, spot_pa, fwd, fwd_pa)."""
    phi = cp_sign(call_put)
    d1, d2 = d1_d2(S, K, T, rd, rf, vol)
    F = forward(S, T, rd, rf)
    if convention == "spot":
        return float(phi * np.exp(-rf * T) * _N(phi * d1))
    if convention == "fwd":
        return float(phi * _N(phi * d1))
    if convention == "spot_pa":
        return float(phi * (K / F) * np.exp(-rf * T) * _N(phi * d2))
    if convention == "fwd_pa":
        return float(phi * (K / F) * _N(phi * d2))
    raise ValueError(f"Unknown delta convention {convention!r}")


def atm_dns_strike(F: float, T: float, vol: float, premium_adjusted: bool) -> float:
    """Delta-neutral straddle strike."""
    return float(F * np.exp((-0.5 if premium_adjusted else 0.5) * vol * vol * T))


def _scale(convention: str, rf: float, T: float) -> float:
    return np.exp(-rf * T) if convention.startswith("spot") else 1.0


def strike_from_delta(target_delta: float, S: float, T: float, rd: float, rf: float,
                      vol: float, call_put: Union[str, int],
                      convention: str = "spot") -> float:
    """Strike whose delta under ``convention`` equals ``target_delta``.

    ``target_delta`` is signed (0.25 for a 25d call, -0.25 for a 25d put).

    Unadjusted conventions have a closed form. Premium-adjusted deltas are solved
    numerically; for calls the PA delta is not monotonic in K (it rises from 0,
    peaks, then falls), so we bracket the root on the OTM branch between the
    strike of maximum delta and the unadjusted strike (an upper bound, since
    PA delta < unadjusted delta at every strike).
    """
    phi = cp_sign(call_put)
    if phi * target_delta <= 0:
        raise ValueError("Delta sign must match call/put")
    F = forward(S, T, rd, rf)
    sqT = np.sqrt(T)
    scale = _scale(convention, rf, T)
    a = phi * target_delta / scale
    if not (0 < a < 1):
        raise ValueError(f"Delta {target_delta} not attainable for {convention}")

    k_unadj = float(F * np.exp(-phi * _Ninv(a) * vol * sqT + 0.5 * vol * vol * T))
    if convention in ("spot", "fwd"):
        return k_unadj

    def f(K: float) -> float:
        return delta(S, K, T, rd, rf, vol, phi, convention) - target_delta

    if phi == 1:
        # strike of max PA call delta: d/dK [K N(d2)] = 0 -> vol sqT N(d2) = n(d2)
        g = lambda d2: vol * sqT * _N(d2) - _n(d2)
        d2_star = brentq(g, -12.0, 12.0)
        k_max = float(F * np.exp(-d2_star * vol * sqT - 0.5 * vol * vol * T))
        if f(k_max) < 0:
            raise ValueError(f"PA call delta {target_delta} exceeds max attainable")
        hi = max(k_unadj, k_max * 1.0001)
        while f(hi) > 0:
            hi *= 1.5
        return float(brentq(f, k_max, hi, xtol=1e-14 * F, maxiter=500))
    # puts: PA put delta is monotone in K; PA strike is below the unadjusted one
    hi = k_unadj
    lo = k_unadj * np.exp(-12 * vol * sqT)
    while f(lo) < 0:  # f(lo) should be > 0 (delta closer to 0)
        lo *= 0.5
    return float(brentq(f, lo, hi * 1.000001 if f(hi) < 0 else hi * 1.5,
                        xtol=1e-14 * F, maxiter=500))


def option_premium(S: float, K: float, T: float, rd: float, rf: float, vol: float,
                   call_put: Union[str, int], pip: float) -> dict[str, float]:
    """Premium in quote ccy per base, quote pips, and % of base notional."""
    p = float(price(S, K, T, rd, rf, vol, call_put))
    return {"premium": p, "pips": premium_pips(p, pip), "pct_base": premium_pct_base(p, S)}
