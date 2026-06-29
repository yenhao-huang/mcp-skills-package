# Filetree Rules

Use this reference before adding, moving, or removing files in this skill.

## Required Layout

```text
set-daily-cron/
├── SKILL.md
├── STATE.md
└── references/
    ├── cron-config.md
    ├── example.md
    ├── tasks/
    │   └── <task-name>/
    │       ├── task.py
    │       ├── config.json
    │       ├── state.json
    │       └── reports/
    ├── rules/
    │   ├── env.md
    │   ├── filetree.md
    │   └── state-rules.md
    └── template/
        └── STATE.template.md
```

## Placement Rules

- `SKILL.md`: Required skill entry point. Keep trigger conditions, core
  workflow, and short rules here.
- `STATE.md`: Per-run working state.
- `references/cron-config.md`: Cron state contract, task schema, and validation
  commands.
- `references/example.md`: Common user requests and expected handling.
- `references/tasks/<task-name>/`: Self-contained task implementation,
  config, mutable state, and generated reports.
- `references/rules/`: Reusable operating rules.
- `references/template/`: Copyable templates.

## Cleanup Rules

- Do not add README, changelog, quick reference, or installation guide files.
- Store generated reports only under the owning
  `references/tasks/<task-name>/reports/` directory.
- Do not create `.agents` paths for cron state or reports.
