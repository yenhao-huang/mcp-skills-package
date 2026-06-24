#!/usr/bin/env python3
"""UserPromptSubmit hook: warn when session context exceeds a token threshold.

Reads the current transcript JSONL, finds the most recent assistant turn's
usage (input_tokens + cache_creation + cache_read = current effective context
size), and if it exceeds THRESHOLD, emits an additionalContext payload telling
Claude (and the user) to run /compact.

Note: hooks cannot directly invoke /compact — that is a user-side slash
command. The strongest action a UserPromptSubmit hook can take is to BLOCK
the prompt with a reason (uncomment the BLOCK variant below to use that).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

THRESHOLD = int(os.environ.get("COMPACT_THRESHOLD", "500000"))
# Set HARD_BLOCK=1 to refuse new prompts until the user runs /compact.
HARD_BLOCK = os.environ.get("COMPACT_HARD_BLOCK") == "1"


def latest_usage(transcript: Path) -> dict | None:
    """Return the most recent assistant turn's usage dict, or None."""
    if not transcript.is_file():
        return None
    last = None
    with transcript.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            usage = (obj.get("message") or {}).get("usage")
            if usage:
                last = usage
    return last


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    transcript_path = payload.get("transcript_path")
    if not transcript_path:
        return 0

    usage = latest_usage(Path(transcript_path))
    if not usage:
        return 0

    total = (
        int(usage.get("input_tokens") or 0)
        + int(usage.get("cache_creation_input_tokens") or 0)
        + int(usage.get("cache_read_input_tokens") or 0)
    )

    if total <= THRESHOLD:
        return 0

    msg = (
        f"Session context size is {total:,} tokens, above the "
        f"{THRESHOLD:,} threshold. Stop and ask the user to run "
        f"`/compact` before doing further work — do not start new "
        f"tool calls or long edits until the conversation is compacted."
    )

    if HARD_BLOCK:
        json.dump(
            {"decision": "block", "reason": msg},
            sys.stdout,
        )
    else:
        json.dump(
            {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": msg,
                }
            },
            sys.stdout,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
