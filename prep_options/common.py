"""Shared helpers for the options interview-prep generators."""
from __future__ import annotations

from functools import lru_cache


import numpy as np

from engine.config import load_config
from engine.fx_conventions import TENORS, get_pair
from engine.market_data import build_market
from engine.structures import SingleMarket, Structure, equity_market, market_from_surface

FX_WEIGHTS = {"EURUSD": 3, "USDJPY": 3, "GBPUSD": 2, "AUDUSD": 2, "USDCHF": 1, "USDCAD": 1,
              "NZDUSD": 1, "EURJPY": 1, "EURGBP": 1, "EURCHF": 1}

GREEK_LABEL = {
    "delta": "Delta", "delta_pa": "Delta (premium-adjusted)", "gamma_1pct": "Gamma", "theta": "Theta", "vega": "Vega",
    "vanna": "Vanna", "volga": "Volga", "charm": "Charm",
}
GREEK_UNITS = {
    "delta": "base notional", "delta_pa": "base notional, premium-adjusted", "gamma_1pct": "delta change per 1% spot",
    "theta": "P&L per day", "vega": "P&L per vol pt", "vanna": "delta change per vol pt",
    "volga": "vega change per vol pt", "charm": "delta change per day",
}


@lru_cache(maxsize=1)
def static_market():
    return build_market()


def fx_market(pair: str) -> SingleMarket:
    """SingleMarket on the calibrated default surface for ``pair``."""
    return market_from_surface(static_market().surface(pair))


def spx_market() -> SingleMarket:
    e = load_config()["equity_index"]
    return equity_market(e["spot"], e["rate"] / 100, e["div_yield"] / 100, e["atm_vol"] / 100,
                         e["skew_per_10pct"], e["name"])


def pick_pair(rng: np.random.Generator) -> str:
    names = list(FX_WEIGHTS)
    w = np.array([FX_WEIGHTS[n] for n in names], dtype=float)
    return str(rng.choice(names, p=w / w.sum()))


def notional_text(mkt: SingleMarket, N: float) -> str:
    if mkt.pair is None:
        return f"{N:,.0f} units of {mkt.name}"
    return f"{mkt.pair.base} {N / 1e6:,.0f}m"


def ccy(mkt: SingleMarket) -> str:
    return mkt.pair.quote if mkt.pair else "USD"


def fmt_num(x: float, digits: int = 0) -> str:
    """Compact signed number: 1,234,567 -> +1.23m, 12,345 -> +12.3k."""
    a = abs(x)
    sgn = "-" if x < 0 else "+"
    if a >= 1e9:
        return f"{sgn}{a / 1e9:.2f}bn"
    if a >= 1e6:
        return f"{sgn}{a / 1e6:.2f}m"
    if a >= 1e3:
        return f"{sgn}{a / 1e3:.1f}k"
    if a >= 1:
        return f"{sgn}{a:.{digits}f}"
    return f"{sgn}{a:.3g}" if a > 0 else "0"


def fmt_greek(mkt: SingleMarket, key: str, v: float) -> str:
    if key in ("delta", "delta_pa", "gamma_1pct", "vanna", "charm"):
        unit = mkt.pair.base if mkt.pair else "units"
        return f"{fmt_num(v)} {unit}"
    return f"{fmt_num(v)} {ccy(mkt)}"


def sign_of(v: float, ref: float, tol: float = 0.10) -> str:
    """'+', '-' or '0' with |v| < tol * ref treated as flat."""
    if abs(v) < tol * abs(ref):
        return "0"
    return "+" if v > 0 else "-"


def spot_grid(mkt: SingleMarket, tau: float, n: int = 41, width_sd: float = 2.5) -> np.ndarray:
    sd = mkt.vol(mkt.forward(tau), tau) * np.sqrt(max(tau, 2 / 365))
    width = min(max(width_sd * sd, 0.01), 0.25)
    return mkt.spot * np.exp(np.linspace(-width, width, n))


def profile(struct: Structure, mkt: SingleMarket, key: str, spots: np.ndarray) -> list[float]:
    """Exposure ``key`` (or 'value') across spot levels, sticky strike."""
    out = []
    for s in spots:
        m = mkt.bump_spot((s / mkt.spot - 1) * 100)
        e = struct.exposure(m)
        out.append(getattr(e, key))
    return out


def direction_word(before: float, after: float, rel_tol: float = 0.03) -> str:
    """Change in SIZE: 'Increases', 'Decreases' or 'Unchanged'."""
    if abs(after - before) <= rel_tol * max(abs(before), abs(after), 1e-300):
        return "Unchanged"
    return "Increases" if abs(after) > abs(before) else "Decreases"


def describe_position_change(name: str, before: float, after: float, fmt) -> str:
    """'short gamma: -1.2m -> -0.9m (less short)'."""
    def side(v: float) -> str:
        return "long" if v > 0 else "short" if v < 0 else "flat"
    b, a = side(before), side(after)
    if b == a and b != "flat":
        more = abs(after) > abs(before)
        if abs(after - before) <= 0.03 * max(abs(before), abs(after)):
            how = "roughly unchanged"
        else:
            how = f"{'more' if more else 'less'} {b}"
        return f"{b} {name}: {fmt(before)} to {fmt(after)} ({how})"
    return f"{name} flips from {b} ({fmt(before)}) to {a} ({fmt(after)})"


def tenor_text(t: str) -> str:
    return {"ON": "overnight", "1W": "1-week", "2W": "2-week", "1M": "1-month", "2M": "2-month",
            "3M": "3-month", "6M": "6-month", "9M": "9-month", "1Y": "1-year"}[t]


__all__ = ["TENORS", "get_pair", "static_market", "fx_market", "spx_market", "pick_pair"]
