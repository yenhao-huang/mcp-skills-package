# Install PM cron

`add-cron.sh` installs system cron. `run-cron.sh` is a nine-line launcher for
Codex to execute the skill; it contains no deterministic daily/weekly report
implementation. No Python job file is used.

On the existing UTC Debian host with user howard, install the skill under
/home/howard/.codex/skills/executorch-pm first, then run:

```sh
/home/howard/.codex/skills/executorch-pm/references/scripts/add-cron.sh --print
/home/howard/.codex/skills/executorch-pm/references/scripts/add-cron.sh --install
```

The installer requires an executable sibling run-cron.sh, Codex on PATH, the
existing state/daily checkout and running cron. It uses sudo for the system
file, replaces only /etc/cron.d/executorch-daily atomically, and preserves the
original in /etc/cron.d/.executorch-daily.before-add-cron. Reinstalling replaces
the same two entries, not appends duplicates. --remove restores that backup,
or removes only this job when no prior file existed. Preserve unrelated jobs.

UTC daily 20:00 = Taipei daily 04:00; UTC Sunday 20:00 = Taipei Monday 04:00.
Both jobs acquire one flock (wait up to two hours), each with a 90-minute run
limit. Order is unspecified; the second job reads the latest same-day artifacts.
State: /home/howard/.local/state/executorch-cron, overridable with
EXECUTORCH_CRON_STATE. Logs: logs/DATE-MODE.log; output: MODE-last-message.txt.
No chat notification channel is configured. The old last-success file is
historical and is not updated by this launcher.

Codex runs with workspace-write and approval_policy=never: it cannot escalate
permissions unattended. It still needs a working sandbox, GitHub/model access
and rendering dependencies. On this container the sandbox probe failed because
bubblewrap could not create namespaces; the successful retry required approval.
Therefore this launcher is NOT verified end to end here. Do not replace the
working deterministic daily job until the execution environment supports these
restrictions. This PR delivers an installer and reviewable configuration; the
active system cron is unchanged by preparing this PR.

Cron's container has sleep infinity as PID 1; restart persistence/backfill is
not guaranteed. Installing a cron file does not fix the container lifecycle.
