# PM cron installer

Run: 2026-10-19, issue 66
Implementation: completed. add-cron.sh installs/removes two system entries;
run-cron.sh is explicitly a nine-line Codex launcher, not report code.
Validation: shell syntax, skill validation and /tmp/test-add-cron.py passed.
Isolated evidence: install/reinstall/remove/reinstall, restoration of original
cron, no duplicate entries, unrelated-file preservation, no-prior cleanup.
Deployment: prepared only; active system cron and installed 95-line daily runner
unchanged. Codex workspace-write without escalation cannot run tools in this
container (bubblewrap namespace failure). No end-to-end activation claimed.
Security: no approve-for-me, danger-full-access or sandbox bypass. Launcher
explicitly denies unattended escalation; missing access is reported as blocked.
Publication: new PR pending review and merge; supersedes earlier approaches.
