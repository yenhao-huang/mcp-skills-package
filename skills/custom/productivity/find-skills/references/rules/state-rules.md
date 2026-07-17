# State Rules

`STATE.md` tracks one discovery or maintenance run. Before a new run, reset it
from `references/template/STATE.template.md` unless the user explicitly asks to
resume the current run.

## Status Values

```text
pending
in_progress
completed
blocked
skipped
```

## Update Rules

1. Set Run ID, Instance, Started, Scope, and Last updated before work begins.
2. Mark a step `in_progress` before performing it.
3. Mark it `completed` only with concrete evidence such as registries and query
   terms searched, candidate paths reviewed, commands run, or validation output.
4. Mark a hard stop `blocked` with the exact unresolved condition.
5. Use `skipped` only when the user's scope makes a step inapplicable and record
   why; installation is normally skipped until explicit approval.
6. Do not complete a later required step while an earlier one remains pending
   or blocked unless the scoped exception is recorded in Notes.
7. Refresh evidence when later edits affect a completed step's acceptance
   criteria.

Do not claim a workflow step is complete unless `STATE.md` was updated in the
same turn with concrete evidence.
