---
name: solve-issue
description: Resolve a GitHub issue end to end by reading its requirements, implementing and testing the change, reviewing the result, committing it, creating a pull request, and following through on CI and review. Use when the user asks to solve, fix, implement, or continue work on a specific GitHub issue.
license: MIT; adapted from canpok1/claude-code-plugins
---

# Solve Issue

Resolve one GitHub issue through a verified pull request. Treat the issue
number or URL supplied by the user as the target; if none is supplied, identify
the issue from the current conversation or ask the user before changing code.

## Workflow

1. Read `STATE.md`, reset it from `references/template/STATE.template.md` for
   a new run, and record the repository and target issue.
2. Use `github-issues` to fetch the issue, labels, comments, linked work, and
   current state. Stop and ask before proceeding if the issue is closed, cannot
   be identified, or has materially ambiguous requirements.
3. Read the repository instructions and use `dev` to investigate, implement,
   and test the smallest complete change that satisfies the issue.
4. Review the changed code for correctness, regressions, security, performance,
   cross-platform behavior, and unnecessary complexity. Fix findings and rerun
   relevant validation.
5. Use `git-commit` to create focused commits that reference the issue. Never
   include unrelated user changes.
6. Use `github-pr-workflow` to push the branch and open a pull request that
   links the issue and reports validation evidence.
7. Monitor CI and review feedback, address failures or actionable comments,
   and merge only when the user explicitly requested merging or repository
   policy clearly grants that authority.
8. Summarize the result, validation, pull request state, and any follow-up or
   residual risk. Mark the run complete in `STATE.md` only when the requested
   lifecycle is actually finished.

## Guardrails

- Use a purpose-built installed skill for each workflow phase when available.
- Keep concise work notes in `STATE.md` at meaningful checkpoints so later
  turns can resume without reconstructing context.
- After a command returns empty or unexpected output, run a read-only state
  check before taking the next mutating action. For example, retry `gh issue
  view` or `gh pr view` with `--json`, inspect `git status` after file-moving
  commands, and verify a remote branch before deleting it.
- If code changes, make each commit a coherent logical unit and validate it in
  proportion to risk.
- Do not merge, close an issue, force-push, delete a branch, or perform another
  consequential remote action unless the user's request or established
  repository workflow authorizes it.

## Provenance

Adapted from `plugins/base-tools/skills/solve-issue` in
`canpok1/claude-code-plugins` at commit
`04f81f5ffc0d83dab157171203520e1d635742cb`. See
`references/LICENSE.txt` for the upstream MIT license.
