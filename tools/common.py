"""Shared helpers for the audit tools."""
from __future__ import annotations

import warnings
from collections import defaultdict

import prep_options as po
import prep_rates as pr

warnings.filterwarnings("ignore")

SECTIONS = [("options", "Section 1: Interview Prep (Options)", po.SUBSECTIONS),
            ("rates", "Section 2: Interview Prep (Rates)", pr.SUBSECTIONS)]


def seeds(code: str, level: int, n: int) -> list[int]:
    base = sum(ord(ch) for ch in code) * 7919 + level * 104729
    return [base + 31 * k for k in range(n)]


def sample(n: int = 40):
    """{(section, code, level): [questions]} with deterministic seeds."""
    out = defaultdict(list)
    for section, _, subs in SECTIONS:
        for code, (_, gen) in subs.items():
            for lvl in (1, 2, 3):
                for s in seeds(code, lvl, n):
                    out[(section, code, lvl)].append(gen(s, lvl))
    return out
