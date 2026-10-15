# State Rules

Use `STATE.md` as the resumable record for one issue-resolution run.

1. For a new issue, copy `references/template/STATE.template.md` to
   `STATE.md`, then fill in the run metadata.
2. Set a step to `in_progress` before starting it.
3. Mark a step `completed` only with concrete evidence such as an issue URL,
   test command and result, commit hash, pull request URL, or CI status.
4. Use `blocked` only when progress cannot continue safely, and record the
   exact blocker and required next action.
5. Do not mark later lifecycle steps complete while an earlier required step
   remains pending or blocked.
6. Update evidence after any new change invalidates an earlier test or review.
7. Do not place secrets, tokens, or sensitive private issue content in state.
8. When the discussion check finds the issue already resolved, mark step 1
   `completed` with the comment or PR link as evidence, mark the remaining
   steps `blocked` with the note "already resolved, bypassed", and do not
   advance to implementation.
