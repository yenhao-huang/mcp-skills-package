#!/usr/bin/env python3
"""Initialize Codex MCP config for Jina, Firecrawl, and Git."""

from __future__ import annotations

import argparse
import datetime as _dt
import os
from pathlib import Path
import re
import shutil
import sys
import tomllib


SERVER_NAMES = ("jina", "firecrawl", "git")


def default_config_path() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser() / "config.toml"
    return Path.home() / ".codex" / "config.toml"


def toml_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def toml_array(values: list[str]) -> str:
    return "[" + ", ".join(toml_string(value) for value in values) + "]"


def managed_blocks(git_repository: str | None) -> str:
    git_args = ["mcp-server-git"]
    if git_repository:
        git_args.extend(["--repository", str(Path(git_repository).expanduser())])

    blocks = [
        (
            "jina",
            [
                'url = "https://mcp.jina.ai/v1"',
                'bearer_token_env_var = "JINA_API_KEY"',
                "startup_timeout_sec = 120",
                "tool_timeout_sec = 600",
            ],
        ),
        (
            "firecrawl",
            [
                'command = "npx"',
                'args = ["-y", "firecrawl-mcp"]',
                "startup_timeout_sec = 120",
                "tool_timeout_sec = 600",
            ],
        ),
        (
            "git",
            [
                'command = "uvx"',
                f"args = {toml_array(git_args)}",
                "startup_timeout_sec = 120",
                "tool_timeout_sec = 600",
            ],
        ),
    ]

    rendered = []
    for name, lines in blocks:
        rendered.append(f"[mcp_servers.{name}]\n" + "\n".join(lines))
    return "\n\n".join(rendered) + "\n"


def remove_existing_blocks(text: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    skip = False
    managed_header = re.compile(r"^\[mcp_servers\.(" + "|".join(SERVER_NAMES) + r")\]$")
    any_header = re.compile(r"^\[.*\]$")

    for line in lines:
        if managed_header.match(line.strip()):
            skip = True
            continue
        if skip and any_header.match(line.strip()):
            skip = False
        if not skip:
            output.append(line)

    return "\n".join(output).rstrip() + "\n" if output else ""


def merge_config(existing: str, git_repository: str | None) -> str:
    base = remove_existing_blocks(existing).rstrip()
    blocks = managed_blocks(git_repository).rstrip()
    if base:
        return base + "\n\n" + blocks + "\n"
    return blocks + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=default_config_path())
    parser.add_argument("--git-repository", help="Optional repository path to bind Git MCP to.")
    parser.add_argument("--dry-run", action="store_true", help="Print merged config without writing.")
    parser.add_argument("--no-backup", action="store_true", help="Do not create a .bak file before writing.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = args.config.expanduser()
    existing = config_path.read_text() if config_path.exists() else ""
    merged = merge_config(existing, args.git_repository)

    try:
        tomllib.loads(merged)
    except tomllib.TOMLDecodeError as exc:
        print(f"Refusing to write invalid TOML: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        print(merged, end="")
        return 0

    config_path.parent.mkdir(parents=True, exist_ok=True)
    if config_path.exists() and not args.no_backup:
        timestamp = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = config_path.with_suffix(config_path.suffix + f".{timestamp}.bak")
        shutil.copy2(config_path, backup_path)
        print(f"Backup: {backup_path}")

    config_path.write_text(merged)
    print(f"Updated: {config_path}")
    print("Configured MCP servers: " + ", ".join(SERVER_NAMES))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
