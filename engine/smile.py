"""Per-tenor FX smile: market quotes -> pillar strikes/vols -> SABR fit.

Quote conventions
-----------------
* ATM: delta-neutral straddle vol.
* RR(x) = vol(x-delta call) - vol(x-delta put)
* BF(x): SMILE STRANGLE definition, so the pillar vols are explicit:
      vol_xC = ATM + BF + RR/2      vol_xP = ATM + BF - RR/2
  (Real broker quotes use the market/broker strangle; see README.)

Pillar strikes are found from the pillar vols with the pair's delta convention.
SABR (Hagan 2002 lognormal expansion, beta fixed) is then fitted: alpha is
solved so the ATM vol is matched exactly, and (rho, nu) are least-squares fitted
to the four wing pillars. If the max wing error exceeds the tolerance the smile
falls back to first-order vanna-volga (Castagna-Mercurio) through 25P/ATM/25C,
with a linear-in-log-strike wing extension anchored on the 10d pillars.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from scipy.optimize import brentq, least_squares

from engine.fx_conventions import atm_dns_strike, delta, strike_from_delta
from engine.fx_pricer import forward


@dataclass(frozen=True)
class SmileQuotes:
    """Market quotes for one tenor, all as decimals (0.071 = 7.1 vol)."""

    atm: float
    rr25: float
    bf25: float
    rr10: float
    bf10: float

    def pillar_vols(self) -> dict[str, float]:
        """Vols at the five pillars using the smile-strangle convention."""
        return {
            "10P": self.atm + self.bf10 - 0.5 * self.rr10,
            "25P": self.atm + self.bf25 - 0.5 * self.rr25,
            "ATM": self.atm,
            "25C": self.atm + self.bf25 + 0.5 * self.rr25,
            "10C": self.atm + self.bf10 + 0.5 * self.rr10,
        }


PILLAR_DELTAS = {"10P": -0.10, "25P": -0.25, "25C": 0.25, "10C": 0.10}


# ---------------------------------------------------------------------------
# SABR
# ---------------------------------------------------------------------------
def sabr_vol(K: np.ndarray | float, F: float, T: float, alpha: float, beta: float,
             rho: float, nu: float) -> np.ndarray | float:
    """Hagan et al. (2002) lognormal implied vol approximation."""
    K = np.asarray(K, dtype=float)
    one_b = 1.0 - beta
    fk = F * K
    fk_b = fk ** (0.5 * one_b)
    logfk = np.log(F / K)
    z = (nu / alpha) * fk_b * logfk
    with np.errstate(divide="ignore", invalid="ignore"):
        xz = np.log((np.sqrt(1 - 2 * rho * z + z * z) + z - rho) / (1 - rho))
        zx = np.where(np.abs(z) < 1e-7, 1.0 - 0.5 * rho * z, z / xz)
    denom = fk_b * (1 + one_b ** 2 / 24 * logfk ** 2 + one_b ** 4 / 1920 * logfk ** 4)
    corr = 1 + (one_b ** 2 / 24 * alpha ** 2 / fk ** one_b
                + 0.25 * rho * beta * nu * alpha / fk_b
                + (2 - 3 * rho * rho) / 24 * nu * nu) * T
    out = alpha / denom * zx * corr
    return out if out.ndim else float(out)


def _alpha_for_atm(K_atm: float, F: float, T: float, vol_atm: float, beta: float,
                   rho: float, nu: float) -> float:
    """Solve alpha so that sabr_vol(K_atm) == vol_atm."""
    f = lambda a: sabr_vol(K_atm, F, T, a, beta, rho, nu) - vol_atm
    guess = vol_atm * F ** (1 - beta)
    lo, hi = guess * 0.2, guess * 5.0
    try:
        return float(brentq(f, lo, hi, xtol=1e-14))
    except ValueError:
        return guess


@dataclass
class TenorSmile:
    """Calibrated smile for one expiry."""

    T: float
    S: float
    rd: float
    rf: float
    quotes: SmileQuotes
    convention: str
    premium_adjusted: bool
    beta: float = 1.0
    tol: float = 0.0015
    model: str = field(init=False, default="sabr")
    params: dict = field(init=False, default_factory=dict)
    pillar_strikes: dict = field(init=False, default_factory=dict)
    pillar_vols: dict = field(init=False, default_factory=dict)
    fit_errors: dict = field(init=False, default_factory=dict)
    warm_start: Optional[tuple[float, float]] = None

    def __post_init__(self) -> None:
        self.F = float(forward(self.S, self.T, self.rd, self.rf))
        self.pillar_vols = self.quotes.pillar_vols()
        self.pillar_strikes = {"ATM": atm_dns_strike(self.F, self.T, self.quotes.atm,
                                                     self.premium_adjusted)}
        for name, d in PILLAR_DELTAS.items():
            self.pillar_strikes[name] = strike_from_delta(
                d, self.S, self.T, self.rd, self.rf, self.pillar_vols[name],
                "C" if d > 0 else "P", self.convention)
        self._calibrate()

    # -- calibration --------------------------------------------------------
    def _calibrate(self) -> None:
        names = ["10P", "25P", "25C", "10C"]
        Ks = np.array([self.pillar_strikes[n] for n in names])
        vs = np.array([self.pillar_vols[n] for n in names])
        Ka, va, F, T, b = self.pillar_strikes["ATM"], self.quotes.atm, self.F, self.T, self.beta

        def resid(x: np.ndarray) -> np.ndarray:
            rho, nu = np.tanh(x[0]), np.exp(x[1])
            a = _alpha_for_atm(Ka, F, T, va, b, rho, nu)
            return (sabr_vol(Ks, F, T, a, b, rho, nu) - vs) * 1e4

        starts = []
        if self.warm_start is not None:
            r0, n0 = self.warm_start
            starts.append(np.array([np.arctanh(np.clip(r0, -0.995, 0.995)), np.log(max(n0, 1e-3))]))
        skew = self.quotes.rr25 / max(self.quotes.atm, 1e-6)
        nu0 = max(np.sqrt(max(self.quotes.bf25, 1e-5) / max(va, 1e-4) * 48 / max(T, 1e-3) / 3), 0.3)
        starts += [np.array([np.arctanh(np.clip(skew * 3, -0.9, 0.9)), np.log(min(nu0, 8.0))]),
                   np.array([0.0, np.log(1.0)]), np.array([np.sign(skew) * 0.5, np.log(3.0)])]
        best = None
        for x0 in starts:
            try:
                r = least_squares(resid, x0, method="lm", xtol=1e-12, ftol=1e-12, max_nfev=400)
            except Exception:  # pragma: no cover - defensive
                continue
            if best is None or r.cost < best.cost:
                best = r
            if np.max(np.abs(r.fun)) < 0.5:  # < 0.05 vol pts: good enough
                break
        ok = False
        if best is not None:
            rho, nu = float(np.tanh(best.x[0])), float(np.exp(best.x[1]))
            alpha = _alpha_for_atm(Ka, F, T, va, b, rho, nu)
            self.params = {"alpha": alpha, "beta": b, "rho": rho, "nu": nu}
            errs = self._errors(lambda K: sabr_vol(K, F, T, alpha, b, rho, nu))
            ok = max(abs(e) for e in errs.values()) <= self.tol and np.isfinite(alpha)
        if ok:
            self.model = "sabr"
            self.fit_errors = errs
        else:
            self.model = "vanna_volga"
            self.params = {}
            self.fit_errors = self._errors(self._vv_vol)

    def _errors(self, fn) -> dict[str, float]:
        return {n: float(fn(self.pillar_strikes[n]) - self.pillar_vols[n])
                for n in self.pillar_strikes}

    # -- vanna-volga fallback ---------------------------------------------
    def _vv_vol(self, K):
        K = np.asarray(K, dtype=float)
        K1, K2, K3 = (self.pillar_strikes[n] for n in ("25P", "ATM", "25C"))
        s1, s2, s3 = (self.pillar_vols[n] for n in ("25P", "ATM", "25C"))
        lK = np.log(K)
        l1, l2, l3 = np.log(K1), np.log(K2), np.log(K3)
        y1 = (l2 - lK) * (l3 - lK) / ((l2 - l1) * (l3 - l1))
        y2 = (lK - l1) * (l3 - lK) / ((l2 - l1) * (l3 - l2))
        y3 = (lK - l1) * (lK - l2) / ((l3 - l1) * (l3 - l2))
        inner = y1 * s1 + y2 * s2 + y3 * s3
        # beyond the 25d pillars: linear in log-strike through the 10d pillars
        k10p, k10c = self.pillar_strikes["10P"], self.pillar_strikes["10C"]
        v10p, v10c = self.pillar_vols["10P"], self.pillar_vols["10C"]
        left = s1 + (v10p - s1) * (lK - l1) / (np.log(k10p) - l1)
        right = s3 + (v10c - s3) * (lK - l3) / (np.log(k10c) - l3)
        out = np.where(K < K1, left, np.where(K > K3, right, inner))
        out = np.maximum(out, 0.25 * self.quotes.atm)
        return out if out.ndim else float(out)

    # -- public -------------------------------------------------------------
    def vol(self, K):
        """Implied vol at strike(s) ``K``."""
        if self.model == "sabr":
            p = self.params
            return sabr_vol(K, self.F, self.T, p["alpha"], p["beta"], p["rho"], p["nu"])
        return self._vv_vol(K)

    def strike_for_delta(self, target_delta: float, convention: Optional[str] = None,
                         iters: int = 60) -> float:
        """Strike for a signed delta using smile-consistent vol (fixed point)."""
        conv = convention or self.convention
        cp = "C" if target_delta > 0 else "P"
        v = self.quotes.atm
        K = self.pillar_strikes["ATM"]
        for _ in range(iters):
            K_new = strike_from_delta(target_delta, self.S, self.T, self.rd, self.rf, v, cp, conv)
            v_new = float(self.vol(K_new))
            if abs(K_new - K) < 1e-12 * K and abs(v_new - v) < 1e-12:
                return K_new
            K, v = K_new, v_new
        return K

    def implied_quotes(self) -> SmileQuotes:
        """Re-derive ATM/RR/BF quotes from the fitted smile (consistency check)."""
        vols = {n: float(self.vol(self.pillar_strikes[n])) for n in self.pillar_strikes}
        return SmileQuotes(
            atm=vols["ATM"], rr25=vols["25C"] - vols["25P"],
            bf25=0.5 * (vols["25C"] + vols["25P"]) - vols["ATM"],
            rr10=vols["10C"] - vols["10P"],
            bf10=0.5 * (vols["10C"] + vols["10P"]) - vols["ATM"])

    def delta_at(self, K: float, cp: str, convention: Optional[str] = None) -> float:
        """Market-convention delta at strike K using the smile vol."""
        return delta(self.S, K, self.T, self.rd, self.rf, float(self.vol(K)), cp,
                     convention or self.convention)
