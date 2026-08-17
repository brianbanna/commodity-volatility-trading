"""Mechanical enforcement of the SPEC Part H rules that can be checked by a machine.

SPEC Part K names 3 refusal points and 1 of them, reimplementing the shared pricing
engine, is the failure mode most likely to happen quietly during a single afternoon of
work. These tests are the backstop for that and for the Part H rule 1 naming restriction.

They are heuristics, not proofs. Passing them is not permission; they exist so that the
obvious version of each violation cannot land silently.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Assembled at runtime so that this file, which has to search for the term, does not
# itself contain it. A plain text search of the repo must return nothing, including here.
RESTRICTED_TERMS: tuple[str, ...] = ("Car" + "gill",)

# Names that belong to statarb.pricing and must never be defined in this repo.
# SPEC Part H rule 2: imported, never reimplemented, never forked.
ENGINE_SYMBOLS: tuple[str, ...] = (
    "black76",
    "margrabe",
    "kirk",
    "bachelier",
    "implied_vol",
    "greeks",
    "delta",
    "gamma",
    "vega",
    "theta",
    "rho",
)

_DEF_PATTERN = re.compile(
    r"^\s*(?:def|class)\s+(" + "|".join(ENGINE_SYMBOLS) + r")\w*\s*[\(:]",
    re.IGNORECASE | re.MULTILINE,
)


def _tracked_files() -> list[Path]:
    """Every file git tracks, which is exactly the set that becomes public."""
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-files", "-z"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [REPO_ROOT / name for name in result.stdout.split("\0") if name]


def _read(path: Path) -> str | None:
    if not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None  # binary or unreadable; nothing to match on


def test_restricted_terms_absent_from_tracked_files() -> None:
    """SPEC Part H rule 1. No tracked file names the prior employer, in any casing."""
    offenders: list[str] = []
    for path in _tracked_files():
        text = _read(path)
        if text is None:
            continue
        lowered = text.lower()
        for term in RESTRICTED_TERMS:
            if term.lower() in lowered:
                offenders.append(f"{path.relative_to(REPO_ROOT)}: restricted term present")
    assert not offenders, "SPEC Part H rule 1 violated:\n" + "\n".join(offenders)


def test_pricing_engine_is_not_reimplemented() -> None:
    """SPEC Part H rule 2. No module defines a symbol that belongs to statarb.pricing.

    A missing payoff or Greek is an additive pull request to the engine package with its
    harness green, a tag bump, and a deliberate repin here. It is never a local definition.
    """
    offenders: list[str] = []
    for path in sorted((REPO_ROOT / "vol_trading").rglob("*.py")):
        text = _read(path)
        if text is None:
            continue
        for match in _DEF_PATTERN.finditer(text):
            line = text[: match.start()].count("\n") + 1
            offenders.append(
                f"{path.relative_to(REPO_ROOT)}:{line}: defines {match.group(1)!r}, "
                "which belongs to statarb.pricing"
            )
    assert not offenders, (
        "SPEC Part H rule 2 violated. The pricing engine is imported, never "
        "reimplemented, never forked:\n" + "\n".join(offenders)
    )
