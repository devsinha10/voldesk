"""Level structure, Givens enforcement, 1A coverage matrices and level progress."""
import sqlite3
import types
import warnings

import numpy as np
import pytest

import prep_options as po
import prep_rates as pr
from grading.question import RecordingMapping, render_givens, fmt_given
from prep_options import greek_matrix as gm
from progress import db

warnings.filterwarnings("ignore")

ALL = [("options", code, gen) for code, (_, gen) in po.SUBSECTIONS.items()] + \
      [("rates", code, gen) for code, (_, gen) in pr.SUBSECTIONS.items()]
N_PER = 20


def _questions(level):
    for section, code, gen in ALL:
        for k in range(N_PER):
            yield section, code, gen(10_000 * level + 37 * k + 1, level)


@pytest.mark.parametrize("level", [1, 2, 3])
def test_solvers_use_only_displayed_givens(level):
    """Every numeric answer = solver(givens); the solver reads only givens, and every given is shown."""
    checked = 0
    for section, code, q in _questions(level):
        nparts = q.numeric_parts()
        if not nparts:
            continue
        assert q.solver is not None and q.givens, f"{code} {q.template}: numeric part without givens/solver"
        # the solver must not close over numbers: only givens may carry inputs
        for cell in (q.solver.__closure__ or ()):
            v = cell.cell_contents
            assert not isinstance(v, (int, float, np.number, list, dict, tuple)), \
                f"{code} {q.template}: solver captures {v!r} outside its givens"
        rec = RecordingMapping(q.givens)
        out = list(q.solver(rec))
        assert len(out) == len(nparts)
        for p, a in zip(nparts, out):
            assert a == pytest.approx(p.correct, rel=1e-12, abs=1e-12), f"{code} {q.template}"
        assert rec.used <= set(q.givens), f"{code} {q.template}: solver read unknown keys"
        assert set(q.given_labels) >= set(q.givens), f"{code} {q.template}: given without a label"
        shown = render_givens(q)
        for k in rec.used:
            assert q.given_labels[k] in shown and fmt_given(q.givens[k]) in shown, f"{code} {q.template}: {k} not displayed"
        checked += 1
    if level > 1:
        assert checked > 0


def test_level1_has_no_calculations():
    for section, code, q in _questions(1):
        assert not q.numeric_parts(), f"{code} {q.template} asks for a number at Level 1"
        assert q.difficulty == 1


@pytest.mark.parametrize("level", [1, 2, 3])
def test_every_subsection_generates_at_every_level(level):
    for section, code, gen in ALL:
        q = gen(level * 991 + 7, level)
        assert q.subsection == code and q.difficulty == level and q.model_answer and q.rubric


def test_level3_has_numbers_in_calculation_sections():
    """Level 3 is where calculations live: most sub-sections ask for at least one number."""
    with_numbers = {code for section, code, q in _questions(3) if q.numeric_parts()}
    expected = {"1A", "1B", "1C", "2A-1", "2A-2", "2A-3", "2A-4", "2A-5", "2B", "2C", "2D", "2E", "2F"}
    assert expected <= with_numbers


def test_levels_differ_in_templates():
    for section, code, gen in ALL:
        t = {lvl: {gen(lvl * 1000 + k, lvl).template for k in range(12)} for lvl in (1, 2, 3)}
        assert t[1].isdisjoint(t[3]), f"{code}: same templates at Level 1 and Level 3"


# ---------------------------------------------------------------------------
# 1A coverage matrices
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("level", [1, 2])
def test_every_matrix_cell_is_producible(level):
    cells = gm.all_cells(level)
    assert len(cells) == 5 * 3 * 2 * 2 * 3 * 2
    missing = [c for i, c in enumerate(cells) if gm.find_conditions(c, np.random.default_rng(i), tries=60) is None]
    assert not missing, missing


def test_matrix_samples_uncovered_cells_first():
    cells = gm.all_cells(1)
    target = cells[123]
    covered = set(cells) - {target}
    q = gm.matrix_question(5, 1, covered)
    assert q.coverage_cell == ("1A-L1", target)


