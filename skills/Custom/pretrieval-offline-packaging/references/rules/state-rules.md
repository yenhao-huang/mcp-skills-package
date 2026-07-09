# State Rules

Use `STATE.md` to track each packaging run.

## Status Values

```text
pending
in_progress
completed
blocked
skipped
```

## Update Rules

1. Reset `STATE.md` from `references/template/STATE.template.md` for a new run.
2. Fill Run ID, Instance, Started, and Scope before executing packaging steps.
3. Mark a step `in_progress` before starting it.
4. Mark a step `completed` only with concrete evidence, such as command output,
   bundle path, image ID, checksum result, or file path.
5. If packaging fails, mark the failed step `blocked` and record the exact
   command and failure.
6. Do not claim a bundle is complete unless checksum validation passed.
