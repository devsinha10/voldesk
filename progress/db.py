"""SQLite storage: question attempts, Leitner boxes, simulator sessions/events."""
from __future__ import annotations

import json
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator, Optional

from engine.config import data_path, load_config

SCHEMA = """
CREATE TABLE IF NOT EXISTS attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts REAL NOT NULL,
    section TEXT NOT NULL,
    subsection TEXT NOT NULL,
    topic TEXT NOT NULL,
    difficulty INTEGER NOT NULL,
    question_id TEXT NOT NULL,
    template TEXT,
    seed INTEGER,
    auto_score REAL,
    llm_score REAL,
    final_score REAL NOT NULL,
    correct INTEGER NOT NULL,
    answer_json TEXT,
    feedback_json TEXT
);
CREATE INDEX IF NOT EXISTS idx_attempts_topic ON attempts(topic);
CREATE TABLE IF NOT EXISTS leitner (
    topic TEXT PRIMARY KEY,
    section TEXT NOT NULL,
    box INTEGER NOT NULL DEFAULT 1,
    last_ts REAL,
    seen INTEGER NOT NULL DEFAULT 0,
    correct INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS sim_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts REAL NOT NULL,
    seed INTEGER NOT NULL,
    level INTEGER NOT NULL,
    regime TEXT,
    pairs TEXT,
    total_pnl_usd REAL,
    scorecard_json TEXT,
    review_text TEXT,
    finished INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS sim_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    t REAL NOT NULL,
    kind TEXT NOT NULL,
    payload_json TEXT
);
CREATE INDEX IF NOT EXISTS idx_events_session ON sim_events(session_id);
"""

N_BOXES = 5


def db_path() -> Path:
    return data_path(load_config()["storage"]["progress_db"])


@contextmanager
def connect(path: Optional[Path] = None) -> Iterator[sqlite3.Connection]:
    """Connection with the schema ensured. Commits on success."""
    con = sqlite3.connect(str(path or db_path()))
    con.row_factory = sqlite3.Row
    try:
        con.executescript(SCHEMA)
        yield con
        con.commit()
    finally:
        con.close()


# ---------------------------------------------------------------------------
# Attempts + Leitner
# ---------------------------------------------------------------------------
def log_attempt(section: str, subsection: str, topic: str, difficulty: int, question_id: str,
                final_score: float, auto_score: Optional[float] = None,
                llm_score: Optional[float] = None, answer: Any = None, feedback: Any = None,
                template: str = "", seed: Optional[int] = None, pass_mark: float = 7.0,
                path: Optional[Path] = None) -> bool:
    """Store an attempt and update that topic's Leitner box. Returns ``correct``."""
    correct = final_score >= pass_mark
    now = time.time()
    with connect(path) as con:
        con.execute(
            "INSERT INTO attempts (ts, section, subsection, topic, difficulty, question_id, template,"
            " seed, auto_score, llm_score, final_score, correct, answer_json, feedback_json)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (now, section, subsection, topic, difficulty, question_id, template, seed, auto_score,
             llm_score, final_score, int(correct), json.dumps(answer, default=str),
             json.dumps(feedback, default=str)))
        row = con.execute("SELECT box, seen, correct FROM leitner WHERE topic=?", (topic,)).fetchone()
        if row is None:
            box = 2 if correct else 1
            con.execute("INSERT INTO leitner (topic, section, box, last_ts, seen, correct) VALUES (?,?,?,?,?,?)",
                        (topic, section, box, now, 1, int(correct)))
        else:
            box = min(row["box"] + 1, N_BOXES) if correct else 1
            con.execute("UPDATE leitner SET box=?, last_ts=?, seen=?, correct=? WHERE topic=?",
                        (box, now, row["seen"] + 1, row["correct"] + int(correct), topic))
    return correct


def leitner_table(section: Optional[str] = None, path: Optional[Path] = None) -> list[dict]:
    with connect(path) as con:
        q = "SELECT * FROM leitner" + (" WHERE section=?" if section else "") + " ORDER BY box, topic"
        rows = con.execute(q, (section,) if section else ()).fetchall()
    return [dict(r) for r in rows]


