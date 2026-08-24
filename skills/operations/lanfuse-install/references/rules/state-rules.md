# State Rules

Use `STATE.md` to record the current Langfuse workflow without secrets.

## Files

- State file: `<skill-dir>/STATE.md`
- Reset template: `<skill-dir>/references/template/STATE.template.md`

Reset `STATE.md` from the template for each new execution unless the user asks
to resume the exact recorded run.

## Status Values

```text
pending
in_progress
completed
blocked
skipped
```

## Evidence Rules

- Set Run ID, instance, timestamp, scope, checkout path, Compose project, and
  requested rollback level before mutation.
- Mark a step `in_progress` before acting and update it with concrete evidence
  before marking it `completed`.
- Record commands and observable results such as service state, health status,
  endpoint response, trace arrival, and volume presence without recording
  credentials or secret values.
- Record whether the target is disposable and whether destructive volume or
  checkout removal was explicitly confirmed.
- Do not mark reversible validation complete without evidence for first
  install, rollback, and second install.
- Mark a blocked step with the exact missing permission, prerequisite, service,
  or safety condition. Do not skip earlier required steps silently.
