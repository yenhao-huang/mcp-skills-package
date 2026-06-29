"""Reference helper code for a create skill.

Files under references/scripts/ are examples to read or adapt. If a script is
intended to be executed directly by the skill workflow, put it in top-level
scripts/ instead.
"""

from __future__ import annotations


def normalize_step_name(name: str) -> str:
    """Return a stable state-table step key from a display name."""

    return " ".join(name.strip().split()).lower().replace(" ", "_")
