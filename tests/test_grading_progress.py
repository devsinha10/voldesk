import os

import pytest

from grading import llm
from grading.question import combine_scores
from progress import db
from progress.review import pick_weighted
import prep_options as po
import numpy as np


@pytest.fixture()
def tmpdb(tmp_path):
    return tmp_path / "t.sqlite"


def test_leitner_promotion_and_reset(tmpdb):
    for _ in range(3):
        db.log_attempt("options", "1A", "greeks:gamma", 1, "q", 9.0, path=tmpdb)
    row = [r for r in db.leitner_table(path=tmpdb) if r["topic"] == "greeks:gamma"][0]
    assert row["box"] == 4
    db.log_attempt("options", "1A", "greeks:gamma", 1, "q", 3.0, path=tmpdb)
    row = [r for r in db.leitner_table(path=tmpdb) if r["topic"] == "greeks:gamma"][0]
    assert row["box"] == 1 and row["seen"] == 4 and row["correct"] == 3


def test_weights_favour_weak_topics(tmpdb):
    db.log_attempt("options", "1A", "weak", 1, "q", 2.0, path=tmpdb)
    for _ in range(4):
        db.log_attempt("options", "1A", "strong", 1, "q", 10.0, path=tmpdb)
    w = db.topic_weights(["weak", "strong", "new"], path=tmpdb)
    assert w["weak"] > w["new"] > w["strong"]


def test_sim_session_roundtrip(tmpdb):
    sid = db.create_session(123, 1, "calm", ["EURUSD"], path=tmpdb)
    db.log_events(sid, [{"t": 0.0, "kind": "trade", "x": 1}], path=tmpdb)
    db.finish_session(sid, 1234.5, {"total": 1234.5}, "ok", path=tmpdb)
    assert db.session_events(sid, path=tmpdb)[0]["x"] == 1
    assert db.sessions(path=tmpdb)[0]["total_pnl_usd"] == 1234.5


def test_no_api_key_means_no_llm(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    assert llm.api_available() is False
    assert llm.grade_answer("q", "a", {}, []) is None
    assert llm.session_review([], {}) is None


def test_combine_scores():
    assert combine_scores(None, None) == 0.0
    assert combine_scores(8.0, None) == 8.0
    assert combine_scores(None, 6.0) == 6.0
    assert combine_scores(10.0, 6.0) == 8.0


def test_grade_schema_shape():
    s = llm.GRADE_SCHEMA
    assert set(s["required"]) == {"score", "correct_points", "missed_points", "errors", "model_answer"}
    assert s["additionalProperties"] is False


def test_cache_key_stable():
    assert llm.cache_key("a", {"x": 1, "y": 2}) == llm.cache_key("a", {"y": 2, "x": 1})


def test_mixed_review_pick(monkeypatch, tmpdb):
    monkeypatch.setattr(db, "db_path", lambda: tmpdb)
    qs = [po.generate("1A", s, 1) for s in range(5)]
    q = pick_weighted(qs, "options", np.random.default_rng(0))
    assert q in qs


def test_grade_answer_with_mocked_api(monkeypatch, tmp_path):
    import json as _json
    calls = []
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test")
    monkeypatch.setattr(llm, "load_config", lambda: {"llm": {"model": "m", "cache_db": str(tmp_path / "c.sqlite")}})
    monkeypatch.setattr(llm, "data_path", lambda rel: tmp_path / "c.sqlite")

    def fake_create(system, user, schema):
        calls.append(user)
        assert "ENGINE FACTS" in user and "<answer>" in user
        return _json.dumps({"score": 12, "correct_points": ["a"], "missed_points": [], "errors": [],
                            "model_answer": "x"})
    monkeypatch.setattr(llm, "_create", fake_create)
    r1 = llm.grade_answer("q", "my answer", {"vega": 1.0}, ["r"])
    r2 = llm.grade_answer("q", "my answer", {"vega": 1.0}, ["r"])
    assert r1["score"] == 10 and not r1["cached"]   # clipped to 0-10
    assert r2["cached"] and len(calls) == 1          # second call served from cache
