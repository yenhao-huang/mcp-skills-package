# Local daily Result cron

Installed on 2026-10-15 in the Debian container for user howard.
Daily job is enabled; weekly shortlist remains not_enabled.

- Service: Debian cron, `/etc/cron.d/executorch-daily`.
- Host timezone: Etc/UTC. `0 20 * * *` equals 04:00 Asia/Taipei next day.
- Runner: `/home/howard/.codex/skills/executorch-pm/references/scripts/run-daily-result.sh` (14 lines; cron invokes the skill file directly).
- Script: installed PM references/scripts/daily_result.py.
- Isolated checkout: `/home/howard/.local/state/executorch-cron/daily`.
- Logs: `/home/howard/.local/state/executorch-cron/logs/YYYY-MM-DD.log`.
- Last success: `/home/howard/.local/state/executorch-cron/last-success`.
- Uses existing gh credentials; no tokens are copied into cron files.
- Uses a lock and 15-minute timeout. API calls are GET only. The sole Git write
  destination is yenhao-huang/daily main, and staged files are limited to Result.md.
- Reconciles tracked PRs across reports, preserves previous dates and source links,
  and keeps status/check time on API failure. Previous CI/review details are dated
  history; this deterministic job checks PR open/closed/draft/merged state only.
- Detailed CI/review investigation is a separate PM run; the daily script sends
  no notifications or community messages and never starts issue development.

## Validate and operate

`sudo service cron status` checks the daemon. Run the runner to publish today,
or run `python3 <installed-PM>/references/scripts/daily_result.py --repo
/home/howard/.local/state/executorch-cron/daily` without --publish for a read-only
remote dry run (it may clone/fetch locally). Inspect logs on failure; an uncommitted
dirty checkout is intentionally not reset. A committed push failure is retried
on the next run. Diverged branches require manual reconciliation, never force push.

To disable only this job, move /etc/cron.d/executorch-daily outside /etc/cron.d.
Restore references/daily-result.cron as root-owned mode 0644 and start cron to
re-enable. Do not stop the shared daemon or remove other jobs. The user authorized
cron installation; use this only for the documented daily job.

## Container lifetime

PID 1 is `sleep infinity`; there is no init/service manager. Cron is running now
but is not guaranteed to start after this container stops/restarts. The container
startup configuration is outside this workspace. After restart run `sudo service
cron start`, or have the container owner add that command to the existing startup
sequence. Cron cannot execute while the container is off and does not backfill
missed days. A new/recreated container needs the package and job installed again.
Do not claim host reboot persistence or weekly shortlist activation.

## Validation evidence

A clean-environment runner invocation successfully published Result.md on
2026-10-15, commit b5565d89d92ff0fffbdb0abeedea9850e4925ab8. Closed-unmerged maps
to PR 未 merge; merged maps to Done; original shortlist links remain absolute.

Cron daemon trigger verified at 2026-10-15T08:19:01Z using a temporary minute
probe, then removed. Simulated next-day tests passed: new Result-only directory,
prior-day immutability, previous snapshot link, and API-failure status retention.

## 2026-10-19 concise entrypoint

Cron now references the skill-owned shell directly instead of a separate copy.
The shell handles Taipei time, private logs, flock, timeout, exit logging and
last-success; daily_result.py owns report generation/publication. Cron supplies
HOME and PATH. EXECUTORCH_CRON_STATE optionally selects an isolated state directory.
The old state/run.sh is a compatibility wrapper to the skill script.
Weekly shortlist and chat notification are not enabled by this change.

Before migration, back up /etc/cron.d/executorch-daily and state/run.sh.
Rollback restores those exact backups and the prior installed shell; leave daily
reports, logs and unrelated cron jobs intact. Validate migration and rollback
in a disposable copy before installing and read back the active cron target.
