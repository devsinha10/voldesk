"""Trading book: positions, cash, valuation, exposures and expiry handling.

Accounting (per pair, in the pair's QUOTE currency):
    P&L = sum(position values at mid) + cash
* Buying an option at price p: cash -= N * p. Selling: N < 0, so cash rises.
* Spot hedges are stored as spot legs at the execution price, so the half
  spread shows up immediately as a small negative value (the hedge cost).
* Spot legs earn carry each tick: N * S * (r_base - r_quote) * dt.
* At expiry an ITM option becomes a spot position at its strike (physical
  delivery), so value is continuous and the delta 'appears' (pin risk).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from engine.fx_pricer import price
from engine.structures import Exposure, Leg, SingleMarket, Structure


@dataclass
class Position:
    id: int
    pair: str
    kind: str                 # 'option' | 'spot'
    notional: float           # signed base units
    K: float
    expiry: float = 0.0       # years since session start
    cp: str = "C"
    tenor: str = ""
    source: str = ""          # client | idb | spot_hedge | inherited | expiry
    trade_id: Optional[int] = None
    client_type: Optional[str] = None
    label: str = ""
    open_t: float = 0.0
    premium: float = 0.0      # quote ccy paid per unit at inception (for the blotter)

    def leg(self) -> Leg:
        return Leg(self.kind, self.notional, self.K, self.expiry, self.cp, self.label)


@dataclass
class Book:
    positions: list[Position] = field(default_factory=list)
    cash: dict = field(default_factory=dict)       # pair -> quote ccy
    next_id: int = 1
    trade_cash: dict = field(default_factory=dict)  # trade_id -> quote ccy cash at inception

    def add(self, pair: str, kind: str, notional: float, K: float, expiry: float = 0.0, cp: str = "C",
            price_per_unit: float = 0.0, **kw) -> Position:
        p = Position(self.next_id, pair, kind, notional, K, expiry, cp, premium=price_per_unit, **kw)
        self.next_id += 1
        self.positions.append(p)
        if kind == "option":
            c = -notional * price_per_unit
            self.cash[pair] = self.cash.get(pair, 0.0) + c
            if p.trade_id is not None:
                self.trade_cash[p.trade_id] = self.trade_cash.get(p.trade_id, 0.0) + c
        return p

    def pairs(self) -> list[str]:
        return sorted({p.pair for p in self.positions} | set(self.cash))

    def legs(self, pair: str) -> list[Leg]:
        return [p.leg() for p in self.positions if p.pair == pair]

    def structure(self, pair: str) -> Structure:
        return Structure(pair, tuple(self.legs(pair)))

    def value(self, pair: str, mkt: SingleMarket) -> float:
        return self.structure(pair).value(mkt)

    def pnl_quote(self, pair: str, mkt: SingleMarket) -> float:
        return self.value(pair, mkt) + self.cash.get(pair, 0.0)

    def exposure(self, pair: str, mkt: SingleMarket) -> Exposure:
        return self.structure(pair).exposure(mkt)

    def position_value(self, pos: Position, mkt: SingleMarket) -> float:
        if pos.kind == "spot":
            return pos.notional * (mkt.spot - pos.K)
        tau = pos.expiry - mkt.t
        if tau <= 0:
            return pos.notional * max((1 if pos.cp == "C" else -1) * (mkt.spot - pos.K), 0.0)
        return pos.notional * float(price(mkt.spot, pos.K, tau, mkt.rd, mkt.rf, mkt.vol(pos.K, tau), pos.cp))

    def carry(self, pair: str, mkt: SingleMarket, dt: float) -> float:
        """Tom-next carry on spot legs for ``dt`` years (quote ccy)."""
        n = sum(p.notional for p in self.positions if p.pair == pair and p.kind == "spot")
        c = n * mkt.spot * (mkt.rf - mkt.rd) * dt
        self.cash[pair] = self.cash.get(pair, 0.0) + c
        return c

    def settle_expiries(self, t: float, spots: dict) -> list[dict]:
        """Convert expired options: ITM -> spot position at the strike; OTM -> removed."""
        out, keep = [], []
        for p in self.positions:
            if p.kind == "option" and p.expiry <= t + 1e-12:
                S = spots[p.pair]
                phi = 1 if p.cp == "C" else -1
                itm = phi * (S - p.K) > 0
                if itm:
                    keep.append(Position(p.id, p.pair, "spot", p.notional * phi, p.K, 0.0, "C", p.tenor, "expiry",
                                         p.trade_id, p.client_type, f"exercised {p.label}", t))
                out.append({"pair": p.pair, "id": p.id, "cp": p.cp, "K": p.K, "notional": p.notional,
                            "itm": bool(itm), "spot": S,
                            "delivered_base": p.notional * phi if itm else 0.0})
            else:
                keep.append(p)
        self.positions = keep
        return out

    def remove(self, pid: int, exec_price_per_unit: float) -> Optional[Position]:
        """Close a position at ``exec_price_per_unit`` (option price, or spot rate for spot legs)."""
        for i, p in enumerate(self.positions):
            if p.id == pid:
                if p.kind == "option":
                    self.cash[p.pair] = self.cash.get(p.pair, 0.0) + p.notional * exec_price_per_unit
                else:
                    self.cash[p.pair] = self.cash.get(p.pair, 0.0) + p.notional * (exec_price_per_unit - p.K)
                return self.positions.pop(i)
        return None

    def trade_pnl(self, trade_id: int, mkts: dict) -> float:
        """MTM P&L (quote ccy) of one client trade's legs since inception (pre-hedge)."""
        v = self.trade_cash.get(trade_id, 0.0)
        for p in self.positions:
            if p.trade_id == trade_id:
                v += self.position_value(p, mkts[p.pair])
        return v
