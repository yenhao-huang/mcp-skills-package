# Repo Create State Rules

Use this reference when tracking a repo-create run with `STATE.md`.

## Files

State file:

```text
repo-create/STATE.md
```

Reusable template:

```text
repo-create/references/template/STATE.template.md
```

## Status Values

```text
pending
in_progress
completed
blocked
skipped
```

## Update Rules

1. Reset `STATE.md` from `references/template/STATE.template.md` for a new
   repo-create run unless the user explicitly asks to resume.
2. Set Run ID, Instance, Started, and Scope before marking workflow steps.
3. Mark the active step `in_progress` before editing target repo docs.
4. Mark a step `completed` only with concrete evidence such as file paths,
   commands, or user decisions.
5. If user decisions are missing, mark the relevant step `blocked` and record
   the exact decision needed.
