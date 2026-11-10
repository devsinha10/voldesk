import math

import numpy as np
import pytest

from engine.fx_conventions import (PAIRS, all_spots, atm_dns_strike, delta, forward_points, get_pair,
                                   premium_pct_base, premium_pips, strike_from_delta, usd_per_quote)
from engine.fx_pricer import forward, greeks


def test_pips_and_ordering():
    assert get_pair("USDJPY").pip == 0.01
    assert get_pair("EURJPY").pip == 0.01
    assert get_pair("EURUSD").pip == 0.0001
    assert get_pair("EURUSD").base == "EUR" and get_pair("EURUSD").quote == "USD"
    assert len(PAIRS) == 10


def test_premium_adjusted_flags():
    pa = {n for n, p in PAIRS.items() if p.premium_adjusted}
    assert pa == {"USDJPY", "USDCHF", "USDCAD", "EURJPY", "EURGBP", "EURCHF"}
    assert get_pair("USDJPY").delta_convention(0.5) == "spot_pa"
    assert get_pair("EURUSD").delta_convention(1.0) == "spot"
    assert get_pair("EURUSD").delta_convention(2.0) == "fwd"


def test_crosses_triangulate():
    usd = {"EURUSD": 1.16, "USDJPY": 152.0, "GBPUSD": 1.32, "AUDUSD": 0.66, "NZDUSD": 0.58,
           "USDCAD": 1.39, "USDCHF": 0.80}
    s = all_spots(usd)
    assert s["EURJPY"] == pytest.approx(1.16 * 152.0)
    assert s["EURGBP"] == pytest.approx(1.16 / 1.32)
    assert s["EURCHF"] == pytest.approx(1.16 * 0.80)
    assert usd_per_quote("EURJPY", s) == pytest.approx(1 / 152.0)


def test_forward_points_cip():
    S, T, rd, rf = 152.0, 0.25, 0.0075, 0.036  # USDJPY: rd = JPY, rf = USD
    fp = forward_points(S, T, rd, rf, 0.01)
    assert fp == pytest.approx((S * math.exp((rd - rf) * T) - S) / 0.01)
    assert fp < 0  # USD has higher rate -> USDJPY forward points negative


def test_premium_display():
    assert premium_pips(0.0123, 0.0001) == pytest.approx(123)
    assert premium_pct_base(0.0116, 1.16) == pytest.approx(1.0)


@pytest.mark.parametrize("conv", ["spot", "fwd", "spot_pa", "fwd_pa"])
@pytest.mark.parametrize("d", [0.10, 0.25, 0.40, -0.10, -0.25, -0.40])
@pytest.mark.parametrize("T,v", [(1 / 365, 0.09), (1 / 12, 0.10), (0.5, 0.12), (1.0, 0.20)])
def test_strike_from_delta_inverts(conv, d, T, v):
    S, rd, rf = 152.0, 0.0075, 0.036
    cp = "C" if d > 0 else "P"
    K = strike_from_delta(d, S, T, rd, rf, v, cp, conv)
    assert delta(S, K, T, rd, rf, v, cp, conv) == pytest.approx(d, abs=1e-10)
    if conv.endswith("pa") and cp == "C":
        # must be on the OTM branch: strike above forward
        assert K > forward(S, T, rd, rf)


@pytest.mark.parametrize("pa", [False, True])
def test_atm_dns_is_delta_neutral(pa):
    S, T, rd, rf, v = 1.16, 0.5, 0.036, 0.02, 0.08
    F = forward(S, T, rd, rf)
    K = atm_dns_strike(F, T, v, pa)
    conv = "spot_pa" if pa else "spot"
    dc = delta(S, K, T, rd, rf, v, "C", conv)
    dp = delta(S, K, T, rd, rf, v, "P", conv)
    assert dc + dp == pytest.approx(0.0, abs=1e-12)


def test_pa_delta_equals_delta_minus_premium_over_spot():
    S, K, T, rd, rf, v = 152.0, 155.0, 0.25, 0.0075, 0.036, 0.10
    g = greeks(S, K, T, rd, rf, v, "C")
    assert delta(S, K, T, rd, rf, v, "C", "spot_pa") == pytest.approx(g.delta - g.price / S, abs=1e-12)
