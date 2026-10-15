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
Taipei timestamp `YYYY-MM-DD_HHmmss` (append a short suffix on collision).
Never overwrite a prior run. Record timezone `Asia/Taipei` and capture time.
Use a persistent checkout selected from the environment; verify its origin.

Each weekly batch stores `issues.json`, `issues.md`, `selection.json`, and
`progress.md`. Store source repository and issue number separately in JSON;
use redirect links in Markdown. Preserve selection records across daily runs.
`selection.json` starts with status `awaiting_user_selection`, empty `selected`,
and null `selected_at` and `selection_evidence`. Record actual user selection,
then status `selected`; never invent an answer or treat elapsed time as consent.

Each daily check stores `prs.json` and `pr-progress.md`, comparing with the latest
successful snapshot across prior run directories. The first run is a baseline.
Track repo, PR number, head SHA, state, draft status, CI conclusions, review
state, actionable comments, updated time, blockers, and next action. Record
permission/API failures as unavailable, not as an empty result or success.

Development writes `development/<issue-number>/progress.md` in its original
selected batch, including baseline, reproducer, acceptance criteria, tests,
branch, fork PR and blockers. It may additionally create dated snapshots.
Use the code repository's report conventions as required by the copied workflow.

For publishing daily records, inspect status, stage only this run's files,
check for unsafe references and secrets, commit, and push only to the verified
`yenhao-huang/daily` remote when publication is authorized. Read the remote
commit back and record success; never claim uploaded if only locally saved.
Keep local data and report the exact blocker after a failed push; do not force.
