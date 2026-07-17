# State Rules

`STATE.md` tracks one design-system workflow run. For a new task, reset it from
`references/template/STATE.template.md`, fill the run metadata, and set the
active step to `in_progress` before changing the target project.

Allowed statuses are `pending`, `in_progress`, `completed`, `blocked`, and
`skipped`. Mark a step complete only with concrete evidence such as inspected
files, implemented tokens/components, test commands, browser checks, or audit
results. Do not complete a later required step while an earlier one is pending
or blocked unless the user explicitly narrows the scope and the state notes it.