@pytest.mark.parametrize("seed", range(12))
def test_matrix_answer_matches_engine_for_small_and_large_shock(seed):
    q = gm.matrix_question(seed, 1 + seed % 2)
    cell = q.facts["cell"]
    g = cell.split("|")[0]
    b, a, a_small = q.facts["before"], q.facts["after"], q.facts["after_small_shock"]
    correct = q.parts[1].correct
    if correct == 2:  # robustly flat
        assert abs(a - b) < 0.015 * max(abs(b), 1e-9) or g in gm.L2_GREEKS
        return
    up = correct == 0
    if g in gm.L1_GREEKS:
        assert (abs(a) > abs(b)) == up and (abs(a_small) > abs(b)) == up
    else:
        assert (a > b) == up and (a_small > b) == up
    assert "depends" not in " ".join(q.parts[1].options).lower()


def test_matrix_question_states_conditions():
    q = gm.matrix_question(42, 1)
    for word in ("strike", "spot", "notional"):
        assert word in q.prompt
    assert any(m in q.prompt for m in ("ATM", "ITM", "OTM"))


# ---------------------------------------------------------------------------
# Level progress storage
# ---------------------------------------------------------------------------
def test_level_pass_rule_and_recommendation(tmp_path):
    p = tmp_path / "t.sqlite"
    for i in range(20):
        db.log_attempt("options", "1A", "t", 1, f"q{i}", 9.0 if i % 10 else 3.0, path=p)  # 18/20 correct
    for i in range(5):
        db.log_attempt("options", "1A", "t", 2, f"r{i}", 9.0, path=p)
    st = db.level_stats("options", path=p)
    l1 = [x for x in st if x["level"] == 1][0]
    l2 = [x for x in st if x["level"] == 2][0]
    assert l1["passed"] and l1["accuracy"] == pytest.approx(0.9)
    assert not l2["passed"]  # 100% but only 5 of the 20 needed
    assert db.recommended_level(st, "options", "1A") == 2
    tr = db.level_trend("options", path=p)
    assert len(tr[1]) == 20 and 0 <= min(tr[1]) <= max(tr[1]) <= 1


def test_old_attempts_excluded_from_levels(tmp_path):
    p = tmp_path / "t.sqlite"
    db.log_attempt("rates", "2B", "t", 1, "q", 9.0, path=p, version=1)
    assert db.level_stats(path=p) == []


def test_coverage_logged(tmp_path):
    p = tmp_path / "t.sqlite"
    db.log_attempt("options", "1A", "t", 1, "q", 9.0, path=p, coverage_cell=("1A-L1", "delta|spot|up|C|ATM|long"))
    db.log_attempt("options", "1A", "t", 1, "q", 2.0, path=p, coverage_cell=("1A-L1", "delta|spot|up|C|ATM|long"))
    cov = db.covered_cells("1A-L1", path=p)
    assert cov["delta|spot|up|C|ATM|long"] == {"seen": 2, "correct": 1}


def test_v1_database_is_migrated(tmp_path):
    p = tmp_path / "old.sqlite"
    con = sqlite3.connect(p)
    con.execute("CREATE TABLE attempts (id INTEGER PRIMARY KEY AUTOINCREMENT, ts REAL NOT NULL, section TEXT NOT NULL,"
                " subsection TEXT NOT NULL, topic TEXT NOT NULL, difficulty INTEGER NOT NULL, question_id TEXT NOT NULL,"
                " template TEXT, seed INTEGER, auto_score REAL, llm_score REAL, final_score REAL NOT NULL,"
                " correct INTEGER NOT NULL, answer_json TEXT, feedback_json TEXT)")
    con.execute("INSERT INTO attempts (ts, section, subsection, topic, difficulty, question_id, final_score, correct)"
                " VALUES (1, 'options', '1A', 't', 1, 'q', 9, 1)")
    con.commit(); con.close()
    db.log_attempt("options", "1A", "t", 1, "q2", 9.0, path=p)
    rows = db.attempts(path=p)
    assert {r["version"] for r in rows} == {1, 2}


def test_no_spec_topic_has_disappeared():
    from tools.topic_coverage import coverage
    missing = [(s, t) for s, t, lv in coverage(40) if not lv]
    assert not missing, missing
