"""python -m tools.audit_levels  ->  audit/levels_sample.md

Prints 10 sample questions per sub-section per level, with the Givens, the
auto-marked answers and the model answers, so the step-up between levels can be
checked by eye.
"""
from __future__ import annotations

from pathlib import Path

from grading.question import render_givens
from tools.common import SECTIONS, seeds

OUT = Path(__file__).resolve().parent.parent / "audit" / "levels_sample.md"
LEVEL_DEF = {1: "Level 1: directional intuition, no calculations",
             2: "Level 2: combinations, light calculations with every input given",
             3: "Level 3: calculations plus subtler concepts"}


def _answer(p) -> str:
    return p.correct_display()


def main(n: int = 10) -> Path:
    lines = ["# VolDesk level audit: sample questions", "",
             f"{n} questions per sub-section per level. Seeds are deterministic, so re-running gives the same file.", ""]
    for section, title, subs in SECTIONS:
        lines += [f"# {title}", ""]
        for code, (name, gen) in subs.items():
            lines += [f"## {code} {name}", ""]
            for lvl in (1, 2, 3):
                lines += [f"### {LEVEL_DEF[lvl]}", ""]
                for i, s in enumerate(seeds(code, lvl, n), 1):
                    q = gen(s, lvl)
                    lines += [f"**Q{i}** (`{q.template}`, topic `{q.topic}`, seed {q.seed})", "", q.prompt, ""]
                    g = render_givens(q)
                    if g:
                        lines += ["Givens:", "", g, ""]
                    for p in q.parts:
                        lines.append(f"- *{p.label}*: **{_answer(p)}**")
                    if q.free_text_prompt:
                        lines.append(f"- *Written*: {q.free_text_prompt}")
                    lines += ["", "<details><summary>Model answer</summary>", "", q.model_answer, "", "</details>", ""]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    return OUT


if __name__ == "__main__":
    print(f"wrote {main()}")
