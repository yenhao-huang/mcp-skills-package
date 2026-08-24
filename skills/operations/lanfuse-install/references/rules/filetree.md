# Managed Filetree Rules

Inspect the actual checkout before mutation. A typical managed deployment uses:

```text
<langfuse-root>/
├── docker-compose.yml       # checked-out service source of truth
└── .env                     # local secrets; never commit

<hermes-home>/
└── .hermes/
    └── .env                 # preserve unrelated Hermes variables
```

## Rules

- Reuse an existing Langfuse checkout only after inspecting its branch and
  local changes. Do not overwrite modified files.
- Keep deployment secrets in the ignored environment mechanism expected by the
  inspected Compose file.
- Do not copy the Langfuse source tree, database files, or container volumes
  into this skill.
- Resolve the absolute checkout path and Compose project before cleanup.
- Delete only files, containers, networks, images, and volumes explicitly
  attributed to the selected deployment.
- Back up or restore a pre-existing Hermes `.env`; never replace the whole file
  merely to add Langfuse variables.
