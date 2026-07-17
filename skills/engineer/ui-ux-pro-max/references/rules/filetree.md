# Filetree Rules

## Maintained Layout

```text
ui-ux-pro-max/
├── SKILL.md
├── STATE.md
└── references/
    ├── data/
    │   ├── *.csv
    │   └── stacks/*.csv
    ├── licenses/
    ├── rules/
    │   ├── env.md
    │   ├── filetree.md
    │   └── state-rules.md
    ├── scripts/
    │   ├── core.py
    │   ├── design_system.py
    │   └── search.py
    ├── template/STATE.template.md
    ├── design-workflow.md
    └── provenance.md
```

- Keep executable Python helpers in `references/scripts/`.
- Keep the searchable CSV knowledge base in `references/data/` and stack data
  in `references/data/stacks/`.
- Keep imported license notices in `references/licenses/` and imported
  revision details in `references/provenance.md`.
- Update script-relative paths when moving scripts or data.
- Do not add a README, changelog, `agents/`, or top-level `scripts/` directory.
- Remove `__pycache__/`, `.pyc`, and other generated files before handoff.
