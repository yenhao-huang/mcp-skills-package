#!/usr/bin/env python3
"""Legacy, non-blocking session context diagnostic.

The script supports both Codex JSONL session files and Claude transcript JSONL
files. Codex performs automatic compaction natively; this diagnostic always
exits successfully so a stale hook registration cannot block a prompt.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

DEFAULT_LIMIT = 300_000


def token_limit() -> int:
    raw = (
        os.environ.get("CODEX_SESSION_TOKEN_LIMIT")
        or os.environ.get("COMPACT_THRESHOLD")
        or str(DEFAULT_LIMIT)
    )
    try:
        limit = int(raw)
    except ValueError:
        print(f"invalid token limit {raw!r}; using {DEFAULT_LIMIT}", file=sys.stderr)
        return DEFAULT_LIMIT
    return max(limit, 0)


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser()


def session_candidates(root: Path) -> list[Path]:
    sessions = root / "sessions"
    if not sessions.is_dir():
        return []
    return sorted(
        (path for path in sessions.rglob("*.jsonl") if path.is_file()),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )


def path_from_stdin() -> Path | None:
    if sys.stdin.isatty():
        return None
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return None
    for key in ("session_path", "transcript_path", "history_path"):
        value = payload.get(key)
        if value:
            return Path(value).expanduser()
    return None


def codex_context_tokens(info: dict[str, Any]) -> int | None:
    """Return the latest request's input context, not cumulative session use."""
    usage = info.get("last_token_usage") or info
    for key in ("input_tokens", "total_tokens"):
        value = usage.get(key)
        if isinstance(value, int):
            return value
    return None


def claude_usage_total(usage: dict[str, Any]) -> int:
    return (
        int(usage.get("input_tokens") or 0)
        + int(usage.get("cache_creation_input_tokens") or 0)
        + int(usage.get("cache_read_input_tokens") or 0)
    )


def latest_token_count(session_file: Path) -> tuple[str, int] | None:
    latest_codex: int | None = None
    latest_claude: int | None = None
    if not session_file.is_file():
        return None

    with session_file.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            payload = event.get("payload") or {}
            if payload.get("type") == "token_count":
                total = codex_context_tokens(payload.get("info") or {})
                if total is not None and total > 0:
                    latest_codex = total
                continue

            usage = (event.get("message") or {}).get("usage")
            if usage:
                latest_claude = claude_usage_total(usage)

    if latest_codex is not None:
        return "Codex context", latest_codex
    if latest_claude is not None:
        return "Claude transcript", latest_claude
    return None


def newest_session_with_usage(paths: list[Path]) -> tuple[Path, str, int] | None:
    for path in paths:
        result = latest_token_count(path)
        if result is not None:
            source, total = result
            return path, source, total
    return None


def check(paths: list[Path], limit: int) -> int:
    result = newest_session_with_usage(paths)
    if result is None:
        return 0

    path, source, total = result
    if total <= limit:
        print(f"{source} token usage OK: {total:,} <= {limit:,}", file=sys.stderr)
        return 0

    print(
        (
            f"{source} token usage is {total:,}, above the {limit:,} diagnostic limit.\n"
            f"Session file: {path}\n"
            "Continuing because Codex native auto-compaction owns context limits."
        ),
        file=sys.stderr,
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--session-file",
        action="append",
        type=Path,
        help="JSONL session or transcript file to inspect. Can be passed more than once.",
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=codex_home(),
        help="Codex home directory containing sessions/.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=token_limit(),
        help="Maximum allowed session tokens.",
    )
    args = parser.parse_args()

    paths = [path.expanduser() for path in args.session_file or []]
    stdin_path = path_from_stdin()
    if stdin_path is not None:
        paths.insert(0, stdin_path)
    if not paths:
        paths = session_candidates(args.codex_home.expanduser())

    return check(paths, max(args.limit, 0))


if __name__ == "__main__":
    raise SystemExit(main())
