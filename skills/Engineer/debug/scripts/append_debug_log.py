#!/usr/bin/env python3
"""Append a structured markdown entry to a debug log."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


def read_text_arg(value: str | None) -> str:
    if not value:
        return ""
    return value.strip()


def read_file_arg(path: str | None) -> str:
    if not path:
        return ""
    return Path(path).read_text(encoding="utf-8").strip()


def next_entry_number(existing: str) -> int:
    count = 0
    for line in existing.splitlines():
        if line.startswith("## Entry "):
            count += 1
    return count + 1


def bullet_block(label: str, body: str) -> str:
    body = body.strip()
    if not body:
        body = "None recorded."
    indented = "\n".join(f"  {line}" if line else "" for line in body.splitlines())
    return f"- {label}:\n{indented}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", required=True, help="Markdown debug log path")
    parser.add_argument("--title", required=True, help="Short entry title")
    parser.add_argument("--time", default="", help="Entry time; defaults to UTC now")
    parser.add_argument("--user-request", default="")
    parser.add_argument("--hypothesis", default="")
    parser.add_argument("--actions", default="")
    parser.add_argument("--actions-file", default="")
    parser.add_argument("--findings", default="")
    parser.add_argument("--findings-file", default="")
    parser.add_argument("--decision", default="")
    parser.add_argument("--next", default="")
    args = parser.parse_args()

    log_path = Path(args.log)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    existing = log_path.read_text(encoding="utf-8") if log_path.exists() else ""
    entry_no = next_entry_number(existing)
    timestamp = args.time or datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    actions = "\n".join(
        part for part in [read_text_arg(args.actions), read_file_arg(args.actions_file)] if part
    )
    findings = "\n".join(
        part for part in [read_text_arg(args.findings), read_file_arg(args.findings_file)] if part
    )

    entry = "\n".join(
        [
            f"## Entry {entry_no} - {args.title}",
            "",
            f"- Time: {timestamp}",
            f"- User request: {read_text_arg(args.user_request) or 'None recorded.'}",
            f"- Working hypothesis: {read_text_arg(args.hypothesis) or 'None recorded.'}",
            bullet_block("Actions", actions),
            bullet_block("Findings", findings),
            f"- Decision: {read_text_arg(args.decision) or 'None recorded.'}",
            f"- Next: {read_text_arg(args.next) or 'None recorded.'}",
            "",
        ]
    )

    prefix = "" if not existing or existing.endswith("\n") else "\n"
    log_path.write_text(existing + prefix + entry, encoding="utf-8")
    print(log_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
