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
- `repo-create`

#### engineer/git

Skills matching `git-*` or `github-*` for local Git repository workflows,
GitHub issues, and pull requests. Store these under `skills/engineer/git/`.

Current examples:

- `git-commit`
- `github-issues`
- `github-pr-workflow`

#### engineer/openspec

OpenSpec change planning, exploration, implementation, synchronization, and
archival workflows. Keep the existing `openspec-*` skill names under
`skills/engineer/openspec/`.

Current examples:

- `openspec-apply-change`
- `openspec-archive-change`
- `openspec-explore`
- `openspec-propose`
- `openspec-sync-specs`

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

- `custom/ai-models`: personal model discovery, download, inference, and evaluation workflows.
- `custom/apple`: personal Apple-platform projects and tool-selection workflows.
- `custom/content`: personal content research, generation, and publishing workflows.
- `custom/cron`: personal recurring workflows migrated from external schedulers.
- `custom/finance`: personal finance analysis and knowledge-management workflows.
- `custom/notion`: personal Notion publishing and structured-update workflows.
- `custom/personal`: personal daily routines and accountability workflows.
- `custom/productivity`: personal productivity and skill-management helpers.
- `custom/wingene`: Wingene/internal environment workflows.

Current examples:

- `custom/ai-models/model-tester`
- `custom/apple/ios-swiftui-mcp`
- `custom/content/daily-news-ops`
- `custom/cron/daily-news-digest`
- `custom/finance/financial-report-analysis`
- `custom/notion/notion-mcp-ops`
- `custom/personal/daily-checkin-assistant`
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
- Use `engineer/git/<skill-name>` for Git/GitHub skills and
  `engineer/openspec/<skill-name>` for OpenSpec skills.
- Use `custom` when the skill is tied to a specific company, project, user, or
  local environment.
- Use `custom/<subcategory>` when multiple internal skills share the same owner
  or purpose.
- Keep `name:` in `SKILL.md` globally unique even when a skill lives under a
  category directory.
- Do not create new top-level categories without updating this file in the same
  change.
