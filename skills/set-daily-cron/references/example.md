# Examples

## Inspect Whether Cron Ran Today

Read
`.codex/skills/set-daily-cron/references/tasks/git-commit/state.json` and
inspect `last_run_at`, `last_result`, and `last_report`. Confirm the report file
exists under
`.codex/skills/set-daily-cron/references/tasks/git-commit/reports/`.

## Regenerate A Deleted Report

If a user deletes the latest report and expects Codex to recreate it, run the
hook manually or ensure the hook runs on the next relevant event. The hook
should regenerate when an enabled task's `last_report` path is missing.

## Reset Daily State

Set the task folder's `state.json` fields such as `last_run_at`,
`last_report`, and `last_result` to `null`. Keep generated reports under that
task folder's `reports/` directory.
