# Environment rules

Use the user's existing project environment, preferring its `.venv`; do not
install into the system Python or personal agent directories. Record the selected
interpreter and run these checks from the output project with that environment
active:

```bash
python --version
python -c 'import manim; print(manim.__version__)'
manim --version
```

Before using MathTex/Tex, check the project's LaTeX toolchain (`latex` and
`dvisvgm`). Text-only scenes do not require LaTeX. Check `ffmpeg -version` and
`ffprobe -version` before the audit or concatenation helpers. Their shell scripts
require Bash and common Unix tools; use a compatible shell on Windows.

If a required dependency is missing, record it as a blocker for the affected step
and report it before installing packages. Follow the project's existing dependency
setup policy; do not silently run the upstream tutorial's global pip commands.
Source and scene planning can proceed without claiming runtime validation.

The `3brown1blue` command in optional narration references belongs to the separate
upstream CLI. This package includes its skill resources, not the CLI or any model
service. Verify that CLI and requested provider are available before use. Keep
provider credentials out of source, logs, state and delivered artifacts.

Use a fresh project/output directory. Review existing files before copying
starters or running helpers, which may replace generated videos and audit frames.
Invoke helper paths relative to this installed skill, or copy them into the
project first; never assume a personal `.claude` or `.codex` installation path.
