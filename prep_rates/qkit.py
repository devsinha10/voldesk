"""Small helpers shared by the rates question generators."""
from __future__ import annotations

from typing import Optional

import numpy as np

from engine.rates import bond_price, bond_risk
from grading.question import Part, Question
from prep_rates.instruments import Instrument, ZeroCurve, fmt_ccy

LONG_SHORT = ["Long", "Short"]
GAIN_LOSE = ["Gain", "Lose", "Roughly nothing"]


def Q(sub: str, topic: str, level: int, template: str, seed: int, prompt: str, parts: list,
      free: Optional[str], model: str, rubric: list, facts: Optional[dict] = None, charts=None, tables=None) -> Question:
    return Question("rates", sub, topic, level, template, seed, prompt=prompt, parts=parts, free_text_prompt=free,
                    model_answer=model, rubric=rubric, facts=facts or {}, charts=charts or [], tables=tables or [])


def mcq(label: str, opts: list, correct: int, weight: float = 1.0) -> Part:
    return Part("mcq", label, list(opts), int(correct), weight=weight)


def num(label: str, unit: str = "", tol_rel: float = 0.02, tol_abs: float = 0.0) -> Part:
    return Part("numeric", label, tol_rel=tol_rel, tol_abs=tol_abs, unit=unit)


def bond_info(coupon: float, maturity: float, y: float, freq: int = 2) -> dict:
    """Price (per 100), modified duration, convexity, DV01 per 100 face."""
    r = bond_risk(y, coupon, maturity, freq)
    return {"price": r.price, "dmod": r.modified, "convexity": r.convexity, "dv01_100": r.dv01, "mac": r.macaulay}


def bond_exact_pnl(face: float, coupon: float, maturity: float, y: float, dy_bp: float, freq: int = 2) -> float:
    """Full-repricing P&L of a long ``face`` position for a yield move of ``dy_bp``."""
    return face / 100 * (bond_price(y + dy_bp * 1e-4, coupon, maturity, freq) - bond_price(y, coupon, maturity, freq))


def approx_pnl(face: float, price: float, dmod: float, convexity: float, dy_bp: float) -> tuple[float, float]:
    """Duration and convexity terms of dP ~ -D P dy + 0.5 C P dy^2, scaled to ``face``."""
    dy = dy_bp * 1e-4
    return face / 100 * (-dmod * price * dy), face / 100 * (0.5 * convexity * price * dy * dy)


def approx_vs_exact_text(dur: float, cvx: float, exact: float) -> str:
    tot = dur + cvx
    return (f"(a) Approximation: duration term {fmt_ccy(dur)} + convexity term {fmt_ccy(cvx)} = **{fmt_ccy(tot)}**.\n"
            f"(b) Exact full repricing (engine): **{fmt_ccy(exact)}**.\n"
            f"Gap: {fmt_ccy(exact - tot)} ({(exact - tot) / abs(exact) * 100 if exact else 0:+.2f}% of the move), "
            f"from the higher-order terms the two-term Taylor expansion leaves out. It grows with the size of the "
            f"move and with maturity.")


def dv01_gamma(inst: Instrument, curve: ZeroCurve) -> float:
    """Change in DV01 (long-duration positive) for a +1bp parallel move."""
    def dv(c):
        return (inst.pv(c.shifted(-1)) - inst.pv(c.shifted(1))) / 2
    return (dv(curve.shifted(1)) - dv(curve.shifted(-1))) / 2


def shuffle_opts(rng, correct_text: str, others: list) -> tuple[list, int]:
    opts = [correct_text] + list(others)
    order = rng.permutation(len(opts))
    opts = [opts[k] for k in order]
    return opts, int(np.where(order == 0)[0][0])