def topic_weights(topics: list[str], section: Optional[str] = None,
                  path: Optional[Path] = None) -> dict[str, float]:
    """Sampling weight per topic: unseen topics weight 4, then 2^(N_BOXES - box)
    so box 1 (weak) comes back 16x as often as box 5 (mastered). Topics not
    seen for a while get a small boost."""
    boxes = {r["topic"]: r for r in leitner_table(section, path)}
    now = time.time()
    out = {}
    for t in topics:
        r = boxes.get(t)
        if r is None:
            out[t] = 4.0
        else:
            stale_days = (now - (r["last_ts"] or now)) / 86400
            out[t] = 2.0 ** (N_BOXES - r["box"]) * (1 + min(stale_days, 14) / 7)
    return out


def weakest_topics(n: int = 5, section: Optional[str] = None, path: Optional[Path] = None) -> list[dict]:
    rows = [r for r in leitner_table(section, path) if r["seen"] > 0]
    rows.sort(key=lambda r: (r["box"], r["correct"] / max(r["seen"], 1)))
    return rows[:n]


def attempts(section: Optional[str] = None, subsection_prefix: Optional[str] = None,
             limit: int = 1000, path: Optional[Path] = None) -> list[dict]:
    q, args = "SELECT * FROM attempts WHERE 1=1", []
    if section:
        q += " AND section=?"
        args.append(section)
    if subsection_prefix:
        q += " AND subsection LIKE ?"
        args.append(subsection_prefix + "%")
    q += " ORDER BY ts DESC LIMIT ?"
    args.append(limit)
    with connect(path) as con:
        return [dict(r) for r in con.execute(q, args).fetchall()]


def stage_stats(subsection: str, path: Optional[Path] = None) -> dict[str, float]:
    with connect(path) as con:
        r = con.execute("SELECT COUNT(*) n, AVG(final_score) avg FROM attempts WHERE subsection=?",
                        (subsection,)).fetchone()
    return {"n": r["n"] or 0, "avg": r["avg"] or 0.0}


# ---------------------------------------------------------------------------
# Simulator sessions
# ---------------------------------------------------------------------------
def create_session(seed: int, level: int, regime: str, pairs: list[str],
                   path: Optional[Path] = None) -> int:
    with connect(path) as con:
        cur = con.execute("INSERT INTO sim_sessions (ts, seed, level, regime, pairs) VALUES (?,?,?,?,?)",
                          (time.time(), seed, level, regime, json.dumps(pairs)))
        return int(cur.lastrowid)


def log_events(session_id: int, events: list[dict], path: Optional[Path] = None) -> None:
    if not events:
        return
    with connect(path) as con:
        con.executemany("INSERT INTO sim_events (session_id, t, kind, payload_json) VALUES (?,?,?,?)",
                        [(session_id, e.get("t", 0.0), e.get("kind", ""), json.dumps(e, default=str))
                         for e in events])


def finish_session(session_id: int, total_pnl: float, scorecard: dict, review: str = "",
                   path: Optional[Path] = None) -> None:
    with connect(path) as con:
        con.execute("UPDATE sim_sessions SET total_pnl_usd=?, scorecard_json=?, review_text=?, finished=1"
                    " WHERE id=?", (total_pnl, json.dumps(scorecard, default=str), review, session_id))


def update_review(session_id: int, review: str, path: Optional[Path] = None) -> None:
    with connect(path) as con:
        con.execute("UPDATE sim_sessions SET review_text=? WHERE id=?", (review, session_id))


def sessions(limit: int = 50, path: Optional[Path] = None) -> list[dict]:
    with connect(path) as con:
        return [dict(r) for r in con.execute(
            "SELECT * FROM sim_sessions ORDER BY ts DESC LIMIT ?", (limit,)).fetchall()]


def session_events(session_id: int, path: Optional[Path] = None) -> list[dict]:
    with connect(path) as con:
        rows = con.execute("SELECT payload_json FROM sim_events WHERE session_id=? ORDER BY id",
                           (session_id,)).fetchall()
    return [json.loads(r["payload_json"]) for r in rows]
