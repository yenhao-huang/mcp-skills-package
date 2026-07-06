---
name: set-daily-cron
description: >
  Configure and maintain project daily cron tasks, also referred to as
  set-cron-task, that run from the do-cron-tasks hook. Use when the user wants
  to add, remove, inspect, reset, validate, or update recurring project checks,
  including tracking git commits and GitHub issues.
---

# Set Daily Cron

Use this skill when managing project cron checks driven by
`.codex/hooks/do-cron-tasks.py`.

## When To Use

Use this skill when the user asks to:

- Create or configure a daily cron task for Codex.
- Inspect, reset, or repair the daily cron state.
- Change where cron reports are written.
- Track project git commits, dirty status, remotes, or GitHub issues.
- Debug why a cron report did or did not run.

Do not use this skill when:

- The user only wants a one-off git status or commit summary.
- The task is unrelated to recurring project checks.
- A hook or cron file should not be changed.

## Workflow

1. Read the user's request and identify whether they want inspect, create,
   update, reset, or debug behavior.
2. Read `STATE.md`; if this is a new run, reset it from
   `references/template/STATE.template.md`.
3. Read `references/cron-config.md` before editing cron task folders or hook
   behavior.
4. Read `references/rules/filetree.md` before adding, moving, or removing files
   in this skill.
5. Mark the current step `in_progress` in `STATE.md`.
6. Make the smallest change that preserves `.codex` as the project-local source
   of truth.
7. Validate with the hook command or the smallest shell command that proves the
   requested behavior.
8. Mark the step `completed`, `blocked`, or `skipped` in `STATE.md` with
   concrete evidence.

## References

- Read `references/cron-config.md` for cron state, report paths, supported task
  types, and validation commands.
- Read `references/example.md` for common request examples and expected
  outcomes.
- Read `references/rules/env.md` before changing Python/runtime assumptions.
- Read `references/rules/filetree.md` before changing this skill's directory
  layout.
- Read `references/rules/state-rules.md` when updating `STATE.md`.

## Environment

- Project cron checks are driven by `.codex/hooks/do-cron-tasks.py`.
- Project-local cron task state belongs under
  `.codex/skills/set-daily-cron/references/tasks/`.
- `STATE.md` is per-run working state and should be reset from
  `references/template/STATE.template.md` for new runs.

## Rules

- `.codex/skills/set-daily-cron/references/tasks/` is the active project-local
  cron task root.
- Each cron task lives under
  `.codex/skills/set-daily-cron/references/tasks/<task-name>/`.
- Do not write cron state or reports under `.agents`.
- Keep this `SKILL.md` focused on trigger conditions and workflow. Put task
  implementation, config, state, reports, and detailed behavior in
  `references/`.
- Do not claim a workflow step is complete unless `STATE.md` was updated with
  evidence.

## Output

Final responses should include:

- What cron behavior or state changed.
- The validation command and result.
- The active report path, when relevant.
