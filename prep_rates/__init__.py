"""Section 2: rates interview prep generators and the 2A unlock rules."""
from prep_rates import duration_stages, topics

SUBSECTIONS = {code: (title, duration_stages.make_generator(code))
               for code, (title, _) in duration_stages.STAGES.items()}
SUBSECTIONS.update({code: (title, topics.make_generator(code)) for code, (title, _) in topics.TOPICS.items()})

UNLOCK_MIN_ATTEMPTS = 3
UNLOCK_MIN_AVG = 6.0


def locked_stages(stats_fn, unlock_all: bool = False) -> dict[str, str]:
    """Stages of 2A still locked. ``stats_fn(code)`` returns {'n', 'avg'}.

    Stage k unlocks once stage k-1 has >= 3 attempts averaging >= 6/10.
    """
    if unlock_all:
        return {}
    codes = list(duration_stages.STAGES)
    locked = {}
    for prev, code in zip(codes, codes[1:]):
        s = stats_fn(prev)
        if prev in locked or s["n"] < UNLOCK_MIN_ATTEMPTS or s["avg"] < UNLOCK_MIN_AVG:
            locked[code] = (f"{code} unlocks after {UNLOCK_MIN_ATTEMPTS}+ attempts on {prev} averaging "
                            f"{UNLOCK_MIN_AVG:.0f}/10 (now {s['n']} attempts, avg {s['avg']:.1f}). "
                            f"Or tick 'Unlock all stages' in the sidebar.")
    return locked


def generate(subsection: str, seed: int, difficulty: int):
    return SUBSECTIONS[subsection][1](seed, difficulty)
