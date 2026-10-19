# PM scheduled runner

Run: 2026-10-19, issue 59
Implementation: completed, 14-line daily shell
Validation: sh -n and quick_validate.py passed. /tmp/test-pm-runner.py passed
isolated install/remove/reinstall, success, failure exit propagation, preservation
of last-success on failure, and flock exclusion. Report generation mocked; no
additional real daily report publication was required for this shell refactor.
Deployment: installed shell updated; /etc/cron.d/executorch-daily read back with
skill path, 20:00 UTC = 04:00 Taipei daily. cron service running. Previous cron,
state runner and skill shell saved in state/backup-20261019. Legacy run.sh now
executes the installed skill shell. Other cron jobs unchanged.
Publication: pending PR merge.
Weekly activation: blocked by automatic approval review for persistent unattended
Codex tool execution and network push scope. No Codex command or approval change
was installed; weekly shortlist and chat notifications remain disabled.
