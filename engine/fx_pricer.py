"""Garman-Kohlhagen pricer for European FX options.

Conventions
-----------
* ``S`` is spot quoted as units of QUOTE (domestic) currency per 1 unit of BASE
  (foreign) currency, e.g. EURUSD = 1.16 USD per EUR.
* ``rd`` is the domestic (quote ccy) rate, ``rf`` the foreign (base ccy) rate,
  both continuously compounded decimals.
* ``vol`` is a decimal (0.10 = 10%). ``T`` is in years (ACT/365).
* Prices are in quote currency per 1 unit of base notional.
* Greeks returned by :func:`greeks` are RAW mathematical derivatives per unit of
  base notional (vega per 1.00 of vol, theta per year). Desk units (per vol
  point, per day, per 1%) are produced by :mod:`engine.structures`.

The pricer sits behind the :class:`Pricer` protocol so another implementation
can be swapped in and compared with :func:`compare_pricers`.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Union, runtime_checkable

import numpy as np
from scipy.optimize import brentq
from scipy.special import ndtr, ndtri

ArrayLike = Union[float, np.ndarray]

_SQRT2PI = np.sqrt(2.0 * np.pi)
_N = ndtr      # standard normal CDF (fast ufunc)
_Ninv = ndtri  # inverse CDF


def _n(x):
    """Standard normal PDF."""
    return np.exp(-0.5 * x * x) / _SQRT2PI


def cp_sign(call_put: Union[str, int, float]) -> int:
    """Map 'C'/'call'/+1 to +1 and 'P'/'put'/-1 to -1."""
    if isinstance(call_put, str):
        c = call_put.strip().lower()
        if c in ("c", "call"):
            return 1
        if c in ("p", "put"):
            return -1
        raise ValueError(f"call_put must be call or put, got {call_put!r}")
    v = int(np.sign(call_put))
    if v not in (1, -1):
        raise ValueError(f"call_put must be +1 or -1, got {call_put!r}")
    return v


def forward(S: ArrayLike, T: ArrayLike, rd: ArrayLike, rf: ArrayLike) -> ArrayLike:
    """Outright forward from covered interest parity: F = S exp((rd - rf) T)."""
    return S * np.exp((rd - rf) * T)


def d1_d2(S: ArrayLike, K: ArrayLike, T: ArrayLike, rd: ArrayLike, rf: ArrayLike,
          vol: ArrayLike) -> tuple[ArrayLike, ArrayLike]:
    """Black-Scholes d1 and d2 for FX."""
    sqT = np.sqrt(T)
    d1 = (np.log(S / K) + (rd - rf + 0.5 * vol * vol) * T) / (vol * sqT)
    return d1, d1 - vol * sqT


def price(S: ArrayLike, K: ArrayLike, T: ArrayLike, rd: ArrayLike, rf: ArrayLike,
          vol: ArrayLike, call_put: Union[str, int]) -> ArrayLike:
    """Garman-Kohlhagen price (quote ccy per unit base notional).

    At ``T <= 0`` returns intrinsic value.
    """
    phi = cp_sign(call_put)
    T_arr = np.asarray(T, dtype=float)
    if np.all(T_arr <= 0):
        return np.maximum(phi * (np.asarray(S) - np.asarray(K)), 0.0)
    d1, d2 = d1_d2(S, K, T, rd, rf, vol)
    dff = np.exp(-rf * T)
    dfd = np.exp(-rd * T)
    return phi * (S * dff * _N(phi * d1) - K * dfd * _N(phi * d2))


@dataclass(frozen=True)
class Greeks:
    """Raw Greeks per unit of base notional.

    delta: dV/dS (spot delta, unadjusted)
    delta_fwd: forward delta  phi N(phi d1)
    delta_pa: premium-adjusted spot delta = delta - V/S
    gamma: d2V/dS2
    vega: dV/dvol (per 1.00 vol)
    theta: dV/dt with calendar time passing (per year), = -dV/dT
    rho_d, rho_f: dV/drd, dV/drf (per 1.00 rate)
    vanna: d2V/dS dvol
    volga: d2V/dvol2
    charm: d(delta)/dt with calendar time passing (per year)
    """

    price: float
    delta: float
    delta_fwd: float
    delta_pa: float
    gamma: float
    vega: float
    theta: float
    rho_d: float
    rho_f: float
    vanna: float
    volga: float
    charm: float


def greeks(S: float, K: float, T: float, rd: float, rf: float, vol: float,
           call_put: Union[str, int]) -> Greeks:
    """Analytic Garman-Kohlhagen Greeks (see :class:`Greeks` for definitions)."""
    phi = cp_sign(call_put)
    if T <= 0:
        itm = phi * (S - K) > 0
        v = max(phi * (S - K), 0.0)
        d = float(phi) if itm else 0.0
        return Greeks(v, d, d, d - v / S, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    sqT = np.sqrt(T)
    d1, d2 = d1_d2(S, K, T, rd, rf, vol)
    dff, dfd = np.exp(-rf * T), np.exp(-rd * T)
    Nd1, Nd2 = _N(phi * d1), _N(phi * d2)
    nd1 = _n(d1)
    pv = phi * (S * dff * Nd1 - K * dfd * Nd2)
    delta = phi * dff * Nd1
    gamma = dff * nd1 / (S * vol * sqT)
    vega = S * dff * nd1 * sqT
    theta = (-S * dff * nd1 * vol / (2 * sqT)
             + phi * (rf * S * dff * Nd1 - rd * K * dfd * Nd2))
    rho_d = phi * K * T * dfd * Nd2
    rho_f = -phi * S * T * dff * Nd1
    vanna = -dff * nd1 * d2 / vol
    volga = vega * d1 * d2 / vol
    dd1_dT = (2 * (rd - rf) * T - d2 * vol * sqT) / (2 * T * vol * sqT)
    ddelta_dT = -rf * delta + dff * nd1 * dd1_dT
    charm = -ddelta_dT
    return Greeks(float(pv), float(delta), float(phi * Nd1), float(delta - pv / S),
                  float(gamma), float(vega), float(theta), float(rho_d), float(rho_f),
                  float(vanna), float(volga), float(charm))


# ---------------------------------------------------------------------------
# Implied volatility
# ---------------------------------------------------------------------------
class ImpliedVolError(ValueError):
    """Raised when a price is outside no-arbitrage bounds."""


def price_bounds(S: float, K: float, T: float, rd: float, rf: float,
                 call_put: Union[str, int]) -> tuple[float, float]:
    """No-arbitrage lower and upper bounds for a European FX option."""
    phi = cp_sign(call_put)
    fwd_intr = phi * (S * np.exp(-rf * T) - K * np.exp(-rd * T))
    lower = max(fwd_intr, 0.0)
    upper = S * np.exp(-rf * T) if phi == 1 else K * np.exp(-rd * T)
    return lower, upper


def implied_vol(target: float, S: float, K: float, T: float, rd: float, rf: float,
                call_put: Union[str, int], tol: float = 1e-10,
                vol_lo: float = 1e-5, vol_hi: float = 5.0) -> float:
    """Implied vol from a GK price.

    Strategy: convert to the OTM option via put-call parity (better conditioned
    for deep ITM), try Newton-Raphson on vega from a Brenner-Subrahmanyam style
    seed, and fall back to Brent bisection on ``[vol_lo, vol_hi]`` if Newton
    leaves the bracket, stalls, or vega is tiny (deep OTM / short expiry).
    """
    if T <= 0:
        raise ImpliedVolError("No implied vol at or after expiry")
    phi = cp_sign(call_put)
    lo_b, hi_b = price_bounds(S, K, T, rd, rf, phi)
    if target < lo_b - 1e-12 or target > hi_b + 1e-12:
        raise ImpliedVolError(f"Price {target} outside bounds [{lo_b}, {hi_b}]")
    F = forward(S, T, rd, rf)
    # switch to the OTM side via parity: C - P = S e^{-rfT} - K e^{-rdT}
    otm_phi = 1 if K >= F else -1
    if otm_phi != phi:
        target = target - phi * (S * np.exp(-rf * T) - K * np.exp(-rd * T))
        phi = otm_phi
    target = max(target, 0.0)
    if target <= 1e-14 * S:
        return vol_lo

    def f(v: float) -> float:
        return float(price(S, K, T, rd, rf, v, phi)) - target

    # Newton
    v = np.sqrt(2 * abs(np.log(F / K)) / T) if K != F else 0.0
    v = max(v, target / (0.4 * S * np.exp(-rf * T) * np.sqrt(T)) if K == F else v)
    v = min(max(v, 0.05), 2.0)
    for _ in range(60):
        diff = f(v)
        if diff == 0.0:
            return float(v)
        vg = greeks(S, K, T, rd, rf, v, phi).vega
        if vg < 1e-12 * S:
            break
        v_new = v - diff / vg
        if not (vol_lo < v_new < vol_hi):
            break
        if abs(v_new - v) < 1e-13 * max(v, 1e-3):
            return float(v_new)
        v = v_new
    # Brent fallback
    flo, fhi = f(vol_lo), f(vol_hi)
    if flo > 0:
        return vol_lo
    if fhi < 0:
        raise ImpliedVolError("Price above model maximum within vol_hi")
    return float(brentq(f, vol_lo, vol_hi, xtol=1e-14, rtol=1e-14, maxiter=500))


# ---------------------------------------------------------------------------
# Pricer interface
# ---------------------------------------------------------------------------
@runtime_checkable
class Pricer(Protocol):
    """Anything with a GK-compatible ``price`` method can plug into the app."""

    def price(self, S: float, K: float, T: float, rd: float, rf: float, vol: float,
              call_put: str) -> float: ...


class GKPricer:
    """Reference Garman-Kohlhagen implementation of :class:`Pricer`."""

    def price(self, S: float, K: float, T: float, rd: float, rf: float, vol: float,
              call_put: str) -> float:
        return float(price(S, K, T, rd, rf, vol, call_put))

    def greeks(self, S: float, K: float, T: float, rd: float, rf: float, vol: float,
               call_put: str) -> Greeks:
        return greeks(S, K, T, rd, rf, vol, call_put)

    def implied_vol(self, target: float, S: float, K: float, T: float, rd: float,
                    rf: float, call_put: str) -> float:
        return implied_vol(target, S, K, T, rd, rf, call_put)


def compare_pricers(mine: Pricer, ref: Pricer | None = None, S: float = 1.10,
                    rd: float = 0.04, rf: float = 0.02,
                    strikes_pct: tuple[float, ...] = (0.8, 0.9, 0.95, 1.0, 1.05, 1.1, 1.2),
                    tenors: tuple[float, ...] = (7 / 365, 1 / 12, 0.25, 0.5, 1.0),
                    vols: tuple[float, ...] = (0.05, 0.10, 0.25)):
    """Grid comparison of two pricers. Returns a pandas DataFrame of differences."""
    import pandas as pd

    ref = ref or GKPricer()
    rows = []
    for T in tenors:
        for kp in strikes_pct:
            for v in vols:
                for cp in ("C", "P"):
                    K = S * kp
                    a = mine.price(S, K, T, rd, rf, v, cp)
                    b = ref.price(S, K, T, rd, rf, v, cp)
                    rows.append(dict(T=T, K=K, vol=v, cp=cp, mine=a, ref=b,
                                     diff=a - b, diff_pips=(a - b) / 1e-4))
    return pd.DataFrame(rows)
