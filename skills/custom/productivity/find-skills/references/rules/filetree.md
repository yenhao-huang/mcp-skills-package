# Filetree Rules

The `find-skills` directory must keep this layout:

```text
find-skills/
├── SKILL.md
├── STATE.md
└── references/
    ├── skill-registry.md
    ├── rules/
    │   ├── candidate-review.md
    │   ├── env.md
    │   ├── filetree.md
    │   └── state-rules.md
    └── template/
        └── STATE.template.md
```

- Keep triggers, core workflow, and short guardrails in `SKILL.md`.
- Keep managed library records and maintenance procedures in
  `references/skill-registry.md`, the registry source of truth.
- Keep reusable review and operating rules in `references/rules/`.
- Put executable helpers in the optional references scripts subdirectory only
  if a future workflow needs them; do not add top-level `scripts/` or `agents/`
  directories.
- Do not add README, changelog, installation guide, or quick-reference files
  unless explicitly requested.
- Remove generated files such as `__pycache__/` before finishing.

Validate with the generic skill validator, required-path inspection, local
reference/link inspection, and `git diff --check`.
