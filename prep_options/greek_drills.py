"""Section 1A: quickfire Greek drills, tiered by level. Ground truth by bumping the engine."""
from __future__ import annotations

import numpy as np

from engine.fx_conventions import TENORS
from engine.structures import build
from grading.question import Part, Question, chart_bar
from prep_options.common import GREEK_LABEL, GREEK_UNITS, fmt_greek, fx_market, pick_pair

DIR_OPTIONS = ["Increases (in size)", "Decreases (in size)", "Roughly unchanged"]
DIR_MAP = {"Increases": 0, "Decreases": 1, "Unchanged": 2}

MONEYNESS = {  # label -> (abs delta of strike or None for ATM, itm flag)
    "ATM": None, "25-delta OTM": 0.25, "10-delta OTM": 0.10, "75-delta ITM": 0.75,
}

def q_compare(rng: np.random.Generator, difficulty: int, seed: int) -> Question:
    """Which of two options has more gamma / vega / theta?"""
    pair = pick_pair(rng)
    mkt = fx_market(pair)
    g = str(rng.choice(["gamma_1pct", "vega", "theta"]))
    if rng.random() < 0.5:
        t1, t2 = rng.choice([("1W", "3M"), ("1M", "1Y"), ("2W", "6M")])
        m1, m2 = "ATM", "ATM"
    else:
        if rng.random() < 0.5:
            t1, t2 = rng.choice([("1W", "3M"), ("1M", "1Y"), ("ON", "1M"), ("2W", "6M")])
            m1 = m2 = str(rng.choice(["ATM", "25-delta OTM"]))
        else:
            t1 = t2 = str(rng.choice(["1W", "1M", "3M"]))
            m1, m2 = "ATM", str(rng.choice(["25-delta OTM", "10-delta OTM"]))
    if rng.random() < 0.5:
        t1, t2, m1, m2 = t2, t1, m2, m1
    sA = build("call", mkt, t1, 1e7, moneyness_delta=MONEYNESS[m1])
    sB = build("call", mkt, t2, 1e7, moneyness_delta=MONEYNESS[m2])
    a, b = getattr(sA.exposure(mkt), g), getattr(sB.exposure(mkt), g)
    gname = GREEK_LABEL[g]
    A = f"A: {t1} {m1} call"
    B = f"B: {t2} {m2} call"
    ratio = abs(a) / abs(b)
    correct = 0 if abs(a) > abs(b) * 1.03 else 1 if abs(b) > abs(a) * 1.03 else 2
    opts = [A, B, "About the same"]
    why = {
        "gamma_1pct": "ATM gamma ~ e^(-rf T) n(d1) / (S vol sqrt(T)): the shorter the expiry the more concentrated (and larger) gamma is near the strike. For OTM strikes this reverses close to expiry, because the strike becomes many standard deviations away.",
        "vega": "Vega ~ S e^(-rf T) n(d1) sqrt(T): longer expiries carry more vega because there is more time for vol to matter. At a given expiry ATM has the most vega; OTM has less (n(d1) is smaller).",
        "theta": "ATM theta ~ -S n(d1) vol / (2 sqrt(T)): short-dated ATM options decay fastest per day. That is the flip side of their larger gamma (gamma/theta trade-off).",
    }[g]
    model = (f"**Answer: {opts[correct]}.**\n\n1. Intuition: {why}\n"
             f"2. Engine numbers (EUR/base 10m each): A = {fmt_greek(mkt, g, a)}, B = {fmt_greek(mkt, g, b)}; "
             f"|A|/|B| = {ratio:.2f}.\n")
    if g == "gamma_1pct" and m1 == m2 == "ATM":
        model += f"3. Rule of thumb: ATM gamma ratio ~ sqrt(T_B / T_A) = {np.sqrt(TENORS[t2]/TENORS[t1]):.2f}.\n"
    if g == "vega" and m1 == m2 == "ATM":
        model += f"3. Rule of thumb: ATM vega ratio ~ sqrt(T_A / T_B) = {np.sqrt(TENORS[t1]/TENORS[t2]):.2f}.\n"
    facts = {"pair": pair, "greek": gname, "A": A, "B": B, "A_value": a, "B_value": b, "ratio_abs_A_over_B": ratio}
    return Question(section="options", subsection="1A", topic=f"greeks:{g.replace('_1pct','')}",
                    difficulty=difficulty, template="compare", seed=seed,
                    prompt=f"{pair}, same notional. Which option has more **{gname.lower()}** (in size)?\n\n- {A}\n- {B}",
                    parts=[Part("mcq", "Which has more?", opts, correct)],
                    free_text_prompt="Why?", facts=facts, model_answer=model,
                    rubric=[f"Answer {opts[correct]}", why],
                    charts=[chart_bar(f"{gname}: A vs B", ["A", "B"], [a, b], f"{gname} ({GREEK_UNITS[g]})")])


# ---------------------------------------------------------------------------
# Levels (v2)
#   L1: first-order Greeks, direction only (coverage matrix) + 'which has more' comparisons
#   L2: second-order Greeks, direction only (coverage matrix) + 'use vanna/volga/... to say how X moves'
#   L3: calculations with every input in a Givens box
# ---------------------------------------------------------------------------
from prep_options import calcs, greek_matrix  # noqa: E402

_COVERAGE_PROVIDER = None


def set_coverage_provider(fn) -> None:
    """fn(matrix_name) -> set of covered cells (the UI plugs in the database)."""
    global _COVERAGE_PROVIDER
    _COVERAGE_PROVIDER = fn


def _covered(level: int):
    if _COVERAGE_PROVIDER is None:
        return None
    try:
        return set(_COVERAGE_PROVIDER(greek_matrix.matrix_name(level)))
    except Exception:
        return None


def generate(seed: int, difficulty: int) -> Question:
    rng = np.random.default_rng(seed)
    u = rng.random()
    if difficulty == 1:
        if u < 0.85:
            return greek_matrix.matrix_question(seed, 1, _covered(1))
        return q_compare(rng, 1, seed)
    if difficulty == 2:
        if u < 0.7:
            return greek_matrix.matrix_question(seed, 2, _covered(2))
        return greek_matrix.via_question(seed, 2)
    fn = [calcs.q_time_scaling, calcs.q_rv_iv, calcs.q_breakeven, calcs.q_vega_buckets][int(rng.integers(4))]
    return fn(rng, 3, seed, "1A")
