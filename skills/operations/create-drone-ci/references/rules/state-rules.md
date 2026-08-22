# State Rules

`STATE.md` records one execution of the create-drone-ci workflow. Before a new
execution, reset it from `references/template/STATE.template.md`.

## Status Values

Use only `pending`, `in_progress`, `completed`, `blocked`, or `skipped`.

## Update Rules

1. Set Run ID, Instance, Started, Scope, and Last updated before work begins.
2. Mark a step `in_progress` before performing it.
3. Mark a step `completed` only with concrete evidence such as a file path,
   command, test result, container state, or webhook inspection.
4. Mark service startup `skipped` when the user requested scaffolding only.
5. Mark a step `blocked` when required provider, callback, credential, remote,
   or host information cannot be safely discovered.
6. Do not mark later required steps complete while an earlier step is pending
   or blocked unless the user explicitly narrowed the scope; record that scope.
7. Update evidence after any later edit that affects acceptance criteria.

## Hard Guard

Do not claim any workflow step is complete unless `STATE.md` was updated in the
same turn with concrete evidence.
