# Filetree Rules

This skill uses the required repository-local layout:

```text
add-tailscale-node/
├── SKILL.md
├── STATE.md
└── references/
    ├── home-multi-node.md
    ├── tailscale-container-workflow.md
    ├── rules/
    │   ├── env.md
    │   ├── filetree.md
    │   └── state-rules.md
    └── template/
        ├── STATE.template.md
        └── home-nodes.template.yaml
```

Keep lifecycle commands and detailed domain guidance in
`references/tailscale-container-workflow.md`. Use
`references/home-multi-node.md` for configurable home/node SSH
authorization and `references/template/home-nodes.template.yaml` for inventory.
Keep runtime peer inventories in the user's private workspace. Keep `SKILL.md`
focused on triggers, workflow routing, and guardrails. Do not add scripts unless a future
task requires tested reusable automation. Do not add README, changelog, or
generated cache files.
