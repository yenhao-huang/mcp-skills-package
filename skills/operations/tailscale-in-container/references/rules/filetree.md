# Filetree Rules

This skill uses the required repository-local layout:

```text
tailscale-in-container/
├── SKILL.md
├── STATE.md
└── references/
    ├── tailscale-container-workflow.md
    ├── rules/
    │   ├── env.md
    │   ├── filetree.md
    │   └── state-rules.md
    └── template/
        └── STATE.template.md
```

Keep lifecycle commands and detailed domain guidance in
`references/tailscale-container-workflow.md`. Keep `SKILL.md` focused on
triggers, workflow routing, and guardrails. Do not add scripts unless a future
task requires tested reusable automation. Do not add README, changelog, or
generated cache files.
