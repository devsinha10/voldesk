"""python -m tools.coverage_report  ->  audit/coverage_1A.md

Lists every cell of the 1A Level 1 and Level 2 matrices and confirms the
generator can produce it (with the engine-verified conditions and answer).
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

from prep_options import greek_matrix as gm

OUT = Path(__file__).resolve().parent.parent / "audit" / "coverage_1A.md"


def main() -> Path:
    lines = ["# 1A coverage matrices", "",
             "Cell = Greek | driver | direction | call/put | moneyness | long/short. 'Answer' is the engine-verified "
             "direction for the conditions found (same direction for a small and a large shock). L1 answers are about the "
             "SIZE of the Greek; L2 answers are signed.", ""]
    for lvl in (1, 2):
        cells = gm.all_cells(lvl)
        ok, rows = 0, []
        for i, c in enumerate(cells):
            r = gm.find_conditions(c, np.random.default_rng(i), tries=60)
            if r:
                ok += 1
                ans = "unchanged" if r["up"] is None else ("up" if r["up"] else "down")
                if lvl == 1 and r["up"] is not None:
                    ans = "grows in size" if r["up"] else "shrinks in size"
                md = "ATM" if r["mdelta"] is None else f"{int(r['mdelta']*100)}d"
                rows.append(f"| {c} | yes | {r['pair']} {r['tenor']} {md}, shock {r['size']} | {ans} |")
            else:
                rows.append(f"| {c} | **NO** | | |")
        flat = sum(1 for x in rows if x.endswith("| unchanged |"))
        lines += [f"## Level {lvl}: {ok}/{len(cells)} cells producible ({flat} resolve to 'roughly unchanged')", "",
                  "| Cell | Producible | Conditions found | Answer |", "|---|---|---|---|"] + rows + [""]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    return OUT


if __name__ == "__main__":
    print(f"wrote {main()}")
