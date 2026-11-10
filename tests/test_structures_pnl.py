import math

import numpy as np
import pytest

from engine.fx_conventions import TENORS, get_pair
from engine.market_data import build_market
from engine.pnl_attribution import attach_trading_terms, attribute_legs
from engine.structures import STRUCTURE_KINDS, build, equity_market, flat_market, market_from_surface

MKT = build_market()
JPY = market_from_surface(MKT.surface("USDJPY"))
EUR = market_from_surface(MKT.surface("EURUSD"))


def test_atm_straddle_is_delta_neutral_in_convention():
    s = build("straddle", JPY, "1M", 1e6)
    assert s.exposure(JPY).delta_pa == pytest.approx(0.0, abs=1e-6 * 1e6)
    s2 = build("straddle", EUR, "1M", 1e6)
    assert s2.exposure(EUR).delta == pytest.approx(0.0, abs=1e-6 * 1e6)


def test_short_straddle_signs():
    e = build("straddle", JPY, "1M", 1e6, side=-1).exposure(JPY)
    assert e.gamma_1pct < 0 and e.vega < 0 and e.theta > 0


@pytest.mark.parametrize("kind", STRUCTURE_KINDS)
def test_every_structure_builds_and_prices(kind):
    s = build(kind, EUR, "1M", 1e6)
    e = s.exposure(EUR)
    assert np.isfinite(e.value)
    h = s.delta_hedged(EUR)
    assert h.exposure(EUR).delta == pytest.approx(0.0, abs=1e-6)


def test_exposure_units_match_bumps():
    s = build("risk_reversal", EUR, "3M", 1e6)
    e = s.exposure(EUR)
    up, dn = EUR.bump_spot(0.01), EUR.bump_spot(-0.01)
    fd_gamma = (s.exposure(up).delta - s.exposure(dn).delta) / 2 * 100  # per 1%
    assert e.gamma_1pct == pytest.approx(fd_gamma, rel=1e-3, abs=1.0)
    fd_vega = (s.value(EUR.bump_vol(0.1)) - s.value(EUR.bump_vol(-0.1))) / 0.2
    assert e.vega == pytest.approx(fd_vega, rel=1e-3, abs=1.0)
    # theta on a flat surface (on a real surface the 1-day FD also picks up smile roll-down)
    flat = flat_market(get_pair("EURUSD"), 1.16, 0.036, 0.02, 0.07)
    sf = build("risk_reversal", flat, "3M", 1e6)
    fd_theta = sf.value(flat.pass_time(1)) - sf.value(flat)
    assert sf.exposure(flat).theta == pytest.approx(fd_theta, rel=0.02)


def test_vega_after_six_months_scales_with_sqrt_time():
    m = flat_market(get_pair("EURUSD"), 1.16, 0.0, 0.0, 0.08)
    s = build("straddle", m, "1Y", 1e6)
    v0 = s.exposure(m).vega
    v1 = s.exposure(m.pass_time(182.5)).vega
    assert v1 / v0 == pytest.approx(math.sqrt(0.5), abs=0.01)


def test_25d_call_delta_rises_with_vol():
    m = flat_market(get_pair("EURUSD"), 1.16, 0.036, 0.02, 0.10)
    s = build("call", m, "3M", 1.0, moneyness_delta=0.25)
    d0 = s.exposure(m).delta
    d1 = s.exposure(m.bump_vol(10)).delta
    assert d0 == pytest.approx(0.25, abs=0.01) and d1 > d0 and d1 < 0.5


def test_equity_market_skew_negative():
    m = equity_market(6000, 0.036, 0.013, 0.16, -3.5)
    assert m.vol(5400, 0.25) > m.vol(6600, 0.25)


def test_attribution_small_step_unexplained_small():
    s = build("straddle", EUR, "1M", 1e7)
    # one simulator-sized tick: 0.1% spot, 0.2 vol, 1/4 day
    m1 = EUR.bump_spot(0.1).bump_vol(0.2).pass_time(0.25)
    att = attribute_legs(s.legs, EUR, m1)
    assert abs(att.unexplained) < 0.01 * abs(att.actual) + 10
    assert att.terms["gamma"] > 0 and att.terms["theta"] < 0 and att.terms["vega"] > 0
    assert sum(att.vega_by_tenor.values()) == pytest.approx(att.terms["vega"])
    tot = att.actual
    attach_trading_terms(att, edge=100, hedge_cost=-20, carry=5)
    assert att.actual == pytest.approx(tot + 85)
    assert att.unexplained == pytest.approx(att.actual - att.explained)
