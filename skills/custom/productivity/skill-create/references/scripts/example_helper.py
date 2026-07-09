"""Reference helper code for a create skill.

Files under references/scripts/ are executable code kept with the skill when
the skill needs reusable helpers.
"""

from __future__ import annotations


def normalize_step_name(name: str) -> str:
    """Return a stable state-table step key from a display name."""

    return " ".join(name.strip().split()).lower().replace(" ", "_")
