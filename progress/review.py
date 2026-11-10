"""Mixed review: draw questions from the weakest topics (Leitner weighted)."""
from __future__ import annotations

from typing import Callable

import numpy as np

from grading.question import Question
from progress.db import topic_weights


def pick_weighted(candidates: list[Question], section: str, rng: np.random.Generator) -> Question:
    """Choose one candidate with probability proportional to its topic weight."""
    w = topic_weights([q.topic for q in candidates], section)
    p = np.array([w[q.topic] for q in candidates], dtype=float)
    return candidates[int(rng.choice(len(candidates), p=p / p.sum()))]


def mixed_review(generators: list[Callable[[int, int], Question]], section: str, seed: int,
                 difficulty: int, n_candidates: int = 10) -> Question:
    """Generate candidates across subsections and pick one, favouring weak topics."""
    rng = np.random.default_rng(seed)
    cands = []
    for i in range(n_candidates):
        g = generators[i % len(generators)]
        try:
            cands.append(g(int(rng.integers(2**31 - 1)), difficulty))
        except Exception:
            continue
    return pick_weighted(cands, section, rng)
