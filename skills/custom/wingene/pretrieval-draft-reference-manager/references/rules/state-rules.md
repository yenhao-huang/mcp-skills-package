# Run evidence

For a new operation copy `references/template/STATE.template.md` to a writable
local run record. Resume an existing run only when it is the same requested task.
Record the requested instance/operation, authorization scope, Taipei date/time,
source SHAs, host, exact affected resources and baseline IDs/StartedAt.

Use pending/in_progress/completed/blocked/skipped. Mark a step completed only with
observed evidence in the same turn. Separate code preparation, host deployment,
functional verification, PR publication and main merge. Record exact commands and
outcomes, paths to private evidence, URLs, limitations and retained/deleted data.
Never include secrets or claim future checks already passed. Static skill
validation does not establish runtime correctness. A PR is pending publication
until merged and verified on main.
