# Filetree Rules

Use this reference before adding, moving, or removing files in a skill
directory.

## Required Layout

```text
skills/<Category>/<skill-name>/
├── agents/
│   └── openai.yaml
├── SKILL.md
├── STATE.md
├── scripts/                         # optional deterministic tools
│   └── <tool>.py
└── references/
    ├── example.md
    ├── rules/
    │   ├── env.md
    │   ├── filetree.md
    │   └── state-rules.md
    └── template/
        └── STATE.template.md
```

`Custom` may use one extra subcategory level:

```text
skills/Custom/<subcategory>/<skill-name>/
```

The files shown without an "optional" comment are required for every new
repo-local skill.

## Placement Rules

- `SKILL.md`: Required skill entry point. Keep trigger conditions, core
  workflow, and short rules here.
- `skills/<Category>/`: Business-function category selected from
  `references/rules/categories.md`.
- `skills/Custom/<subcategory>/`: Optional subcategory for internal or
  user-specific skills, such as `Productivity` or `wingene`.
- `STATE.md`: Per-run working state. Keep it at the skill root so it is easy to
  find and update.
- `agents/openai.yaml`: UI metadata for skill lists and default prompts.
- `references/example.md`: Concrete examples of when the skill should trigger
  and what outputs it should produce.
- `references/rules/`: Reusable operating rules, such as state handling and
  filetree conventions. `env.md`, `filetree.md`, and `state-rules.md` are
  required.
- `references/template/`: Copyable templates, such as `STATE.template.md`.
- `scripts/`: Deterministic executable tools used directly by the workflow.
  Add this directory only when the skill needs runnable helper scripts.
- `assets/`: Output assets or templates consumed by the task. Add only when the
  skill needs non-reference files such as images, fonts, or boilerplate.

## Validation Rules

Run both validators before claiming a skill is complete:

```bash
python /home/howard/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-dir>
python skills/Custom/Productivity/skill-create/scripts/validate_skill_layout.py <skill-dir>
```

If the generic validator is unavailable because dependencies such as PyYAML are
missing, use the repository virtual environment or report the blocker. Do not
skip the local layout validator.

The local layout validator also checks that skills under `skills/` use an
approved top-level category.

To check only category placement for all skills, run:

```bash
find skills -name SKILL.md -type f -exec dirname {} \; \
  | sort \
  | xargs -n1 python skills/Custom/Productivity/skill-create/scripts/validate_skill_layout.py --category-only
```

## Cleanup Rules

- Do not add README, changelog, quick reference, or installation guide files
  unless the user explicitly asks for user-facing documentation.
- Remove generated files such as `__pycache__/` before finishing.
- Keep references one level deep where possible; avoid nested reference chains
  unless the organization materially improves discoverability.
