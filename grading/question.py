"""Question model shared by both interview-prep sections.

A question has auto-markable parts (MCQ, direction, sign table, numeric) and an
optional free-text part that Claude marks. Every number in ``facts`` and
``model_answer`` comes from the engine at generation time.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any, Optional

DIRECTIONS = ["Up", "Down", "Unchanged"]
SIGNS = ["+", "-", "0"]


@dataclass
class Part:
    """An auto-marked part.

    kind: 'mcq' | 'numeric' | 'sign_table'
    * mcq: ``options`` list, ``correct`` index
    * numeric: ``correct`` float, ``tol_abs`` / ``tol_rel`` tolerance, ``unit``
    * sign_table: ``rows`` (Greek names), ``correct`` dict row -> '+','-','0'
    """

    kind: str
    label: str
    options: list = field(default_factory=list)
    correct: Any = None
    tol_abs: float = 0.0
    tol_rel: float = 0.0
    unit: str = ""
    rows: list = field(default_factory=list)
    weight: float = 1.0
    explain: str = ""

    def mark(self, answer: Any) -> float:
        """Fraction correct in [0, 1]."""
        if answer is None:
            return 0.0
        if self.kind == "mcq":
            return 1.0 if answer == self.correct else 0.0
        if self.kind == "numeric":
            try:
                a = float(answer)
            except (TypeError, ValueError):
                return 0.0
            tol = max(self.tol_abs, self.tol_rel * abs(self.correct))
            if abs(a - self.correct) <= tol:
                return 1.0
            if abs(a - self.correct) <= 2 * tol:
                return 0.5
            return 0.0
        if self.kind == "sign_table":
            if not self.rows:
                return 0.0
            ok = 0
            for r in self.rows:
                c = self.correct[r]
                ok += 1 if (answer.get(r) in c if isinstance(c, (list, tuple, set)) else answer.get(r) == c) else 0
            return ok / len(self.rows)
        raise ValueError(self.kind)

    def correct_display(self) -> str:
        if self.kind == "mcq":
            return str(self.options[self.correct])
        if self.kind == "numeric":
            return f"{self.correct:,.4g} {self.unit}".strip()
        if self.kind == "sign_table":
            fmt = lambda c: "/".join(c) if isinstance(c, (list, tuple, set)) else c
            return ", ".join(f"{r}: {fmt(self.correct[r])}" for r in self.rows)
        return str(self.correct)


@dataclass
class Question:
    """A generated interview question with its engine-derived ground truth."""

    section: str            # 'options' | 'rates'
    subsection: str         # e.g. '1A', '1B', '2A-3'
    topic: str              # tag used for spaced repetition
    difficulty: int
    template: str
    seed: int
    prompt: str
    parts: list[Part] = field(default_factory=list)
    free_text_prompt: Optional[str] = None
    facts: dict = field(default_factory=dict)
    model_answer: str = ""
    rubric: list[str] = field(default_factory=list)
    charts: list[dict] = field(default_factory=list)
    tables: list[dict] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    @property
    def qid(self) -> str:
        h = hashlib.sha1(f"{self.template}|{self.seed}|{self.difficulty}|{self.prompt}".encode()).hexdigest()
        return h[:12]

    def auto_score(self, answers: dict[int, Any]) -> Optional[float]:
        """Weighted auto score out of 10, or None if no auto parts."""
        if not self.parts:
            return None
        w = sum(p.weight for p in self.parts)
        return 10.0 * sum(p.weight * p.mark(answers.get(i)) for i, p in enumerate(self.parts)) / w

    def to_json(self) -> str:
        return json.dumps(asdict(self), default=str)


def combine_scores(auto: Optional[float], llm: Optional[float], auto_weight: float = 0.5) -> float:
    """Blend the auto score and the free-text score (out of 10)."""
    if auto is None and llm is None:
        return 0.0
    if auto is None:
        return float(llm)
    if llm is None:
        return float(auto)
    return auto_weight * auto + (1 - auto_weight) * llm


def chart_line(title: str, x: list, series: dict[str, list], xlabel: str, ylabel: str,
               vline: Optional[float] = None, vline_label: str = "") -> dict:
    """Serializable line-chart spec rendered by the UI with Plotly."""
    return {"type": "line", "title": title, "x": list(map(float, x)),
            "series": {k: list(map(float, v)) for k, v in series.items()},
            "xlabel": xlabel, "ylabel": ylabel, "vline": vline, "vline_label": vline_label}


def chart_bar(title: str, labels: list[str], values: list[float], ylabel: str) -> dict:
    return {"type": "bar", "title": title, "labels": labels, "values": list(map(float, values)),
            "ylabel": ylabel}
