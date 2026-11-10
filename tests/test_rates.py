import math

import pytest

from engine.rates import (BP, ZeroCurve, annuity, bachelier_swaption, bond_price, bond_risk, bond_yield,
                          conversion_factor, ctd_analysis, floater_dv01, implied_move_probability,
                          key_rate_dv01s, par_swap_rate, price_change_approx, receiver_carry_rolldown,
                          swap_dv01, swap_pv, zero_coupon_price)


def test_hull_bond_duration_example():
    # Hull Table 4.6: 3y 10% semiannual bond, 12% continuously compounded yield
    y = 2 * (math.exp(0.06) - 1)
    r = bond_risk(y, 0.10, 3, 2)
    assert r.price == pytest.approx(94.213, abs=1e-3)
    assert r.macaulay == pytest.approx(2.653, abs=1e-3)
    assert r.modified == pytest.approx(2.653 / (1 + y / 2), abs=1e-3)


@pytest.mark.parametrize("c,m,f,y", [(0.04, 10, 2, 0.045), (0.0, 7, 1, 0.03), (0.08, 30, 2, 0.05),
                                     (0.02, 2, 1, 0.04)])
def test_duration_convexity_match_fd(c, m, f, y):
    r = bond_risk(y, c, m, f)
    h = 1e-5
    up, dn = bond_price(y + h, c, m, f), bond_price(y - h, c, m, f)
    assert r.modified == pytest.approx(-(up - dn) / (2 * h) / r.price, rel=1e-7)
    assert r.convexity == pytest.approx((up - 2 * r.price + dn) / h ** 2 / r.price, rel=1e-4)
    assert r.dv01 == pytest.approx((dn - up) / (2 * h) * BP, rel=1e-7)


def test_zero_coupon_duration_equals_maturity():
    r = bond_risk(0.04, 0.0, 10, 1)
    assert r.macaulay == pytest.approx(10.0)
    assert zero_coupon_price(0.04, 10) == pytest.approx(r.price)


def test_longer_and_lower_coupon_more_duration():
    assert bond_risk(0.04, 0.04, 10).modified > bond_risk(0.04, 0.04, 5).modified
    assert bond_risk(0.04, 0.01, 10).modified > bond_risk(0.04, 0.06, 10).modified


def test_price_change_approx_accuracy():
    r = bond_risk(0.04, 0.04, 20)
    for dy in (-0.01, 0.01):
        actual = bond_price(0.04 + dy, 0.04, 20) - r.price
        approx = price_change_approx(r.price, r.modified, r.convexity, dy)
        assert abs(approx["total"] - actual) < abs(approx["duration_term"] - actual)
        assert abs(approx["total"] - actual) / abs(actual) < 0.01
    assert bond_yield(r.price, 0.04, 20) == pytest.approx(0.04)


def test_swap_par_dv01_and_directions():
    c = ZeroCurve.from_pct({0.5: 3.5, 2: 3.3, 5: 3.5, 10: 4.0, 30: 4.5})
    S = par_swap_rate(c, 0, 10)
    assert swap_pv(c, S, 0, 10, 1e6) == pytest.approx(0.0, abs=1e-6)
    rec = swap_dv01(c, S, 0, 10, 1e6, "receive")
    pay = swap_dv01(c, S, 0, 10, 1e6, "pay")
    assert rec > 0 and pay == pytest.approx(-rec)
    assert rec == pytest.approx(annuity(c, 0, 10) * 1e6 * BP, rel=0.03)
    assert abs(floater_dv01(c, 1e6)) < 0.05 * rec
    fwd_start = swap_dv01(c, par_swap_rate(c, 5, 10), 5, 10, 1e6)
    assert 0 < fwd_start < rec


def test_bachelier_parity_and_greeks():
    F, K, T, v, A = 0.035, 0.036, 1.0, 0.0085, 8.5
    p = bachelier_swaption(F, K, T, v, A, "payer")
    r = bachelier_swaption(F, K, T, v, A, "receiver")
    assert p.price - r.price == pytest.approx(A * (F - K), abs=1e-14)
    atm = bachelier_swaption(F, F, T, v, A, "payer")
    assert atm.price == pytest.approx(A * v * math.sqrt(T) / math.sqrt(2 * math.pi))
    h = 1e-6
    fd = (bachelier_swaption(F + h, K, T, v, A).price - bachelier_swaption(F - h, K, T, v, A).price) / (2 * h)
    assert p.delta_rate == pytest.approx(fd, rel=1e-6)
    assert p.dv01 < 0 and r.dv01 > 0  # payer = short duration, receiver = long duration
    fd_g = (bachelier_swaption(F + BP, K, T, v, A).delta_rate - bachelier_swaption(F - BP, K, T, v, A).delta_rate) / 2 * BP
    assert p.gamma_dv01_per_bp == pytest.approx(fd_g, rel=1e-4)
    assert p.gamma_dv01_per_bp > 0 and r.gamma_dv01_per_bp > 0
    fd_v = (bachelier_swaption(F, K, T, v + BP, A).price - bachelier_swaption(F, K, T, v - BP, A).price) / 2
    assert p.vega_bp == pytest.approx(fd_v, rel=1e-6)


def test_ctd_switches_with_yield_level():
    basket = [(0.04, 8), (0.05, 15), (0.035, 25)]
    low = [r for r in ctd_analysis(basket, 0.03) if r["ctd"]][0]
    high = [r for r in ctd_analysis(basket, 0.08) if r["ctd"]][0]
    # above the notional coupon long-duration bonds are cheapest; below, short-duration
    assert high["mod_dur"] > low["mod_dur"]
    assert conversion_factor(0.06, 10) == pytest.approx(1.0)


def test_implied_probability_example():
    assert implied_move_probability(-15)["prob_next_step"] == pytest.approx(0.6)
    r = implied_move_probability(-35)
    assert r["full_steps_certain"] == 1 and r["prob_next_step"] == pytest.approx(0.4)


def test_carry_rolldown_steep_curve():
    c = ZeroCurve.from_pct({0.25: 2.0, 1: 2.3, 5: 3.5, 10: 4.2})
    r5 = receiver_carry_rolldown(c, 5)
    assert r5["carry_bp"] > 0 and r5["roll_bp"] > 0


def test_key_rate_dv01_sum_to_parallel():
    c = ZeroCurve.from_pct({1: 3.0, 2: 3.1, 5: 3.4, 10: 3.9, 30: 4.3})
    S = par_swap_rate(c, 0, 10)
    pv = lambda cc: swap_pv(cc, S, 0, 10, 1e6)
    kr = key_rate_dv01s(pv, c, [1, 2, 5, 10, 30])
    assert sum(kr.values()) == pytest.approx(swap_dv01(c, S, 0, 10, 1e6), rel=0.02)
    assert max(kr, key=kr.get) == 10
