# Filetree Rules

- Preserve the target repository's existing structure and naming conventions.
- Add files only where repository instructions or established adjacent code
  indicate they belong.
- Keep generated artifacts, caches, build output, and temporary work out of
  commits unless the repository explicitly tracks them.
- Do not move or delete unrelated user files.
- Before committing, inspect the complete changed-file list and stage only the
  files required to solve the target issue.

The skill itself must retain this repository-local layout:

```text
skills/engineer/solve-issue/
├── SKILL.md
├── STATE.md
└── references/
    ├── LICENSE.txt
    ├── rules/
    │   ├── env.md
    │   ├── filetree.md
    │   └── state-rules.md
    └── template/
        └── STATE.template.md
```
