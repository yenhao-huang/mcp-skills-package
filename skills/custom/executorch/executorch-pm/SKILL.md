---
name: executorch-pm
description: Manage ExecuTorch weekly 10-issue selection, community drafts, and daily PR tracking through issue-dispatch.md and Result.md. Use for shortlist generation, user selection handoff to executorch-dev, templates, or read-only progress; never post to the community.
---

# ExecuTorch PM

Read [references/project-policy.md](references/project-policy.md) for all runs.
All user-facing reports use Traditional Chinese. The daily batch contains only
`issue-dispatch.md` and `Result.md`, with exact spelling and capitalization.
Templates and internal schedule/state files remain inside the skill.

## Schedule

Timezone: `Asia/Taipei`. Every Monday at 04:00 collect 10 candidates; every day
at 04:00 check PR progress. Monday performs both jobs once. Collection waits
for user selection before development. Skill instructions do not activate a
scheduler. Use the supported automation API when available, deduplicate jobs,
and read back enabled state before claiming activation. Otherwise record
`not_enabled` internally; never silently install cron. The confirmed intent is
in [references/schedule.json](references/schedule.json), never copied to daily.

## Workflow

1. Read STATE.md, the project policy, and the existing batch's two Markdown
   files. Use `references/template/STATE.template.md` for a new internal run.
   Determine shortlist, selection, draft maintenance, or PR-check mode.
   Verify source access and the personal output repository before mutation.
2. For a shortlist, paginate open issues from `pytorch/executorch`, exclude PRs
   and duplicates, and read candidate bodies, all comments and linked work.
   Prefer actionable unresolved issues without an active assignee or fix PR.
   Explain exceptions and coordination needs; exclude already resolved work.
   Fetch more candidates until 10 are found or eligible results are exhausted.
   Report shortages honestly. Do not implement or select on the user's behalf.
3. Read [template/issue-dispatch.md](template/issue-dispatch.md) and write the
   batch's `issue-dispatch.md`: 10 numbered `title <scope>: <summary>` entries,
   each with a redirect issue link, `問題釐清` and `可能解法`. Use scopes such as
   perf, inference, operator, export, runtime, memory, backend, build, ci or
   tooling. Ground the diagnosis in the discussion, mark proposed solutions as
   hypotheses, and mention hardware, prior fixes and remaining uncertainty.
4. Initialize `Result.md` from [template/Result.md](template/Result.md) with an
   empty selected-issue table and an explicit waiting-for-selection statement.
   Present the dispatch and wait. On actual selection, record the chosen issue,
   time and user evidence in Result.md, recheck its current state, and hand off
   only selected unresolved issues to `$executorch-dev` with the batch path.
   Do not replace resolved selections without another user choice.
5. For drafting, use [references/community-templates.md](references/community-templates.md).
   Maintain templates inside the skill only. Never archive templates to daily,
   send notices, request reviews or post community comments.
6. For daily tracking, read selected issues and associated fork/community PRs
   from Result.md, including previously tracked PRs now closed or merged. Read
   all relevant CI/review changes and update the same Result.md in place.
   Use exactly four stages: `選擇 issue`, `issue 開發`, `用戶在社群寄送 PR`,
   `該 PR 被 merge`. Treat fork PRs as development evidence only. Stage three
   requires a verified community PR submitted by the user; stage four requires
   that same PR's merged state. Neither a closed PR nor a merged fork PR counts.
   If the user reports a new PR, verify its issue relationship and destination
   read-only before recording it. Record unavailable checks as unknown; retain
   prior facts. Do not initiate development or perform any community writes.
7. Validate the two output files, counts, headings, four stage columns, actual
   selection evidence and redirect links. New shortlists use new timestamped
   batches; progress updates preserve the existing batch and selection history.
   Publish only to the verified personal repository via an authorized task
   branch and PR. Never copy JSON snapshots, STATE.md, schedules, templates,
   progress.md or development logs to daily. Record publication evidence in
   internal STATE.md. Notify only for meaningful changes or required action;
   keep unchanged daily checks quiet.
