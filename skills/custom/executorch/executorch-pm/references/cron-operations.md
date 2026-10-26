# Install PM cron

`add-cron.sh` installs system cron. `run-cron.sh` is a compact launcher for
Codex to execute the skill; it contains no deterministic daily/weekly report
implementation. No Python job file is used.

On the existing UTC Debian host with user howard, first install the complete
skill (including its matching run-cron.sh) under /home/howard/.codex/skills.
Then run the ten-line installer with no arguments:

```sh
/home/howard/.codex/skills/executorch-pm/references/scripts/add-cron.sh
```

It checks the executable and UTC host, writes both entries to one temporary file,
installs /etc/cron.d/executorch-daily root-owned mode 0644, and starts cron.
Re-running replaces this dedicated file rather than appending duplicate jobs.
There are no preview/remove options or automatic backups. Before replacing an
existing job, manually copy its cron file and runner outside /etc/cron.d.
To roll back, restore those exact files; on a first installation remove only
/etc/cron.d/executorch-daily. Preserve unrelated jobs and report artifacts.
This host-specific installer assumes installed Codex, credentials, checkout and
rendering tools; it does not provision them or provision GitHub/model access.

UTC daily 20:00 = Taipei daily 04:00; UTC Sunday 20:00 = Taipei Monday 04:00.
Both jobs acquire one flock (wait up to two hours), each with a 90-minute run
limit. Order is unspecified; the second job reads the latest same-day artifacts.
State: /home/howard/.local/state/executorch-cron, overridable with
EXECUTORCH_CRON_STATE. Logs: logs/DATE-MODE.log; output: MODE-last-message.txt.
The launcher sets `umask 077` before creating state directories, logs or last-message
files, keeping newly created artifacts private to the running account. Existing
files retain their current permissions.
No chat notification channel is configured. The old last-success file is
historical and is not updated by this launcher.

Codex now uses the user's explicitly authorized `danger-full-access`,
`approval_policy="never"`, `--ephemeral` and `--skip-git-repo-check`, with
checkout `/workspace/executorch-worktrees/daily`. The daily launcher was tested
under a minimal cron environment on 2026-10-20 and published verified remote
commit `2ead54b26dc26b1e8ec94c4989b7759b945d411f`. Weekly was not rerun.
The previous workspace-write namespace failure describes the old configuration.
For a minimal direct-Codex alternative, use
[the four-line timer template](../../../../operations/set-daily-cron/references/template/codex.cron).
Replace the existing entries when installing it; do not install both versions.
The template writes mode-specific logs but does not use the launcher's timeout
or last-message files. Preparing the template does not change active cron.

Cron's container has sleep infinity as PID 1; restart persistence/backfill is
not guaranteed. Installing a cron file does not fix the container lifecycle.
