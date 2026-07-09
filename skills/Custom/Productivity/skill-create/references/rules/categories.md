# Skill Category Rules

Use this reference before creating, moving, or reclassifying skills under
`.codex/skills`.

## Approved Categories

```text
Sales
Engineer
Operations
Finance
Legal
Content-Producer
Custom
Others
```

Empty categories may be kept with `.gitkeep`.

## Category Definitions

### Sales

Sales, customer development, business communication, proposal support, CRM, and
revenue-facing workflows.

Current status: empty.

### Engineer

Software engineering, debugging, codebase understanding, repository management,
technical specifications, and implementation workflows.

Current examples:

- `code-summary`
- `debug`
- `dev`
- `openspec-*`
- `repo-create`

### Operations

Automation, scheduling, infrastructure setup, runtime services, MCP setup,
sandboxing, knowledge operations, and local service management.

Current examples:

- `agent-loop`
- `create-sandbox`
- `mcp-init`
- `notion`
- `set-daily-cron`
- `vllm-embedding-server`

### Finance

Finance, accounting, budgeting, cost analysis, invoices, and financial reports.

Current status: empty.

### Legal

Legal, contracts, compliance, policy review, governance, and risk workflows.

Current status: empty.

### Content-Producer

Content planning and production: posts, reports, summaries, presentation
material, video material collection, and public-facing writing.

Current examples:

- `linkedin-post`

### Custom

Company-specific, user-specific, or project-specific skills. Use subcategories
when they make ownership clearer.

Current subcategories:

- `Custom/Productivity`: personal productivity and skill-management helpers.
- `Custom/wingene`: Wingene/internal environment workflows.

Current examples:

- `Custom/Productivity/skill-create`
- `Custom/Productivity/find-skills`
- `Custom/wingene/send-to-vdi`
- `Custom/pretrieval-offline-packaging`

### Others

Skills that do not cleanly fit the above business functions, are analysis-only,
or are pending a better category.

Current examples:

- `loop-analysis`

## Placement Rules

- Prefer a business-function category over `Others`.
- Use `Custom` when the skill is tied to a specific company, project, user, or
  local environment.
- Use `Custom/<subcategory>` when multiple internal skills share the same owner
  or purpose.
- Keep `name:` in `SKILL.md` globally unique even when a skill lives under a
  category directory.
- Do not create new top-level categories without updating this file and
  `validate_skill_layout.py` in the same change.
