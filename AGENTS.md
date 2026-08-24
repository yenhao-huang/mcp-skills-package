# Agent Instructions

## Skill Work

When a task involves reading, creating, updating, reviewing, validating, or
documenting any skill under `skills/`, read this file first:

```text
skills/custom/productivity/skill-create/SKILL.md
```

Follow the workflow and reference-loading rules in
`skills/custom/productivity/skill-create/SKILL.md` before changing skill files.

Use this rule for requests that mention skills, skill directories, `SKILL.md`,
skill metadata, skill references, skill validation, or skill behavior.

If the task is only to install a skill from an external source, use the
`skill-installer` workflow instead.

### Skill Change Delivery

Any change under `skills/` must use the following delivery workflow:

1. Create or link a GitHub issue that defines the scope and acceptance
   criteria before editing the skill.
2. Make the change on a non-default branch, validate it, and open a pull
   request linked to the issue. Never push the skill change directly to
   `main`.
3. Wait for the pull request to be merged into `main`, then verify that the
   merged `main` contains the change before reporting the task as complete.

An open pull request is not completion. If issue or pull-request creation is
unavailable, or the pull request is still awaiting review, checks, or merge,
report the exact pending state instead of claiming the skill change is
complete.
## Tailscale Container Workflow

When a task involves installing, starting, integrating, diagnosing, stopping,
or uninstalling Tailscale inside an existing Docker or LXC container, read:

```text
skills/operations/tailscale-in-container/SKILL.md
```

Use this workflow for container-to-cluster connectivity, userspace networking,
`/dev/net/tun` and capability checks, Tailscale Serve or proxy configuration,
and safe package or identity removal while keeping the host out of the tailnet.

## Langfuse Installation Workflow

When a task involves installing, configuring, validating, integrating,
reinstalling, or uninstalling a local self-hosted Langfuse deployment, read:

```text
skills/operations/lanfuse-install/SKILL.md
```

Use this workflow for Docker Compose deployment, first-run initialization,
Hermes observability traces, isolated Windows Hermes environments, and safe
Langfuse container, volume, image, or checkout cleanup.

## Git Commit Workflow

When a requested implementation task is complete and relevant validation has
passed, create a focused local git commit unless the user explicitly says not
to commit.

Keep each commit scoped to one self-contained feature, bug fix, refactor,
documentation update, skill update, or maintenance step. Stage only files
related to that completed unit of work, inspect the staged diff before
committing, and do not include unrelated user changes.

Use Conventional Commits where possible:

```text
feat: add new behavior
fix: correct broken behavior
refactor: restructure code without changing behavior
docs: update documentation or reports
chore: maintain repository or skill packaging
```

Never push to `upstream`, `origin`, or any shared remote unless the user
explicitly asks for a push.

## Repository Safety

Preserve unrelated user changes. Stage or commit only files that belong to the
current request.
