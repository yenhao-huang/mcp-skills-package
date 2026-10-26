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

Use `yenhao-huang/daily`, directory `executorch/<id>_<time>/`, where `<id>` is
exactly six decimal digits and `<time>` is an Asia/Taipei timestamp
`YYYY-MM-DD_HHmmss`. GitHub's ascending filename order must show newer batches
first. Apply these allocation rules under the existing shared run lock (do not
acquire it recursively when the launcher already holds it):

- Seed an empty archive at `999999`. For a user-authorized migration of existing
  timestamp-only directories, sort them by timestamp from oldest to newest and
  assign `999999`, `999998`, etc. once. Never renumber already prefixed batches.
  If prefixed and legacy directories coexist, do not seed a second sequence;
  require an explicit migration mapping before allocating or moving old IDs.
- For each new batch, allocate `min(existing prefixed IDs) - 1`, formatted with
  six digits; use all existing prefixed directories to avoid collisions. For
  example, `999997_2026-10-17_040002` sorts above
  `999998_2026-10-16_040001`. If the minimum is `000000`, stop and report ID
  exhaustion; never wrap, reuse an ID, or expand the width silently.
- Reusing today's snapshot keeps its full existing directory name and ID.
  An explicit new shortlist/refresh allocates a new ID even on the same day.
  A timestamp collision does not require renaming an older batch: the new ID
  makes the full directory unique.
- For discovery, strip only a leading six-digit ID plus underscore, then parse
  the timestamp. Accept legacy `YYYY-MM-DD_HHmmss` names and their documented
  collision suffixes during migration. Choose the latest report by timestamp,
  never by lexicographic maximum of the full name: larger IDs are older.
- Store the full directory name in Result.md's batch field, HTML batch metadata,
  archive paths and new publication-ledger `batch` values. Build Result/HTML/PDF
  URLs from this exact name, not from the timestamp alone.
- When a directory is explicitly migrated, update repository-local links and
  PDF URI annotations to the migrated paths. Resolve old ledger `batch` and
  `artifact_url` paths by their unique timestamp suffix, updating only path
  fields under the lock. Preserve candidate IDs, recommendation history, issue
  selection/handling state and check timestamps; do not clear a ledger to fix
  a path. If no unique directory matches, report the ambiguity instead of
  inventing a replacement. Links pinned to historical commits remain valid and
  must not be rewritten to paths that did not exist in those commits.

Publish a Result.md snapshot every Asia/Taipei calendar day, even without status
changes. Reuse today's directory on reruns or allocate a new prefixed batch at
run time. Carry forward tracking and selections; preserve prior days' contents.
Directory/metadata/link changes to historical batches require an explicit
migration request. Do not perform additional backfills or reorder historical
batches merely because the naming rule changed. Follow PM's Daily Result
snapshot rules for cross-batch reconciliation and links.

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
The selected-issue table's last column is `目前社群 CI 情況`: a dated current
community-CI summary with workflow fail/success counts, a fix-relevance verdict
and linked evidence, following ci-triage.md. Keep development history in internal
records and the code report; do not fill this cell with old fork/test narratives.
New or unreviewed failures authorize read-only investigation only. Missing logs
or permissions require an unknown verdict, not an unsupported claim of no fix.
Preserve investigation records across daily runs and synchronize any duplicated
CI conclusion in the PR tracking table.

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
