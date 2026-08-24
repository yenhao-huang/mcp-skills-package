# State Rules

Use `STATE.md` as per-run workflow state. For a new request, reset it from
`references/template/STATE.template.md`, then fill Run ID, Instance, Started,
Scope, and Last updated.

Allowed statuses are `pending`, `in_progress`, `completed`, `blocked`, and
`skipped`.

Before starting a phase, mark it `in_progress`. Mark it `completed` only with
concrete evidence such as detected runtime facts, exact commands, daemon
status, Tailscale status, or an application connectivity test. Do not mark a
later required phase complete while an earlier phase is pending or blocked.

Never record auth keys, login URLs containing credentials, reusable secrets,
or unredacted sensitive logs in `STATE.md`.
