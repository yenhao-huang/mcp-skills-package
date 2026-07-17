# Environment Rules

Primary language: Python and Markdown
Runtime version: Python 3.9 or newer
Package manager: None
Frameworks: Python standard library only
Service manager: None
Required services: None

- Run searches with `python3`; the bundled tools require no package install and
  no network service.
- Resolve the skill directory at runtime instead of assuming a global Codex or
  Claude installation path.
- Set `PYTHONDONTWRITEBYTECODE=1` when running the tools inside the maintained
  repository so they do not create `__pycache__` files.
- The scripts read only the CSV files under `references/data/` and write
  results to standard output.
- Do not install frontend dependencies or start a development service unless
  the target repository and user request require it.
