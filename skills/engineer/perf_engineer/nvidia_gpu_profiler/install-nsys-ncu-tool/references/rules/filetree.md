# Filetree Rules

```text
install-nsys-ncu-tool/
├── SKILL.md
├── STATE.md
├── scripts/                # user-requested location for the Docker files
│   ├── Dockerfile
│   └── compose.yaml
└── references/
    ├── rules/{env,filetree,state-rules}.md
    └── template/STATE.template.md
```

Do not write reports, archives, or `work/` into the skill directory; use
`WORK_DIR` and an external path for `nsys-ncu-tool.tar.zst`.
