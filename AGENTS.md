# Agent Instructions

## Skill Work

When a task involves reading, creating, updating, reviewing, validating, or
documenting any skill under `skills/`, read this file first:

```text
skills/skill-create/SKILL.md
```

Follow the workflow and reference-loading rules in `skills/skill-create/SKILL.md`
before changing skill files.

Use this rule for requests that mention skills, skill directories, `SKILL.md`,
skill metadata, skill references, skill validation, or skill behavior.

If the task is only to install a skill from an external source, use the
`skill-installer` workflow instead.

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
