import numpy as np
import pytest

from engine.fx_conventions import PAIRS, TENORS
from engine.market_data import build_market, default_quotes, parse_frankfurter
from engine.smile import SmileQuotes, TenorSmile, sabr_vol
from engine.surface import RateCurve, VolSurface

MKT = build_market()
TOL = 0.0015  # 0.15 vol


@pytest.mark.parametrize("pair", list(PAIRS))
def test_sabr_reproduces_quotes(pair):
    surf = MKT.surface(pair)
    for t, sm in surf.smiles.items():
        assert sm.model == "sabr", f"{pair} {t} fell back"
        q, iq = surf.quotes[t], sm.implied_quotes()
        assert iq.atm == pytest.approx(q.atm, abs=1e-8)       # ATM exact
        for f in ("rr25", "bf25", "rr10", "bf10"):
            assert abs(getattr(iq, f) - getattr(q, f)) < TOL, (pair, t, f)


@pytest.mark.parametrize("pair", list(PAIRS))
def test_default_surfaces_arbitrage_free(pair):
    rep = MKT.surface(pair).check_arbitrage()
    assert rep.ok, (rep.calendar_violations, rep.butterfly_violations)


def test_pillar_strikes_have_right_delta():
    surf = MKT.surface("USDJPY")
    sm = surf.smiles["1M"]
    for name, d in (("25C", 0.25), ("25P", -0.25), ("10C", 0.10), ("10P", -0.10)):
        K = sm.pillar_strikes[name]
        from engine.fx_conventions import delta
        assert delta(sm.S, K, sm.T, sm.rd, sm.rf, sm.pillar_vols[name], "C" if d > 0 else "P",
                     sm.convention) == pytest.approx(d, abs=1e-10)


def test_smile_strike_for_delta_inverts():
    sm = MKT.surface("EURUSD").smiles["3M"]
    for d in (0.15, 0.25, 0.35, -0.2, -0.3):
        K = sm.strike_for_delta(d)
        assert sm.delta_at(K, "C" if d > 0 else "P") == pytest.approx(d, abs=1e-9)


def test_vanna_volga_fallback_hits_3_points():
    q = SmileQuotes(0.10, -0.01, 0.002, -0.019, 0.007)
    sm = TenorSmile(T=0.25, S=152.0, rd=0.0075, rf=0.036, quotes=q, convention="spot_pa",
                    premium_adjusted=True, tol=-1.0)  # negative tol forces fallback
    assert sm.model == "vanna_volga"
    for n in ("25P", "ATM", "25C", "10P", "10C"):
        assert float(sm.vol(sm.pillar_strikes[n])) == pytest.approx(sm.pillar_vols[n], abs=1e-12)


def test_sabr_atm_limit_finite():
    v = sabr_vol(1.0, 1.0, 0.5, 0.1, 1.0, -0.3, 0.8)
    assert np.isfinite(v)
    assert v == pytest.approx(0.1 * (1 + (0.25 * -0.3 * 0.8 * 0.1 + (2 - 3 * 0.09) / 24 * 0.64) * 0.5))


def test_surface_interpolation_total_variance():
    surf = MKT.surface("EURUSD")
    T1, T2 = TENORS["1M"], TENORS["2M"]
    Tm = 0.5 * (T1 + T2)
    a = surf.atm_vol(Tm)
    w1, w2 = surf.quotes["1M"].atm ** 2 * T1, surf.quotes["2M"].atm ** 2 * T2
    assert a ** 2 * Tm == pytest.approx(0.5 * (w1 + w2))
    # pillar vol reproduces the smile
    K = surf.smiles["3M"].pillar_strikes["25C"]
    assert surf.vol(K, TENORS["3M"]) == pytest.approx(surf.smiles["3M"].pillar_vols["25C"], abs=TOL)


def test_calendar_arbitrage_detected():
    q = default_quotes("EURUSD")
    bad = dict(q)
    bad["6M"] = SmileQuotes(0.04, q["6M"].rr25, q["6M"].bf25, q["6M"].rr10, q["6M"].bf10)
    s = VolSurface("EURUSD", 1.16, RateCurve(0.036), RateCurve(0.02), bad)
    assert not s.check_arbitrage().calendar_ok


def test_parse_frankfurter():
    payload = {"base": "USD", "rates": {"EUR": 0.862, "JPY": 152.0, "GBP": 0.757, "AUD": 1.515,
                                        "NZD": 1.724, "CAD": 1.39, "CHF": 0.80}}
    s = parse_frankfurter(payload)
    assert s["EURUSD"] == pytest.approx(1 / 0.862)
    assert s["USDJPY"] == 152.0
    assert parse_frankfurter({"rates": {"EUR": 1}}) is None
