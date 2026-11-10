import warnings

import numpy as np
import pytest

from engine.fx_conventions import PAIRS, TENOR_LIST, TENORS, get_pair
from engine.market_sim import MarketSim
from engine.surface import atm_calendar_ok
from simulator.book import Book
from simulator.clients import RFQ, client_decides, metric_and_vega
from simulator.debrief import rule_based_review, scorecard
from simulator.session import SimSession

warnings.filterwarnings("ignore")


def test_market_is_seeded_and_replayable():
    a, b = MarketSim(42, 2), MarketSim(42, 2)
    for _ in range(60):
        a.step(); b.step()
    assert a.regime == b.regime and a.pairs == b.pairs
    assert all(a.spot(p) == b.spot(p) for p in PAIRS)
    c = MarketSim(43, 2)
    for _ in range(60):
        c.step()
    assert any(abs(a.spot(p) - c.spot(p)) > 1e-12 for p in PAIRS)


def test_crosses_consistent_and_calendar_arb_free():
    m = MarketSim(7, 3, regime="risk_off")
    for _ in range(120):
        m.step()
        assert m.spot("EURJPY") == pytest.approx(m.spot("EURUSD") * m.spot("USDJPY"), rel=1e-12)
        for p in m.pairs:
            assert atm_calendar_ok(m.quotes(p))
    # spot levels stay plausible
    assert 100 < m.spot("USDJPY") < 220 and 0.8 < m.spot("EURUSD") < 1.6


def test_usdjpy_spot_vol_correlation_negative():
    m = MarketSim(5, 3, regime="calm")
    rets, dvol = [], []
    for _ in range(400):
        s0, l0 = m.spot("USDJPY"), m.state["USDJPY"].level
        m.step()
        rets.append(np.log(m.spot("USDJPY") / s0))
        dvol.append(m.state["USDJPY"].level - l0)
    assert np.corrcoef(rets, dvol)[0, 1] < -0.2


def test_event_priced_then_crushed():
    m = MarketSim(3, 1, regime="cb_week")
    e = m.events[0]
    pair = m.pairs[0]
    while m.day_float < e.day - 0.05:
        m.step()
    pre = m.quotes(pair)["1W"].atm
    while not e.done:
        m.step()
    post = m.quotes(pair)["1W"].atm
    assert post < pre


def test_session_pnl_identity_and_expiry():
    s = SimSession(11, 1, inherit=True)
    while not s.market.finished:
        if s.paused:
            s.toggle_pause()
        s.step()
        for r in s.open_rfqs():
            fair, _, _ = metric_and_vega(r, s.mkt(r.pair))
            s.quote(r.id, fair - 0.15, fair + 0.15)
        if s.market.tick % 20 == 0:
            for p in s.pairs:
                s.delta_hedge(p)
    t = s.total_terms
    total = sum(v for k, v in t.items() if k != "vega_by_tenor")
    assert total == pytest.approx(s.pnl_usd, rel=1e-9, abs=1e-6)
    greek = sum(abs(t[k]) for k in ("delta", "gamma", "vega", "theta", "vanna", "volga"))
    assert abs(t["unexplained"]) < 0.05 * greek + 1000
    assert len(s.debriefs) == 10
    card = scorecard(s)
    assert card["rfqs"] > 0 and "fill_rate_pct" in card
    assert rule_based_review(s, card)
    assert any(e["kind"] == "day_end" for e in s.log)


def test_expiry_converts_itm_to_spot():
    b = Book()
    b.add("EURUSD", "option", 1e6, 1.10, expiry=0.01, cp="C", price_per_unit=0.01)
    b.add("EURUSD", "option", 1e6, 1.30, expiry=0.01, cp="C", price_per_unit=0.001)
    out = b.settle_expiries(0.02, {"EURUSD": 1.16})
    assert len(b.positions) == 1 and b.positions[0].kind == "spot" and b.positions[0].notional == 1e6
    assert b.positions[0].K == 1.10 and sum(o["itm"] for o in out) == 1


def test_client_decision_logic():
    r = RFQ(1, 0, 10, "EURUSD", "vanilla", "1M", 1e7, "corporate", 1, (), half_width_mult=1.0)
    assert client_decides(r, 6.9, 7.1, 7.0, 0.2)        # inside competition -> trades
    assert not client_decides(r, 6.9, 7.5, 7.0, 0.2)    # offer too high
    assert not client_decides(r, 7.2, 7.1, 7.0, 0.2)    # crossed
    r.client_side = -1
    assert client_decides(r, 6.9, 7.1, 7.0, 0.2) and not client_decides(r, 6.5, 7.1, 7.0, 0.2)


def test_quote_edge_sign():
    s = SimSession(21, 2, inherit=False)
    while not s.open_rfqs():
        s.step()
    r = s.open_rfqs()[0]
    fair, _, _ = metric_and_vega(r, s.mkt(r.pair))
    res = s.quote(r.id, fair - 0.01, fair + 0.01)
    if res["traded"]:
        assert s.trades[-1]["edge_usd"] > 0  # quoted around fair: small positive edge


def test_hedges_cost_money_and_flatten_delta():
    s = SimSession(8, 1, inherit=True)
    p = s.pairs[0]
    if abs(s.risk[p]["delta_base"]) > 2e5:
        res = s.delta_hedge(p)
        assert res["ok"]
        assert abs(s.risk[p]["delta_base"]) < 1e5
        assert s.total_terms["hedge_cost"] < 0
    s.idb_trade(p, "1M", "ATM", 1, 1e7, straddle=True)
    assert s.risk[p]["vega_usd"] != 0
