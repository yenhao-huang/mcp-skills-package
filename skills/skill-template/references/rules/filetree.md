# Filetree Rules

Use this reference before adding, moving, or removing files in a skill
directory.

## Required Layout

```text
skill-name/
├── SKILL.md
├── STATE.md
└── references/
    ├── example.md
    ├── rules/
    │   ├── filetree.md
    │   └── state-rules.md
    ├── scripts/
    │   └── example_helper.py
    └── template/
        └── STATE.template.md
```

## Placement Rules

- `SKILL.md`: Required skill entry point. Keep trigger conditions, core
  workflow, and short rules here.
- `STATE.md`: Per-run working state. Keep it at the skill root so it is easy to
  find and update.
- `references/rules/`: Reusable operating rules, such as state handling and
  filetree conventions.
- `references/template/`: Copyable templates, such as `STATE.template.md`.
- `references/scripts/`: Reference code examples to read or adapt.
- `scripts/`: Deterministic executable tools used directly by the workflow.
  Add this directory only when the skill needs runnable helper scripts.
- `assets/`: Output assets or templates consumed by the task. Add only when the
  skill needs non-reference files such as images, fonts, or boilerplate.

## Cleanup Rules

- Do not add README, changelog, quick reference, or installation guide files
  unless the user explicitly asks for user-facing documentation.
- Remove generated files such as `__pycache__/` before finishing.
- Keep references one level deep where possible; avoid nested reference chains
  unless the organization materially improves discoverability.
