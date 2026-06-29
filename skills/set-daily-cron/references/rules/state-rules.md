# State Rules

Use this reference when this skill tracks multi-step work with `STATE.md`.

## Files

State file:

```text
set-daily-cron/STATE.md
```

Reusable template:

```text
set-daily-cron/references/template/STATE.template.md
```

`STATE.md` is per-run working state. Before starting a new execution, reset it
from `references/template/STATE.template.md` unless the user explicitly asks to
resume the existing run.

## Hard Guard

```text
Do not claim a workflow step is complete unless STATE.md was updated in the
same turn with concrete evidence.
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

1. Before starting a workflow step, create `STATE.md` from
   `references/template/STATE.template.md` if it does not exist.
2. If `STATE.md` has completed, blocked, or in-progress steps and the user did
   not explicitly ask to resume that exact run, overwrite `STATE.md` from
   `references/template/STATE.template.md` before continuing.
3. Set Run ID, Instance, Started, and Scope before marking workflow steps.
4. When beginning a step, set that step to `in_progress`.
5. When completing a step, set that step to `completed` and add concrete
   evidence such as command output, file path, or hook result.
6. When blocked, set the step to `blocked` and record the exact blocker.
7. Do not mark a later step completed while an earlier required step is still
   pending or blocked unless the user explicitly scoped the task to that later
   step.
