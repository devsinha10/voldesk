"""Config loading and seeded RNG helpers."""
from __future__ import annotations

import os
import secrets
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = Path(os.environ.get("VOLDESK_CONFIG", ROOT / "config.yaml"))


@lru_cache(maxsize=1)
def load_config(path: str | None = None) -> dict[str, Any]:
    """Load ``config.yaml`` once and cache it."""
    p = Path(path) if path else CONFIG_PATH
    with open(p, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def reload_config() -> dict[str, Any]:
    """Clear the cache and reload (used after editing config in the UI)."""
    load_config.cache_clear()
    return load_config()


def new_seed() -> int:
    """A fresh random 32-bit seed (logged by callers so sessions can be replayed)."""
    return secrets.randbelow(2**31 - 1)


def make_rng(seed: int) -> np.random.Generator:
    """Seeded NumPy generator."""
    return np.random.default_rng(seed)


def data_path(rel: str) -> Path:
    """Resolve a path relative to the project root, creating the parent folder."""
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    return p
