import math

import numpy as np
import pytest

from engine.fx_pricer import (GKPricer, ImpliedVolError, compare_pricers, greeks, implied_vol,
                              price, price_bounds)

CASES = [
    (1.10, 1.10, 0.25, 0.04, 0.02, 0.08),
    (1.10, 1.20, 1.00, 0.04, 0.02, 0.10),
    (150.0, 140.0, 0.08, 0.005, 0.045, 0.12),
    (0.66, 0.60, 0.5, 0.035, 0.04, 0.15),
    (1.30, 1.45, 2 / 52, 0.03, 0.04, 0.30),
]


@pytest.mark.parametrize("S,K,T,rd,rf,v", CASES)
def test_put_call_parity_fx(S, K, T, rd, rf, v):
    c = price(S, K, T, rd, rf, v, "C")
    p = price(S, K, T, rd, rf, v, "P")
    assert c - p == pytest.approx(S * math.exp(-rf * T) - K * math.exp(-rd * T), abs=1e-12)


def test_hull_known_value():
    # Hull, Options Futures & Other Derivatives, Example 15.6 (rf = 0 reduces GK to BS)
    assert price(42, 40, 0.5, 0.10, 0.0, 0.20, "C") == pytest.approx(4.76, abs=0.005)
    assert price(42, 40, 0.5, 0.10, 0.0, 0.20, "P") == pytest.approx(0.81, abs=0.005)


def test_gk_equals_bs_with_dividend_yield_style():
    # GK with rf=q is Black-Scholes-Merton with continuous dividend yield
    S, K, T, r, q, v = 100, 95, 0.75, 0.05, 0.02, 0.25
    d1 = (math.log(S / K) + (r - q + v * v / 2) * T) / (v * math.sqrt(T))
    d2 = d1 - v * math.sqrt(T)
    from scipy.stats import norm
    bsm = S * math.exp(-q * T) * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    assert price(S, K, T, r, q, v, "C") == pytest.approx(bsm, rel=1e-12)


@pytest.mark.parametrize("S,K,T,rd,rf,v", CASES)
@pytest.mark.parametrize("cp", ["C", "P"])
def test_greeks_vs_finite_differences(S, K, T, rd, rf, v, cp):
    g = greeks(S, K, T, rd, rf, v, cp)
    hS, hv, hT, hr = S * 1e-5, 1e-4, 1e-5, 1e-6
    P = lambda S_=S, T_=T, rd_=rd, rf_=rf, v_=v: float(price(S_, K, T_, rd_, rf_, v_, cp))
    fd_delta = (P(S_=S + hS) - P(S_=S - hS)) / (2 * hS)
    fd_gamma = (P(S_=S + hS) - 2 * P() + P(S_=S - hS)) / hS ** 2
    fd_vega = (P(v_=v + hv) - P(v_=v - hv)) / (2 * hv)
    fd_theta = -(P(T_=T + hT) - P(T_=T - hT)) / (2 * hT)
    fd_rhod = (P(rd_=rd + hr) - P(rd_=rd - hr)) / (2 * hr)
    fd_rhof = (P(rf_=rf + hr) - P(rf_=rf - hr)) / (2 * hr)
    D = lambda S_=S, T_=T, v_=v: greeks(S_, K, T_, rd, rf, v_, cp).delta
    V = lambda v_=v: greeks(S, K, T, rd, rf, v_, cp).vega
    fd_vanna = (D(v_=v + hv) - D(v_=v - hv)) / (2 * hv)
    fd_volga = (V(v + hv) - V(v - hv)) / (2 * hv)
    fd_charm = -(D(T_=T + hT) - D(T_=T - hT)) / (2 * hT)
    scale = S
    assert g.delta == pytest.approx(fd_delta, abs=1e-7)
    assert g.gamma == pytest.approx(fd_gamma, rel=2e-4, abs=1e-6 / S)
    assert g.vega == pytest.approx(fd_vega, rel=1e-6, abs=1e-9 * scale)
    assert g.theta == pytest.approx(fd_theta, rel=1e-4, abs=1e-8 * scale)
    assert g.rho_d == pytest.approx(fd_rhod, rel=1e-6, abs=1e-9 * scale)
    assert g.rho_f == pytest.approx(fd_rhof, rel=1e-6, abs=1e-9 * scale)
    assert g.vanna == pytest.approx(fd_vanna, rel=1e-5, abs=1e-8)
    assert g.volga == pytest.approx(fd_volga, rel=1e-5, abs=1e-8 * scale)
    assert g.charm == pytest.approx(fd_charm, rel=1e-4, abs=1e-6)
    assert g.delta_pa == pytest.approx(g.delta - g.price / S, abs=1e-14)


@pytest.mark.parametrize("T", [1 / 365, 7 / 365, 1 / 12, 0.25, 1.0])
@pytest.mark.parametrize("kp", [0.7, 0.85, 0.95, 1.0, 1.05, 1.2, 1.4])
@pytest.mark.parametrize("cp", ["C", "P"])
def test_implied_vol_round_trip(T, kp, cp):
    S, rd, rf = 1.10, 0.04, 0.02
    for v in (0.04, 0.10, 0.35):
        K = S * kp
        p = float(price(S, K, T, rd, rf, v, cp))
        lo, _ = price_bounds(S, K, T, rd, rf, cp)
        # skip options whose time value is below machine precision (vol not identifiable)
        if p - lo < 1e-13:
            continue
        iv = implied_vol(p, S, K, T, rd, rf, cp)
        assert float(price(S, K, T, rd, rf, iv, cp)) == pytest.approx(p, abs=1e-12)
        vega = greeks(S, K, T, rd, rf, v, cp).vega
        if vega > 1e-6:
            assert iv == pytest.approx(v, abs=1e-6)


def test_implied_vol_rejects_arbitrage_price():
    with pytest.raises(ImpliedVolError):
        implied_vol(2.0, 1.1, 1.1, 0.5, 0.04, 0.02, "C")


def test_compare_pricers_self_is_zero():
    df = compare_pricers(GKPricer())
    assert np.max(np.abs(df["diff"])) == 0.0


def test_expiry_intrinsic():
    assert float(price(1.2, 1.1, 0.0, 0.03, 0.01, 0.1, "C")) == pytest.approx(0.1)
    assert float(price(1.2, 1.1, 0.0, 0.03, 0.01, 0.1, "P")) == 0.0
