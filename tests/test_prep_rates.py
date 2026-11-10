import numpy as np
import pytest

import prep_rates as pr
from engine.rates import par_swap_rate
from prep_rates.instruments import (Bond, Composite, Swap, Swaption, base_curve, callable_bond, move_curve,
                                    pnl, risk)


@pytest.mark.parametrize("sub", list(pr.SUBSECTIONS))
@pytest.mark.parametrize("diff", [1, 2, 3])
def test_rates_generators(sub, diff):
    for seed in range(10):
        q = pr.generate(sub, 500 * diff + seed, diff)
        assert q.section == "rates" and q.subsection == sub and q.model_answer and q.rubric
        for p in q.parts:
            if p.kind == "mcq":
                assert 0 <= p.correct < len(p.options)
            if p.kind == "numeric":
                assert np.isfinite(p.correct)


def test_exposure_signs():
    c = base_curve()
    F = par_swap_rate(c, 1, 11)
    rec = risk(Swaption(1, 10, F, 0.0085, "receiver", 1e8), c)
    pay = risk(Swaption(1, 10, F, 0.0085, "payer", 1e8), c)
    short_rec = risk(Swaption(1, 10, F, 0.0085, "receiver", -1e8), c)
    assert rec.dv01 > 0 and rec.convexity_pnl > 0
    assert pay.dv01 < 0 and pay.convexity_pnl > 0
    assert short_rec.convexity_pnl < 0
    sw_r = risk(Swap(0, 10, par_swap_rate(c, 0, 10), 1e8, "receive"), c)
    assert sw_r.dv01 > 0
    cb = callable_bond(0.045, 10, 2, 1e8, 0.0085, c)
    r = risk(cb, c)
    assert r.dv01 > 0 and r.convexity_pnl < 0  # long duration, short convexity
    assert risk(cb, c.shifted(-50)).dv01 < r.dv01  # duration shortens in a rally


def test_move_curve_parallel_matches_shift():
    c = base_curve()
    b = Bond(0.04, 10, 1e8)
    assert pnl(b, c, move_curve(c, {0: 25})) == pytest.approx(pnl(b, c, c.shifted(25)), rel=1e-12)


def test_unlock_rules():
    stats = {"2A-1": {"n": 5, "avg": 7.0}, "2A-2": {"n": 1, "avg": 9.0}}
    locked = pr.locked_stages(lambda c: stats.get(c, {"n": 0, "avg": 0.0}))
    assert "2A-2" not in locked and "2A-3" in locked and "2A-5" in locked
    assert pr.locked_stages(lambda c: {"n": 0, "avg": 0}, unlock_all=True) == {}


def test_sonia_probability_example():
    from engine.rates import implied_move_probability
    assert implied_move_probability(-15)["prob_next_step"] == pytest.approx(0.6)
