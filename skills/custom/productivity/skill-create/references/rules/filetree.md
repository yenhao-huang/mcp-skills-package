# Filetree Rules

Use this reference before adding, moving, or removing files in a skill
directory.

## Required Layout

```text
skills/<category>/<skill-name>/
├── SKILL.md
├── STATE.md
└── references/
    ├── rules/
    │   ├── env.md
    │   ├── filetree.md
    │   └── state-rules.md
    ├── scripts/                       # optional skill executable code
    │   └── <tool>.py
    └── template/
        └── STATE.template.md
```

`custom` may use one extra subcategory level:

```text
skills/custom/<subcategory>/<skill-name>/
```

The files shown without an "optional" comment are required for every new
repo-local skill.

## Placement Rules

- `SKILL.md`: Required skill entry point. Keep trigger conditions, core
  workflow, and short rules here.
- `skills/<category>/`: Business-function category selected from
  `references/rules/categories.md`.
- `skills/custom/<subcategory>/`: Optional subcategory for internal or
  user-specific skills, such as `productivity` or `wingene`.
- `STATE.md`: Per-run working state. Keep it at the skill root so it is easy to
  find and update.
- `references/rules/`: Reusable operating rules, such as state handling and
  filetree conventions. `env.md`, `filetree.md`, and `state-rules.md` are
  required.
- `references/scripts/`: Executable code needed by the skill. Add this only
  when the skill has reusable helper code that belongs with the skill's
  references.
- `references/template/`: Copyable templates, such as `STATE.template.md`.
- `assets/`: Output assets or templates consumed by the task. Add only when the
  skill needs non-reference files such as images, fonts, or boilerplate.

## Validation Rules

Run generic skill validation before claiming a skill is complete:

```bash
python /home/howard/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-dir>
```

If the generic validator is unavailable because dependencies such as PyYAML are
missing, use the repository virtual environment or report the blocker.

Also inspect the skill directory against this file and
`references/rules/categories.md`:

- The path must be `skills/<category>/<skill-name>/`, except `custom` may use
  `skills/custom/<subcategory>/<skill-name>/`.
- The category must be one of the approved categories.
- Required Markdown files must be present.

## Cleanup Rules

- Do not add README, changelog, quick reference, or installation guide files
  unless the user explicitly asks for user-facing documentation.
- Do not add `agents/` or top-level `scripts/` to repo-local skill directories
  unless a separate repository rule explicitly introduces them.
- Remove generated files such as `__pycache__/` before finishing.
- Keep references one level deep where possible; avoid nested reference chains
  unless the organization materially improves discoverability.
