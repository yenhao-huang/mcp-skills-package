# Filetree rules

- `SKILL.md`: triggers, ordered workflow and resource entry points.
- `STATE.md`: current run, initialized from the state template.
- `references/guide.md`: adapted upstream guide and selective technical index.
- `references/rules/`: operating rules and upstream technical guidance.
- `references/audiences/`, `references/domains/`: profiles indexed by profiles.md.
- `references/scripts/`: reusable rendering, audit and safety helpers.
- `references/template/`: copyable Python starters and STATE.template.md.
- `assets/designing-math/`: upstream-rendered example PNGs.
- `references/SOURCE.md`, `references/LICENSE`: provenance and attribution.

Keep generated scenes, videos, audio, frames and environment files in the user's
project, outside this skill. Resolve Markdown links from their containing file;
resolve workflow resource paths from the skill root. Keep `style.py` beside copied
scene templates so imports work in both categorized and flat installations.
