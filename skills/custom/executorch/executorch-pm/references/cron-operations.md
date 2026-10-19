# Daily Result cron

The only job executable is `references/scripts/run-cron.sh`. It contains the
complete daily workflow in Bash and uses git, gh, jq, awk and GNU coreutils.
It does not embed Python or invoke another custom executable. It re-enters itself
under timeout; this is the same file, not a hidden second script.

- `/etc/cron.d/executorch-daily` calls the installed skill file directly.
- `0 20 * * *` on this UTC host is daily 04:00 Asia/Taipei.
- State: `/home/howard/.local/state/executorch-cron`; override with
  EXECUTORCH_CRON_STATE for an isolated checkout/log directory.
- Checkout: state/daily, verified yenhao-huang/daily main only.
- Logs: state/logs/YYYY-MM-DD.log; successful published run: state/last-success.
- Lock: state/run.lock; total timeout 15 minutes. Cron supplies PATH and HOME.
- Run without arguments to publish. `run-cron.sh --dry-run` fetches Git/API data
  and writes the proposed report to the private log, without report writes,
  commits or pushes. --worker is internal to the timeout invocation.
- Reconcile tracking rows from all dates, preserve selections and original
  relative link destinations, reuse today's latest snapshot, and preserve older
  days. Failed PR lookups keep prior state/check time with a failure note.
- Done requires merged=true. Closed-unmerged remains PR 未 merge. No-change
  states still produce today's snapshot. Only Result.md may be staged/pushed.
- Dirty/diverged checkouts stop without reset. A rejected push remains a local
  commit; later runs verify pending file paths/references before retrying.
- Weekly candidate generation and chat delivery are NOT enabled by this file.
  This deterministic job checks PR state, not detailed CI or review changes.

## Install / rollback

Back up the installed runner and /etc/cron.d/executorch-daily outside active
skill scripts before migration. Install run-cron.sh mode 0755 and
references/daily-result.cron as root-owned /etc/cron.d/executorch-daily mode 0644.
Remove legacy job executables only after backing them up. Validate shell syntax,
a dry run, cron readback and service status. Do not modify other jobs.
Rollback restores the exact backed-up runner(s) and cron file and removes only
the newly installed run-cron.sh; preserve reports/logs and unrelated state.
The 2026-10-19 migration backup is state/backup-single-file-20261019.

## Lifetime

Cron runs in a container whose PID 1 is sleep infinity. It does not survive a
stopped/recreated container automatically. After restart the owner must start
cron or add it to the container startup configuration. No backfill or reboot
persistence is claimed. Verify with `sudo service cron status`.
