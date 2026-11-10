"""Section 1: options interview prep generators."""
from prep_options import concepts, exposures, greek_drills

SUBSECTIONS = {
    "1A": ("Greek drills (quickfire)", greek_drills.generate),
    "1B": ("Write your Greek exposures", exposures.generate),
    "1C": ("Concepts and trade expression", concepts.generate),
}


def generate(subsection: str, seed: int, difficulty: int):
    return SUBSECTIONS[subsection][1](seed, difficulty)
