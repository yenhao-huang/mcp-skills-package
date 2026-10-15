---
name: executorch-pm
description: Manage ExecuTorch weekly 10-issue selection, community drafts, and daily PR tracking through issue-disptach.html, issue-disptach.pdf and Result.md. Use for shortlist generation, user selection handoff to executorch-dev, templates, or read-only progress; never post to the community.
---

# ExecuTorch PM

Read [references/project-policy.md](references/project-policy.md) for all runs.
All user-facing reports use Traditional Chinese. A shortlist batch contains only
`issue-disptach.html`, `issue-disptach.pdf` and `Result.md`, with exact spelling and capitalization.
On progress-only days, publish only Result.md.
Templates and internal schedule/state files remain inside the skill.
The exact output filename is `issue-disptach.pdf` (user spelling); do not
normalize it to issue-dispatch.pdf or retain Markdown dispatches in daily.

## HTML-to-PDF presentation

Use the bundled [frontend-slides skill](references/frontend-slides/SKILL.md)
for every HTML generation/update and PDF conversion. Read its
[SOURCE.md](references/frontend-slides/SOURCE.md) for provenance and PM overrides,
then its SKILL.md and relevant HTML/viewport references before rendering.
The upstream source is https://github.com/zarazhangrui/frontend-slides, pinned
to commit 9906a34d640d2111f724544cbc50f7f130569ae1. No separate installation or
network fetch is required. PM output and community-silence rules take precedence.
Use [template/issue-disptach.html](template/issue-disptach.html) as a reusable
reading-first example, replacing sample content, counts and dates, and adding
one issue slide per candidate. Keep the issue number, `(<scope>) <summary>`,
問題釐清, 可能解法 and all relevant redirect source links. Do not add a cover slide. Start with the index and include
a link to Result.md. Preserve source facts when converting an existing batch;
conversion alone does not authorize fresh selection or a shortlist refresh.

Generate a single self-contained HTML with inline CSS/JS, fixed 1920×1080 stage
scaling, keyboard/touch navigation, reduced-motion support and readable type.
Embed required font glyphs for the final content (regenerate the font subset
when text changes), preserve embedded font and upstream CSS license notices,
and avoid runtime CDN dependencies. Local text editing must stay local, never
write to GitHub, and provide HTML download. Validate rendered bounds and inspect
desktop/phone screenshots before conversion. Export the HTML with a Chromium-based
browser PDF API (for example Playwright page.pdf), using print backgrounds and
preferCSSPageSize. Keep the fixed 16:9 page size and one slide per page; print
CSS must reveal every slide, disable animations and hide editing/navigation
controls. Wait for document.fonts.ready and clear slide inert/aria-hidden state.
Preserve selectable Chinese text and clickable redirect source links. Make the
Result.md link an absolute URL to this batch in the personal daily repository.
Verify PDF page count (index + candidate count), extracted text, source
links and rendered page bounds; visually inspect the PDF before publication.
Publish issue-disptach.html, issue-disptach.pdf and Result.md together. Retain
the generated HTML alongside its PDF, and keep the reusable template in the skill. PDF is static; do not describe keyboard
navigation or local editing as PDF features. Do not enable hosting.

## Focus part

Current focus scopes (editable here; this is the source of truth):

- `build operator`: operator/kernel implementation, missing operator support,
  registration, selective build, and operator-specific build/link integration.
  This is one combined category, not separate build and operator scopes.
- `quantization`: quantizers, calibration, quantized operators, precision/dtype
  behavior, accuracy regressions, and quantized backend lowering.

Focus controls candidate search and eligibility, not just the final heading.
Search each category separately with several related terms; do not require the
literal phrase "build operator". For example, use GitHub issue searches such as
`repo:pytorch/executorch is:issue is:open kernel`, `... operator`,
`... "selective build"`, `... quantization`, `... quantizer`,
`... int8`, and `... calibration` (expand `...` to the same repo/type/state
filters). Inspect actual labels first before using label filters. Read bodies,
comments and linked work to confirm relevance; keyword hits alone do not qualify.

Exclude general CI/dependency maintenance, unrelated packaging, generic memory
planning and unrelated inference issues. An otherwise general issue qualifies
only if its concrete unresolved work fits one of the two focus scopes; explain
that relationship in 問題釐清. Search both scopes, deduplicate overlaps, choose
one primary scope per item and rank by evidence and tractability. No fixed
five/five quota is required. If fewer than 10 eligible issues remain, report the
count and shortage; never fill with unrelated issues or silently broaden focus.

When the user changes focus, update this section and the template's focus line.
Existing dispatches remain historical snapshots unless a refresh is requested.
Focus never removes selected issues from Result.md or stops their PR tracking.

## PR tracking summary

Maintain a user-facing `PR 追蹤表` in Result.md, alongside the existing four-stage
issue detail. Its progress column has exactly three values:

- `未發 PR`: selected work has no verified community PR; a personal fork PR alone
  remains in this state.
- `PR 未 merge`: a community PR exists but merged is false, including drafts and
  closed-unmerged PRs. Explain closure/blockers in notes; never call them Done.
- `Done`: the same community PR has verified merged=true / mergedAt evidence.

