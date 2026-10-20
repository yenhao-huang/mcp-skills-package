# ExecuTorch project policy

## Destinations and community silence

- Read community issues, PRs, discussions, CI and reviews. Never write to any
  community repository: no comments, review replies, PRs, issues, labels,
  assignments, reactions, state changes, review requests, or pushes.
- Do not cause indirect cross-references. In any published artifact, including
  commit messages, PR titles/bodies, daily reports and draft templates, never
  use bare community `owner/repo#number`, canonical GitHub issue/PR URLs,
  closing keywords, or autolinking references. Use this form:

  `Related issue: [ExecuTorch #1234](https://redirect.github.com/pytorch/executorch/issues/1234)`

- Use the redirect host for community PR links too. Sanitize copied quotations
  and source text before publishing. Avoid bare issue numbers in fork PR text
  when they might resolve to an unintended issue. The redirect convention is
  required by the user; do not test its behavior by publishing to a community.
- Inspect the entire outgoing diff and all commit messages before a push or PR
  write, not just the description. Stop the write if unsafe references remain.
- Verify the exact destination of each write. Development branches and PRs go
  only to `yenhao-huang/executorch`; progress goes to `yenhao-huang/daily`.
  No automatic merges, force pushes, branch deletions or upstream writes.
- Drafting is permitted; never send the community templates or reviewer notices.

## Storage and handoff

Use `yenhao-huang/daily`, directory `executorch/<time>/`, where `<time>` is a
Taipei timestamp `YYYY-MM-DD_HHmmss` (append a suffix on collision).
Publish a Result.md snapshot every Asia/Taipei calendar day, even without status
changes. Reuse today's directory on reruns or create YYYY-MM-DD_HHmmss at run
time. Carry forward tracking and selections; preserve prior days unchanged.
Follow PM's Daily Result snapshot rules for cross-batch reconciliation and links.

A shortlist batch contains exactly three user-facing files (HTML source + PDF dispatch + Markdown results):

- `issue-disptach.html`: the self-contained generated presentation used for PDF export.
- `issue-disptach.pdf`: one index plus exactly two pages per issue/topic (up to
  10 topics, 21 pages total), exported from the PM skill's
  `template/issue-disptach.html`. Both pages retain `(<scope>) <summary>` and
  redirect source links. Page one covers 問題釐清、可能解法、應用場景、專有名詞介紹;
  page two covers 需求: bugs compare 修正前 and 修正後（預期）, while features
  explain only 重點功能、Input、Output. Follow PM's two-page contract.
- `Result.md`: actual selected issues and the four stages from the PM skill's
  `template/Result.md`: 選擇 issue、issue 開發、用戶在社群寄送 PR、該 PR 被 merge.

Before any selection, Result.md explicitly says no issues have been selected and
has no selected-issue rows. Later shortlists preserve existing selections and PR
tracking; progress-only days contain Result.md alone. Only real user selection creates a row, with time/evidence.
Never treat ranking, silence or elapsed time as selection.

Development updates only the selected issue row and concise evidence in
Result.md. Keep reproduction logs, tests, reports and branch details in the
code repository under its existing conventions; link when useful. Do not
publish development directories, progress.md, JSON snapshots, schedule.json,
STATE.md, or template files to daily. Templates and scheduling intent stay in
the skill. Internal caches may be local but must not be staged to daily.

Fork PRs are evidence for issue 開發 only. Community submission belongs to the
user: read back the actual community PR before completing stage three, and
verify that PR's mergedAt/merged state before completing stage four. Closed
without merge is not completion. Failed API reads are unknown, never success.
Track blockers and next actions as notes, not extra stages.

Before publishing, inspect the full diff and commit messages for unsafe
references and secrets. Stage only the intended batch files. The user explicitly
authorizes direct commits and normal pushes to `main` in `yenhao-huang/daily`;
no task branch or pull request is needed for this repository. Verify the remote
repository, fetch main and preserve unrelated changes before publishing. Use
an explicit destination (`git push origin HEAD:refs/heads/main`) and verify the
remote commit and the expected daily files afterward. If main advances, reconcile
safely before retrying; never force-push. Publish today's snapshot even when statuses are unchanged; skip only identical
same-day reruns.

This exception applies only to daily records. The skill-package repository
still requires task-created branches and pull requests, and community writes
remain forbidden. Keep local files and report the exact blocker if publishing
fails; never claim uploaded when only locally saved.

## PR summary tracking

Result.md also contains a PR tracking table with exactly `未發 PR`, `PR 未 merge`,
and `Done`. Done requires verified community merge; closed without merge remains
PR 未 merge with a note. Track user-supplied PRs independently of shortlist selection
and preserve the four-stage detail. Read failures retain prior status and mark
uncertainty in notes. PM owns the summary format and cross-batch discovery rules.
