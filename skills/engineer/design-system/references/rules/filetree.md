# Filetree Rules

The maintained skill layout is:

```text
skills/engineer/design-system/
├── SKILL.md
├── STATE.md
└── references/
    ├── LICENSE.txt
    ├── design-system-rules.md
    ├── motion-choreography.md
    ├── provenance.md
    ├── rules/
    │   ├── env.md
    │   ├── filetree.md
    │   └── state-rules.md
    └── template/
        └── STATE.template.md
```

- Keep trigger conditions and workflow in `SKILL.md`.
- Keep detailed design guidance under `references/`.
- Record per-run evidence in `STATE.md` and reset it from the template for a
  new run.
- Do not add top-level scripts, agents, generated screenshots, build output,
  fonts, or frontend packages to this skill.
