# Environment Rules

Use this reference before changing runtime assumptions for this skill.

## Runtime

Primary language: Python
Runtime version: Python 3 from `/usr/bin/python3`
Package manager: none
Frameworks: none
Service manager: none
Required services: none

## Rules

- Do not install packages for this skill.
- Use only Python standard library modules in `do-cron-tasks.py`.
- Run hook validation from the project root.
- Use `.codex/hooks/do-cron-tasks.py` as the active Codex hook.
- Treat `.codex/hooks.json` as the active hook registration file.
