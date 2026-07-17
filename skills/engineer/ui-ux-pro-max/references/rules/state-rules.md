# State Rules

Before each new UI/UX workflow, reset `STATE.md` from
`references/template/STATE.template.md` and fill in the run metadata.

Use only these statuses: `pending`, `in_progress`, `completed`, `blocked`, and
`skipped`. Mark a step completed only after recording concrete evidence such as
the search command, inspected component or page, rendered viewport, test
result, or accessibility check.

Do not mark validation complete from search recommendations alone. Validation
must examine the actual interface or implementation produced by the task.
