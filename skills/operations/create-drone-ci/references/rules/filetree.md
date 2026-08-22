# Filetree Rules

Read this file before adding, moving, or removing files.

## Skill Package Layout

```text
skills/operations/create-drone-ci/
├── SKILL.md
├── STATE.md
└── references/
    ├── drone-conventions.md
    ├── validation.md
    ├── rules/
    │   ├── env.md
    │   ├── filetree.md
    │   └── state-rules.md
    ├── scripts/
    │   └── scaffold_drone_ci.py
    └── template/
        └── STATE.template.md
```

Do not add a README, changelog, `agents/`, or top-level `scripts/` directory to
this skill.

## Generated Repository Layout

```text
<repo>/
├── .drone.yml                    # canonical Drone pipeline entry point
└── .ci/
    ├── drone/
    │   ├── compose.yaml          # Drone Server and Docker Runner
    │   ├── .env.example          # committed variable names/placeholders
    │   ├── CONVENTIONS.md        # ownership, security, and operations rules
    │   ├── Dockerfile.server     # optional; only with --with-dockerfiles
    │   └── Dockerfile.runner     # optional; only with --with-dockerfiles
    ├── docs/
    │   └── pipeline.md           # CI task and trigger documentation
    ├── scripts/
    │   └── ci.sh                 # task entry point called by Drone
    └── tests/
        └── test_ci_smoke.py      # test for the task script/layout
```

## Placement Rules

- Keep `.drone.yml` at the root because Drone discovers that path by default.
- Keep only CI infrastructure and task support under `.ci/`.
- Put Server/Runner Compose, optional Dockerfiles, runtime examples, and
  operational conventions under `.ci/drone/`.
- Put explanations of workflows and triggers under `.ci/docs/`.
- Put deterministic CI task entry points under `.ci/scripts/`.
- Put tests for those scripts under `.ci/tests/`.
- Ignore `.ci/drone/.env`; commit `.ci/drone/.env.example`.
- Follow a target repository's stricter existing convention when it conflicts
  with this starter layout, and record the deviation in `STATE.md`.