Columns: `追蹤項目 | 社群 PR | 進度 | 目前狀況／下一步 | 查核時間`.
Record check timestamps in Asia/Taipei and use redirect links, including comment
anchors. User-provided PRs are tracked even outside the current shortlist/focus;
tracking does not select a shortlist issue or authorize development. Deduplicate
by repository and PR number; keep one row per PR and retain completed rows.
For selected issues without a PR, use an issue row and replace/update it when the
corresponding PR is verified. Read every batch's Result.md to discover existing
tracked PRs and carry them into today's snapshot under the daily rules below.
On read failure retain the prior status and last successful check timestamp;
mark the failed check/uncertainty in notes, never invent a fourth status or Done.
Review approval and successful CI do not imply merge. Preserve the four-stage
selected-issue table separately; do not infer its history from a supplied PR.

## Daily Result snapshot

Every Asia/Taipei calendar day must have a Result.md, even when all PR states
are unchanged or no issues are selected. Run at the confirmed daily 04:00 time.
Use executorch/YYYY-MM-DD_HHmmss/Result.md; reuse today's existing snapshot on
reruns (choose the latest if multiple exist), otherwise create one at run time.
Carry forward all tracked PRs, completed rows, actual selections and evidence
from the latest snapshot; reconcile any older rows absent from it, deduplicating
by repository/PR and preserving newer verified facts. Recheck current states.
Never overwrite prior days to record today's progress. Record report date,
check time, prior Result.md link and original shortlist link; relative links must
resolve from the new directory. No-change days still publish today's snapshot.
On API failure publish the snapshot with prior status/last successful check time
and a clearly dated failed-check note. Do not fabricate checks or missing dates.
Only same-day identical reruns may skip a commit. Unchanged results can remain
silent in notifications; this never suppresses the daily file output.
On shortlist days include the HTML/PDF plus Result.md; other days publish only
Result.md, without duplicating slides. A new shortlist must preserve existing
tracking/selected rows, while its new candidates remain unselected.

## Schedule

Timezone: `Asia/Taipei`. Every Monday at 04:00 collect 10 candidates; every day
at 04:00 check PR progress. Monday performs both jobs once. Collection waits
for user selection before development. Skill instructions do not activate a
scheduler. The user has explicitly authorized and enabled local cron for the
daily Result job; see [cron operations](references/cron-operations.md) for current
state, limitations and verification. Weekly shortlist remains disabled.
Use the supported automation API when available, deduplicate jobs,
and read back enabled state before claiming activation. Otherwise record
`not_enabled` internally; never silently install cron. The confirmed intent is
in [references/schedule.json](references/schedule.json), never copied to daily.

## Workflow

1. Read STATE.md, the project policy, and the existing batch's PDF dispatch
   and Result.md. Use `references/template/STATE.template.md` for a new internal run.
   Determine shortlist, selection, draft maintenance, or PR-check mode.
   Verify source access and the personal output repository before mutation.
2. For a shortlist, apply Focus part searches and relevance checks first,
   paginate open issues from `pytorch/executorch`, exclude PRs
   and duplicates, and read candidate bodies, all comments and linked work.
   Prefer actionable unresolved issues without an active assignee or fix PR.
   Explain exceptions and coordination needs; exclude already resolved work.
   Fetch more candidates until 10 are found or eligible results are exhausted.
   Report shortages honestly. Do not implement or select on the user's behalf.
3. Read [template/issue-disptach.html](template/issue-disptach.html) and write the
   batch's `issue-disptach.html`, then export `issue-disptach.pdf`: up to 10 numbered issue slides with
   `(<scope>) <summary>` headings,
   each with a redirect issue link, `問題釐清` and `可能解法`. Use only the active Focus part scopes: currently
   `build operator` or `quantization`. Do not include the word `title` or a
   colon after the closing parenthesis. Ground the diagnosis in the discussion, mark proposed solutions as
   hypotheses, and mention hardware, prior fixes and remaining uncertainty.
4. Initialize `Result.md` from [template/Result.md](template/Result.md) with an
   waiting-for-selection statement for new candidates. Preserve prior actual
   selections and PR tracking rows; use an empty table only on the first run.
   Present the dispatch and wait. On actual selection, record the chosen issue,
   time and user evidence in Result.md, recheck its current state, and hand off
   only selected unresolved issues to `$executorch-dev` with the batch path.
   Do not replace resolved selections without another user choice.
5. For drafting, use [references/community-templates.md](references/community-templates.md).
   Maintain templates inside the skill only. Never archive templates to daily,
   send notices, request reviews or post community comments.
6. For daily tracking, update the three-status PR tracking summary above.
   Read selected issues and associated fork/community PRs
   from Result.md, including previously tracked PRs now closed or merged. Read
   all relevant CI/review changes and publish today's Result.md snapshot,
   even if no status changed. Preserve prior days.
   Use exactly four stages: `選擇 issue`, `issue 開發`, `用戶在社群寄送 PR`,
   `該 PR 被 merge`. Treat fork PRs as development evidence only. Stage three
   requires a verified community PR submitted by the user; stage four requires
   that same PR's merged state. Neither a closed PR nor a merged fork PR counts.
   If the user reports a new PR, verify its issue relationship and destination
   read-only before recording it. Record unavailable checks as unknown; retain
   prior facts. Do not initiate development or perform any community writes.
7. Validate today's Result.md (and HTML/PDF on shortlist days), counts, headings, three-status tracking rows, four stage columns, actual
   selection evidence and redirect links. New shortlists use new timestamped
   batches; progress updates preserve historical snapshots and selection history.
   Commit and push directly to verified `yenhao-huang/daily` main, as
   authorized by the user; do not create a daily PR. Never copy JSON snapshots, STATE.md, schedules, templates,
   progress.md or development logs to daily. Record publication evidence in
   internal STATE.md. Notify only for meaningful changes or required action;
   keep unchanged daily checks quiet.
