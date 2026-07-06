# State Rules

Use this reference when a create-sandbox workflow tracks progress with
`STATE.md`.

## Files

- State file: `STATE.md`
- Reset template: `references/template/STATE.template.md`

`STATE.md` is per-run working state. Before starting a new execution, reset it
from the template unless the user explicitly asks to resume the existing run.

## Hard Guard

Do not claim a workflow step is complete unless `STATE.md` was updated in the
same turn with concrete evidence.

## Status Values

```text
pending
in_progress
completed
blocked
skipped
```

## Update Rules

1. Before starting a workflow step, create `STATE.md` from the template if it
   does not exist.
2. If `STATE.md` has completed, blocked, or in-progress steps and the user did
   not explicitly ask to resume that exact run, overwrite it from the template
   before continuing.
3. Set Run ID, Instance, Started, and Scope before marking workflow steps.
4. When beginning a step, set that step to `in_progress`.
5. When completing a step, set that step to `completed` and add concrete
   evidence such as command output, test name, file path, or code path.
6. When blocked, set the step to `blocked` and record the exact blocker.
7. Do not mark a later step completed while an earlier required step is pending
   or blocked unless the user explicitly scoped the task to that later step.
