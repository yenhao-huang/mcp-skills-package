# Single-file cron migration

Run: 2026-10-19, issue 61
Implementation: completed. One Bash executable run-cron.sh; old Python and shell
runner removed. No embedded Python and no other custom job implementation.
Validation: bash -n, isolated snapshot tests, real GitHub dry-run passed.
Fixture evidence: next-day creation, same-day reuse, historical immutability,
older missing PR reconciliation, merged vs closed, API failure retention,
selected/unissued rows, source-relative links, dirty checkout and push failures.
Deployment: completed. Cron readback points directly to installed run-cron.sh;
cron is running; installed outer --dry-run succeeded against real GitHub data.
Old Python, old shell and state/run.sh removed after backup. Executable
install/remove/reinstall and outer failure/logging/last-success tests passed.
Weekly automation/notifications remain disabled.
Publication: pending PR merge.
