# Skill Category Rules

Use this reference before creating, moving, or reclassifying skills under
`.codex/skills`.

## Approved Categories

```text
sales
engineer
operations
finance
legal
content-producer
custom
others
```

Empty categories may be kept with `.gitkeep`.

## Category Definitions

### sales

Sales, customer development, business communication, proposal support, CRM, and
revenue-facing workflows.

Current status: empty.

### engineer

Software engineering, debugging, codebase understanding, repository management,
technical specifications, and implementation workflows.

Current examples:

- `code-summary`
- `debug`
- `dev`
- `git-commit`
- `github-issues`
- `github-pr-workflow`
- `openspec-*`
- `repo-create`

### operations

Automation, scheduling, infrastructure setup, runtime services, MCP setup,
sandboxing, knowledge operations, and local service management.

Current examples:

- `agent-loop`
- `create-sandbox`
- `mcp-init`
- `notion`
- `set-daily-cron`
- `vllm-embedding-server`

### finance

Finance, accounting, budgeting, cost analysis, invoices, and financial reports.

Current status: empty.

### legal

Legal, contracts, compliance, policy review, governance, and risk workflows.

Current status: empty.

### content-producer

Content planning and production: posts, reports, summaries, presentation
material, video material collection, and public-facing writing.

Current examples:

- `linkedin-post`

### custom

Company-specific, user-specific, or project-specific skills. Use subcategories
when they make ownership clearer.

Current subcategories:

- `custom/productivity`: personal productivity and skill-management helpers.
- `custom/wingene`: Wingene/internal environment workflows.

Current examples:

- `custom/productivity/skill-create`
- `custom/productivity/find-skills`
- `custom/wingene/send-to-vdi`
- `custom/pretrieval-offline-packaging`

### others

Skills that do not cleanly fit the above business functions, are analysis-only,
or are pending a better category.

Current examples:

- `loop-analysis`

## Placement Rules

- Prefer a business-function category over `others`.
- Use `custom` when the skill is tied to a specific company, project, user, or
  local environment.
- Use `custom/<subcategory>` when multiple internal skills share the same owner
  or purpose.
- Keep `name:` in `SKILL.md` globally unique even when a skill lives under a
  category directory.
- Do not create new top-level categories without updating this file in the same
  change.
