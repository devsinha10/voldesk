"""Builds a consistent static market (spots, rate curves, surfaces) from config,
with an optional live spot snapshot from frankfurter.app (ECB reference rates).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from engine.config import load_config
from engine.fx_conventions import PAIRS, TENOR_LIST, TENORS, USD_PAIRS, all_spots, get_pair
from engine.smile import SmileQuotes
from engine.surface import RateCurve, VolSurface


def rate_curves(cfg: Optional[dict] = None) -> dict[str, RateCurve]:
    """Per-currency rate curves (decimals) from config."""
    cfg = cfg or load_config()
    out = {}
    overrides = cfg.get("rate_curves") or {}
    for ccy, r in cfg["rates"].items():
        pts = None
        if ccy in overrides:
            pts = {TENORS[t]: v / 100 for t, v in overrides[ccy].items()}
        out[ccy] = RateCurve(r / 100, pts)
    return out


def default_quotes(pair: str, cfg: Optional[dict] = None) -> dict[str, SmileQuotes]:
    """Smile quotes per tenor for a pair from config (decimals)."""
    cfg = cfg or load_config()
    sd = cfg["smile_defaults"]
    v = cfg["vols"][pair]
    out = {}
    for i, t in enumerate(cfg["tenors"]):
        atm, rr25, bf25 = v["atm"][i], v["rr25"][i], v["bf25"][i]
        rr10 = v["rr10"][i] if "rr10" in v else rr25 * sd["rr10_mult"]
        bf10 = v["bf10"][i] if "bf10" in v else bf25 * sd["bf10_mult"]
        out[t] = SmileQuotes(atm / 100, rr25 / 100, bf25 / 100, rr10 / 100, bf10 / 100)
    return out


def fetch_live_usd_spots(cfg: Optional[dict] = None) -> Optional[dict[str, float]]:
    """Try the configured free API for USD-based rates. Returns None on failure."""
    cfg = cfg or load_config()
    lc = cfg.get("live_spot", {})
    if not lc.get("enabled", False):
        return None
    try:
        import requests

        r = requests.get(lc["url"], timeout=lc.get("timeout_s", 4))
        r.raise_for_status()
        return parse_frankfurter(r.json())
    except Exception:
        return None


def parse_frankfurter(payload: dict) -> Optional[dict[str, float]]:
    """Convert a frankfurter ``?from=USD`` payload into the 7 USD-pair spots."""
    rates = payload.get("rates", {})
    need = {"EUR", "JPY", "GBP", "AUD", "NZD", "CAD", "CHF"}
    if not need.issubset(rates):
        return None
    out = {}
    for name in USD_PAIRS:
        p = get_pair(name)
        if p.base == "USD":
            out[name] = float(rates[p.quote])
        else:
            out[name] = 1.0 / float(rates[p.base])
    return out


@dataclass
class StaticMarket:
    """Snapshot of spots, curves and surfaces."""

    spots: dict[str, float]
    curves: dict[str, RateCurve]
    quotes: dict[str, dict[str, SmileQuotes]]
    source: str = "config"
    surfaces: dict[str, VolSurface] = field(default_factory=dict)

    def rd(self, pair: str, T: float) -> float:
        return self.curves[get_pair(pair).quote](T)

    def rf(self, pair: str, T: float) -> float:
        return self.curves[get_pair(pair).base](T)

    def surface(self, pair: str) -> VolSurface:
        if pair not in self.surfaces:
            p = get_pair(pair)
            cfg = load_config()
            self.surfaces[pair] = VolSurface(
                p, self.spots[pair], self.curves[p.quote], self.curves[p.base],
                self.quotes[pair], beta=cfg["smile_defaults"]["sabr_beta"],
                tol=cfg["smile_defaults"]["sabr_tol_vol"] / 100)
        return self.surfaces[pair]


def build_market(use_live: bool = False, cfg: Optional[dict] = None) -> StaticMarket:
    """Static market from config (and optionally a live spot snapshot)."""
    cfg = cfg or load_config()
    usd = None
    source = "config"
    if use_live:
        usd = fetch_live_usd_spots(cfg)
        source = "frankfurter (ECB)" if usd else "config (live fetch failed)"
    usd = usd or dict(cfg["spot_fallback"])
    spots = all_spots(usd)
    quotes = {p: default_quotes(p, cfg) for p in PAIRS}
    return StaticMarket(spots, rate_curves(cfg), quotes, source)


__all__ = ["build_market", "StaticMarket", "default_quotes", "rate_curves",
           "fetch_live_usd_spots", "parse_frankfurter", "TENOR_LIST"]
