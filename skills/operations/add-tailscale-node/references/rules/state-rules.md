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

For `@home`, record add/remove intent, key and firewall changes, managed
shared-key source unions, backup paths and each directional validation round.
If either required direction fails unexpectedly, record at least three rounds,
even if it recovers in round 2. Each round covers both directions, with actual
test counts and inaccessible-source prerequisites distinguished. Use current
final-round results; do not carry an earlier pass forward without retesting.
Expected denied access on explicit removal is not an unexpected failure.
User-skipped nodes remain skipped; configured-but-untested revocation remains
unverified. Keep per-run inventories and evidence outside the shared skill.
