# ExecuTorch PM State

Run ID: weekly-refresh-104
Scope: Weekly deduplication and 2026-10-26 quantization/speculative-decoding focus.
Mode: user-requested correction
Publication status: daily batch published; policy PR pending

| Step | Status | Evidence |
| --- | --- | --- |
| Read context | completed | Read user request, active scheduler registry, PM policy, Humanizer and frontend-slides. |
| Collect or process selection | completed | Seven repeated candidates in 2026-10-26 vs 2026-10-19; read candidate issues, all returned comments and linked work. No new user selections. |
| Save records | completed | Added publication ledger and date-limited focus. Refreshed 2026-10-26_104113; preserved all existing selection and PR tracking rows. |
| Validate and publish | completed | daily main 37158189449b004bf5b092bb2f2763438a935807; 21 PDF pages, 27 links, zero stage overflow, desktop/phone/PDF visual checks passed; 10 IDs have zero historical or registry overlap. |
| Handoff | in_progress | Active cron-host policy and four-batch ledger deployed under run.lock; existing issues.json and cron preserved. Source PR https://github.com/yenhao-huang/mcp-skills-package/pull/105 open; merge is not authorized. |

## PR 60 conflict resolution (2026-10-26)

Scope: Resolve conflicts with current main for the existing issue 59 PR.
Preserved main's shared daily/weekly Codex launcher, installer, recommendation
ledger and dated focus. Kept the deletion of obsolete daily-result.cron and
run-daily-result.sh; did not revive daily_result.py or the old disabled-weekly
claims. Retained PR 60's private-artifact intent by setting umask 077 in the
current launcher before it creates state/log files. Existing permissions are
not changed. No live cron installation or scheduled report execution performed.
Validation: sh -n passed for run-cron.sh and add-cron.sh; quick_validate.py passed. Isolated test /tmp/test-pr60-runner.sh passed for daily/weekly dispatch, state/log/output modes (700 directories, 600 files), failure exit 23, invalid mode exit 2 and real flock exclusion (timeout exit 124). Evidence: /tmp/pr60-runner.PeSGsE. Both working and staged whitespace checks passed. Source PR 60 pending merge.
