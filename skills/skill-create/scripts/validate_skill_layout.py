#!/usr/bin/env python3
"""Validate the repo-local required skill layout."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "STATE.md",
    "agents/openai.yaml",
    "references/example.md",
    "references/rules/env.md",
    "references/rules/filetree.md",
    "references/rules/state-rules.md",
    "references/template/STATE.template.md",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", type=Path)
    args = parser.parse_args()

    skill_dir = args.skill_dir
    errors: list[str] = []

    if not skill_dir.exists():
        errors.append(f"missing skill directory: {skill_dir}")
    elif not skill_dir.is_dir():
        errors.append(f"not a directory: {skill_dir}")

    for relative_path in REQUIRED_FILES:
        path = skill_dir / relative_path
        if not path.is_file():
            errors.append(f"missing required file: {relative_path}")

    skill_md = skill_dir / "SKILL.md"
    if skill_md.is_file():
        text = skill_md.read_text(encoding="utf-8")
        errors.extend(_validate_frontmatter(text))
        if "TODO" in text or "Replace this" in text:
            errors.append("SKILL.md still contains template placeholder text")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if openai_yaml.is_file():
        text = openai_yaml.read_text(encoding="utf-8")
        if "$" not in text or "default_prompt:" not in text:
            errors.append("agents/openai.yaml must include a default_prompt with the skill name")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Skill layout is valid: {skill_dir}")
    return 0


def _validate_frontmatter(text: str) -> list[str]:
    match = re.match(r"^---\n(?P<body>.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        return ["SKILL.md is missing YAML frontmatter"]

    body = match.group("body")
    errors = []
    if not re.search(r"^name:\s*[a-z0-9-]+\s*$", body, flags=re.MULTILINE):
        errors.append("SKILL.md frontmatter must include lowercase hyphenated name")
    if not re.search(r"^description:\s*\S", body, flags=re.MULTILINE):
        errors.append("SKILL.md frontmatter must include a non-empty description")
    return errors


if __name__ == "__main__":
    raise SystemExit(main())
