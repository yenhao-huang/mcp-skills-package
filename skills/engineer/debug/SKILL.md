---
name: debug
description: Record and run structured debugging sessions. Use when the user asks to enter debug mode, debug phase, debugging session, investigate an issue while logging the process, or explicitly asks to record each dialogue/search/command/decision during troubleshooting.
---

# Debug

Use this skill to keep an auditable debugging trail while investigating a live issue.

## Workflow

1. Start or select a log file under `logs/debug/`.
   - Prefer `logs/debug/YYYY-MM-DD-<short-topic>.md`.
   - If the user is continuing the same issue, append to the existing log.
2. Record every turn while debug mode is active:
   - User question or request.
   - Assistant interpretation and current hypothesis.
   - Commands, searches, files read, and important outputs.
   - Decisions, changes made, and validation results.
   - Open questions and next actions.
3. Keep entries chronological. Use exact timestamps when available; otherwise use the current date and turn order.
4. Keep raw command output concise. Include the command and the decisive lines, not full noisy logs unless the raw log itself is the artifact under investigation.
5. Before finalizing a debug turn, append a short "Current conclusion" and "Next step" entry to the log.

## Log Format

Use this structure for each entry:

```markdown
## Entry N - <short title>

- Time: <ISO-like timestamp or date>
- User request: <summary or quote>
- Working hypothesis: <what is being tested>
- Actions:
  - `<command or file read>` -> <important result>
- Findings:
  - <fact with evidence>
- Decision:
  - <what changed or what to do next>
- Next:
  - <next check/action>
```

## Script

Use `scripts/append_debug_log.py` to append structured entries when it is convenient:

```bash
python3 .codex/skills/engineer/debug/scripts/append_debug_log.py \
  --log logs/debug/2026-07-08-topic.md \
  --title "Check API health" \
  --user-request "Why is ready 0?" \
  --hypothesis "Ready is derived from PG files/pages state" \
  --actions-file /tmp/debug-actions.md \
  --findings-file /tmp/debug-findings.md \
  --decision "Continue by querying ingestion_file_tasks" \
  --next "Check task status distribution"
```

For small entries, using `apply_patch` directly on the markdown log is also acceptable.
