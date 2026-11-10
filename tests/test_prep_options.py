import numpy as np
import pytest

import prep_options as po
from engine.structures import build
from grading.question import Part
from prep_options.common import fx_market


@pytest.mark.parametrize("sub", list(po.SUBSECTIONS))
@pytest.mark.parametrize("diff", [1, 2, 3])
def test_generators_produce_valid_questions(sub, diff):
    for seed in range(15):
        q = po.generate(sub, 1000 * diff + seed, diff)
        assert q.prompt and q.model_answer and q.topic and q.rubric
        assert q.section == "options" and q.subsection == sub
        for p in q.parts:
            if p.kind == "mcq":
                assert 0 <= p.correct < len(p.options)
            if p.kind == "sign_table":
                assert set(p.rows) <= set(p.correct)


def test_generation_is_deterministic():
    a = po.generate("1B", 42, 3)
    b = po.generate("1B", 42, 3)
    assert a.prompt == b.prompt and a.parts[0].correct == b.parts[0].correct


def test_exposure_signs_match_engine():
    # perfect answers score 10 and the signs agree with the engine for clear cases
    for seed in range(25):
        q = po.generate("1B", seed, 2)
        p = q.parts[0]
        perfect = {r: (c[0] if isinstance(c, list) else c) for r, c in p.correct.items()}
        assert q.auto_score({0: perfect}) == pytest.approx(10.0)
        before = q.facts["before"]
        for r, c in p.correct.items():
            if isinstance(c, str) and c != "0" and r != "Delta":
                assert np.sign(before[r]) == (1 if c == "+" else -1)


def test_short_straddle_example_from_brief():
    m = fx_market("USDJPY")
    s = build("straddle", m, "1M", 1e7, side=-1)
    e0, e1 = s.exposure(m), s.exposure(m.bump_vol(4))
    assert abs(e0.delta_pa) < 0.01 * 1e7          # roughly delta-flat
    assert e0.gamma_1pct < 0 and e0.vega < 0 and e0.theta > 0
    assert abs(e1.gamma_1pct) < abs(e0.gamma_1pct)  # less short gamma after the spike
    assert e1.theta > e0.theta                      # more theta income
    assert s.value(m.bump_vol(4)) < s.value(m)      # immediate vega loss


def test_quickfire_25d_call_delta_rises_with_vol_example():
    m = fx_market("EURUSD")
    s = build("call", m, "3M", 1.0, moneyness_delta=0.25)
    assert s.exposure(m.bump_vol(10)).delta > s.exposure(m).delta


def test_part_marking():
    assert Part("mcq", "x", ["a", "b"], 1).mark(1) == 1.0
    p = Part("numeric", "x", correct=0.71, tol_abs=0.05)
    assert p.mark(0.7) == 1.0 and p.mark(0.78) == 0.5 and p.mark(1.0) == 0.0
    st = Part("sign_table", "s", rows=["Delta", "Gamma"], correct={"Delta": ["+", "0"], "Gamma": "-"})
    assert st.mark({"Delta": "0", "Gamma": "-"}) == 1.0
    assert st.mark({"Delta": "-", "Gamma": "-"}) == 0.5
