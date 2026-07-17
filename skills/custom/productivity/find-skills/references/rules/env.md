# Environment Rules

The core discovery workflow is documentation-driven and does not require a
project runtime or local service.

```text
Primary language: Markdown
Runtime version: none
Package manager: none for discovery; npx only for optional approved installs
Frameworks: none
Service manager: none
Required services: none; network access is needed for live remote discovery
```

- Prefer the available web/GitHub tools for read-only source inspection.
- Shell examples in the registry use `curl` and `jq`; use an equivalent
  read-only method when either is unavailable.
- Do not install packages merely to search a source when its catalog can be
  inspected directly.
- Before any approved install, confirm Node.js/npm availability if the chosen
  installer uses `npx` and use its dry-run mode first.
- Never invent credentials, target directories, host flags, or runtime
  assumptions. Ask for a material missing choice before writing externally.
