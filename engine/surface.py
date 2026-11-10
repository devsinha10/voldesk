"""Vol surface per pair: calibrated tenor smiles + interpolation in time.

Interpolation between pillar expiries is linear in TOTAL VARIANCE at fixed
log-forward moneyness k = ln(K / F(T)). This is arbitrage-free in time as long
as total variance is non-decreasing across pillars at each k (checked by
:meth:`VolSurface.check_arbitrage`). Before the first pillar the ON smile is
used at the same k; beyond the last pillar vol is held flat (in k).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

import numpy as np

from engine.fx_conventions import TENORS, FXPair, get_pair
from engine.fx_pricer import forward, price
from engine.smile import SmileQuotes, TenorSmile


class RateCurve:
    """Simple zero curve: flat rate or piecewise-linear zero rates by year fraction."""

    def __init__(self, flat: float, points: Optional[dict[float, float]] = None) -> None:
        self.flat = flat
        if points:
            ts = sorted(points)
            self._t = np.array(ts)
            self._r = np.array([points[t] for t in ts])
        else:
            self._t = None
            self._r = None

    def __call__(self, T: float) -> float:
        if self._t is None:
            return self.flat
        return float(np.interp(T, self._t, self._r))

    def shifted(self, bp: float) -> "RateCurve":
        """Parallel shift (in basis points)."""
        pts = None if self._t is None else {t: r + bp * 1e-4 for t, r in zip(self._t, self._r)}
        return RateCurve(self.flat + bp * 1e-4, pts)


@dataclass
class ArbReport:
    """Result of the arbitrage checks."""

    calendar_ok: bool
    butterfly_ok: bool
    calendar_violations: list
    butterfly_violations: list

    @property
    def ok(self) -> bool:
        return self.calendar_ok and self.butterfly_ok


class VolSurface:
    """Arbitrage-checked vol surface for one FX pair."""

    def __init__(self, pair: str | FXPair, spot: float, rd: RateCurve, rf: RateCurve,
                 quotes: dict[str, SmileQuotes], beta: float = 1.0, tol: float = 0.0015,
                 warm: Optional["VolSurface"] = None) -> None:
        self.pair = get_pair(pair) if isinstance(pair, str) else pair
        self.spot = float(spot)
        self.rd, self.rf = rd, rf
        self.quotes = dict(quotes)
        self.tenors = [t for t in TENORS if t in quotes]
        self.smiles: dict[str, TenorSmile] = {}
        for t in self.tenors:
            T = TENORS[t]
            ws = None
            if warm is not None and t in warm.smiles and warm.smiles[t].model == "sabr":
                p = warm.smiles[t].params
                ws = (p["rho"], p["nu"])
            self.smiles[t] = TenorSmile(T=T, S=self.spot, rd=rd(T), rf=rf(T), quotes=quotes[t],
                                        convention=self.pair.delta_convention(T),
                                        premium_adjusted=self.pair.premium_adjusted,
                                        beta=beta, tol=tol, warm_start=ws)
        self._T = np.array([TENORS[t] for t in self.tenors])

    # -- basics -----------------------------------------------------------
    def forward(self, T: float) -> float:
        return float(forward(self.spot, T, self.rd(T), self.rf(T)))

    def _smile_vol_at_k(self, i: int, k: np.ndarray) -> np.ndarray:
        sm = self.smiles[self.tenors[i]]
        return np.asarray(sm.vol(sm.F * np.exp(k)), dtype=float)

    def vol(self, K, T: float):
        """Implied vol for strike(s) ``K`` and expiry ``T`` (years)."""
        K = np.asarray(K, dtype=float)
        T = max(float(T), 1e-6)
        k = np.log(K / self.forward(T))
        Ts = self._T
        if T <= Ts[0]:
            out = self._smile_vol_at_k(0, k)
        elif T >= Ts[-1]:
            out = self._smile_vol_at_k(len(Ts) - 1, k)
        else:
            j = int(np.searchsorted(Ts, T))
            i = j - 1
            w_i = self._smile_vol_at_k(i, k) ** 2 * Ts[i]
            w_j = self._smile_vol_at_k(j, k) ** 2 * Ts[j]
            x = (T - Ts[i]) / (Ts[j] - Ts[i])
            out = np.sqrt(((1 - x) * w_i + x * w_j) / T)
        return out if out.ndim else float(out)

    def atm_vol(self, T: float) -> float:
        """ATM (DNS) vol at any expiry, interpolated in total variance."""
        Ts = self._T
        atms = np.array([self.quotes[t].atm for t in self.tenors])
        if T <= Ts[0]:
            return float(atms[0])
        if T >= Ts[-1]:
            return float(atms[-1])
        w = np.interp(T, Ts, atms ** 2 * Ts)
        return float(np.sqrt(w / T))

    def strike_for_delta(self, tenor: str, target_delta: float) -> float:
        """Strike of a signed-delta option at a pillar tenor (market convention)."""
        return self.smiles[tenor].strike_for_delta(target_delta)

    def atm_strike(self, tenor: str) -> float:
        return self.smiles[tenor].pillar_strikes["ATM"]

    # -- arbitrage checks ---------------------------------------------------
    def check_arbitrage(self, n_k: int = 41, k_std: float = 3.0) -> ArbReport:
        """Calendar (total variance increasing in T at fixed k) and butterfly
        (call price convex in strike, i.e. non-negative density) checks."""
        cal_v, bf_v = [], []
        Ts = self._T
        atm_long = self.quotes[self.tenors[-1]].atm
        kgrid = np.linspace(-k_std, k_std, n_k) * atm_long * np.sqrt(Ts[-1]) * 0.6
        prev = None
        for i, t in enumerate(self.tenors):
            w = self._smile_vol_at_k(i, kgrid) ** 2 * Ts[i]
            if prev is not None:
                bad = np.where(w < prev - 1e-10)[0]
                if bad.size:
                    cal_v.append((t, float(np.min(w - prev))))
            prev = w
        for i, t in enumerate(self.tenors):
            sm = self.smiles[t]
            sd = sm.quotes.atm * np.sqrt(sm.T)
            Ks = sm.F * np.exp(np.linspace(-3.5 * sd, 3.5 * sd, 121))
            vols = np.asarray(sm.vol(Ks))
            if np.any(~np.isfinite(vols)) or np.any(vols <= 0):
                bf_v.append((t, "non-positive vol"))
                continue
            C = price(sm.S, Ks, sm.T, sm.rd, sm.rf, vols, "C")
            d1 = np.diff(C) / np.diff(Ks)
            d2 = np.diff(d1) / (0.5 * (Ks[2:] - Ks[:-2]))
            tolr = 1e-9 * sm.S / (Ks[1] - Ks[0])
            if np.min(d2) < -tolr:
                bf_v.append((t, float(np.min(d2))))
        return ArbReport(not cal_v, not bf_v, cal_v, bf_v)

    def quotes_table(self):
        """DataFrame of the quoted grid in vol points."""
        import pandas as pd

        rows = []
        for t in self.tenors:
            q = self.quotes[t]
            rows.append({"Tenor": t, "ATM": q.atm * 100, "25RR": q.rr25 * 100,
                         "25BF": q.bf25 * 100, "10RR": q.rr10 * 100, "10BF": q.bf10 * 100,
                         "Model": self.smiles[t].model})
        return pd.DataFrame(rows).set_index("Tenor")
