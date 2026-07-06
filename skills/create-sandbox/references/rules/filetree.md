# Filetree Rules

Use this reference before adding, moving, or removing files in the
`create-sandbox` skill directory.

## Layout

```text
create-sandbox/
├── SKILL.md
├── STATE.md
├── references/
│   ├── tools.md
│   ├── rules/
│   │   ├── env.md
│   │   ├── filetree.md
│   │   ├── lifecycle.md
│   │   ├── mounts.md
│   │   ├── runtime-mount-permissions.md
│   │   ├── service-tests.md
│   │   └── state-rules.md
│   └── template/
│       └── STATE.template.md
└── src/
    ├── Dockerfile
    ├── after_create_container.sh
    ├── build_and_exec.sh
    └── test_service.sh
```

## Placement Rules

- `SKILL.md`: Required entry point. Keep trigger conditions, core workflow, and
  short rules here.
- `STATE.md`: Per-run working state.
- `references/rules/`: Detailed operating rules loaded only when relevant.
- `references/template/`: Copyable templates.
- `src/`: Deterministic executable templates and scripts used by the workflow.

## Cleanup Rules

- Do not add README, changelog, quick reference, or installation guide files
  unless the user explicitly asks for user-facing documentation.
- Remove generated files such as `__pycache__/` before finishing.
- Keep references directly linked from `SKILL.md`.
