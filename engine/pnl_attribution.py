"""Taylor-expansion P&L attribution for option books.

For each step the realised P&L of an option leg is split into::

    delta  = delta0 * dS
    gamma  = 0.5 * gamma0 * dS^2
    vega   = vega0 * dvol          (bucketed by the leg's tenor)
    theta  = theta0 * dt
    vanna  = vanna0 * dS * dvol
    volga  = 0.5 * volga0 * dvol^2
    rho    = rho_d0 * drd + rho_f0 * drf
    unexplained = actual - sum(above)

``dvol`` is the change in the leg's own implied vol, vol1(K, tau1) - vol0(K, tau0),
so roll-down along the smile and term structure lands in vega, not theta.

The simulator adds non-Greek terms (new-trade edge, hedge costs, carry) with
:func:`attach_trading_terms`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

import numpy as np

from engine.fx_pricer import greeks, price
from engine.structures import Leg, SingleMarket, bucket_for

GREEK_TERMS = ["delta", "gamma", "vega", "theta", "vanna", "volga", "rho"]


@dataclass
class Attribution:
    """P&L breakdown (in the underlying's quote currency unless converted)."""

    actual: float = 0.0
    terms: dict = field(default_factory=lambda: {k: 0.0 for k in GREEK_TERMS})
    vega_by_tenor: dict = field(default_factory=dict)
    trading: dict = field(default_factory=dict)

    @property
    def explained(self) -> float:
        return sum(self.terms.values()) + sum(self.trading.values())

    @property
    def unexplained(self) -> float:
        return self.actual - self.explained

    def scaled(self, k: float) -> "Attribution":
        return Attribution(self.actual * k, {a: b * k for a, b in self.terms.items()},
                           {a: b * k for a, b in self.vega_by_tenor.items()},
                           {a: b * k for a, b in self.trading.items()})

    def add(self, other: "Attribution") -> "Attribution":
        out = Attribution(self.actual + other.actual,
                          {k: self.terms.get(k, 0) + other.terms.get(k, 0) for k in GREEK_TERMS})
        for src in (self.vega_by_tenor, other.vega_by_tenor):
            for k, v in src.items():
                out.vega_by_tenor[k] = out.vega_by_tenor.get(k, 0) + v
        for src in (self.trading, other.trading):
            for k, v in src.items():
                out.trading[k] = out.trading.get(k, 0) + v
        return out

    def as_dict(self) -> dict[str, float]:
        d = dict(self.terms)
        d.update({f"vega_{k}": v for k, v in self.vega_by_tenor.items()})
        d.update(self.trading)
        d["unexplained"] = self.unexplained
        d["actual"] = self.actual
        return d


def attribute_legs(legs: Iterable[Leg], m0: SingleMarket, m1: SingleMarket) -> Attribution:
    """Attribute the P&L of ``legs`` moving from market ``m0`` to ``m1``."""
    out = Attribution()
    dS = m1.spot - m0.spot
    dt = m1.t - m0.t
    drd, drf = m1.rd - m0.rd, m1.rf - m0.rf
    for leg in legs:
        N = leg.notional
        if leg.kind == "spot":
            out.actual += N * dS
            out.terms["delta"] += N * dS
            continue
        tau0, tau1 = leg.expiry - m0.t, leg.expiry - m1.t
        if tau0 <= 0:
            continue
        v0 = m0.vol(leg.K, tau0)
        g = greeks(m0.spot, leg.K, tau0, m0.rd, m0.rf, v0, leg.cp)
        if tau1 > 0:
            v1 = m1.vol(leg.K, tau1)
            p1 = float(price(m1.spot, leg.K, tau1, m1.rd, m1.rf, v1, leg.cp))
        else:
            v1 = v0
            p1 = max((1 if leg.cp == "C" else -1) * (m1.spot - leg.K), 0.0)
        dv = v1 - v0
        out.actual += N * (p1 - g.price)
        out.terms["delta"] += N * g.delta * dS
        out.terms["gamma"] += N * 0.5 * g.gamma * dS * dS
        out.terms["vega"] += N * g.vega * dv
        out.terms["theta"] += N * g.theta * dt
        out.terms["vanna"] += N * g.vanna * dS * dv
        out.terms["volga"] += N * 0.5 * g.volga * dv * dv
        out.terms["rho"] += N * (g.rho_d * drd + g.rho_f * drf)
        b = bucket_for(tau0)
        out.vega_by_tenor[b] = out.vega_by_tenor.get(b, 0.0) + N * g.vega * dv
    return out


def attach_trading_terms(att: Attribution, edge: float = 0.0, hedge_cost: float = 0.0,
                         carry: float = 0.0) -> Attribution:
    """Add simulator trading terms (already in the same currency as ``att``).

    These are cash/day-one effects outside the Greek Taylor expansion, so they
    are added to both ``actual`` and the explained set.
    """
    att.trading["edge"] = att.trading.get("edge", 0.0) + edge
    att.trading["hedge_cost"] = att.trading.get("hedge_cost", 0.0) + hedge_cost
    att.trading["carry"] = att.trading.get("carry", 0.0) + carry
    att.actual += edge + hedge_cost + carry
    return att
