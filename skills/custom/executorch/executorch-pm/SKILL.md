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

## Prose review with Humanizer

Before rendering any HTML/PDF or finalizing Result.md and community draft prose,
apply the shared [Humanizer skill](../../../content-producer/humanizer/SKILL.md)
in embedded mode. In flat installations resolve `$humanizer` by name beside this
skill. Read its writing guide, draft the revision, compare facts and save only
the final prose. Make subjects/actions clear and remove redundant framing.

Keep issue identity/order, examples, numbers, dates, code, URLs, citations,
uncertainty and proposed-versus-verified status. Preserve all required headings,
topic/page pairs, tables, selection evidence and tracking statuses. Rebuild the
font subset after text changes, then run the HTML/PDF checks below. A wording
preview preserves historical files and does not refresh or select candidates.

## HTML-to-PDF presentation

Use the shared [frontend-slides skill](../../../content-producer/frontend-slides/SKILL.md)
for every HTML generation/update and PDF conversion. Read its provenance and
relevant rendering references. For flat installations resolve `$frontend-slides`
by name beside this skill; provision it together with `$humanizer` before a PM
run. If either dependency is missing, report the missing dependency instead of
silently skipping it. PM output and community-silence rules take precedence.
Use the existing approved design, do not repeat style questions, and do not
execute the upstream hosting/deployment helpers.
Use [template/issue-disptach.html](template/issue-disptach.html) as a reusable
reading-first example, replacing sample content, counts and dates, and adding
exactly two consecutive issue slides per candidate, following the two-page
contract below. Keep the same issue number, `(<scope>) <summary>` and relevant
redirect source links on both pages. Do not add a cover slide. Start with the index and include
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
Verify PDF page count (1 index + 2 × candidate count; 21 pages for 10 candidates), extracted text, source
links and rendered page bounds; visually inspect the PDF before publication.
Publish issue-disptach.html, issue-disptach.pdf and Result.md together. Retain
the generated HTML alongside its PDF, and keep the reusable template in the skill. PDF is static; do not describe keyboard
navigation or local editing as PDF features. Do not enable hosting.

## Two-page issue introduction

Every shortlisted issue/topic has exactly two consecutive pages, in this order:

1. **背景與解法**: four clearly labeled sections: `問題釐清` (trigger,
   observed problem and impact), `可能解法` (evidence-backed options and
   explicitly marked hypotheses), `應用場景` (who encounters it and in which
   workflow/hardware), and `專有名詞介紹` (brief plain-language definitions of
   the technical terms used for this topic). Keep each section concise.
2. **需求**: choose the structure from the actual requested behavior, using
   the issue body/discussion as evidence rather than guessing from its label:
   - **bug**: `修正前` describes the current observable failure and trigger;
     `修正後（預期）` describes the expected observable behavior for the same
     scenario. A proposed fix is not evidence that it already works.
   - **feat**: only `重點功能`, `Input`, and `Output`; explain the core capability,
     the input it accepts, and the output/result it produces. Omit secondary
     functions and implementation detail.

If the type or a required fact is unclear, label it `待釐清` and state the
missing evidence; never invent behavior, inputs, outputs or reproduction data.
Keep both pages about the same issue, retaining issue identity and source links.
The index has one entry per topic and jumps to its first page; navigation must
include both pages. Page count is `1 + 2N` for N candidates; no cover or extra
topic pages. Keep existing dispatches historical unless a refresh is requested.

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

## Issue recommendation history

Read root [issues.json](issues.json) before every shortlist search, ranking,
same-day reuse, and final publication. This is persistent recommendation state,
not a report or a replacement for Result.md. Keep it inside the installed skill;
never publish it to daily. Its repository is pytorch/executorch and issue keys
are decimal issue numbers, not PR numbers. Entries contain status, title, reason,
updated_at (Asia/Taipei ISO timestamp), evidence and append-only history.

Statuses:
- `in_progress`: user selected or development underway; exclude from new issues.
- `handled`: existing development/processed work; exclude. This does not mean
  upstream merged, fixed or Done; retain normal PR tracking separately.
- `excluded`: user explicitly rejected the issue; exclude until user restores it.
- `eligible`: explicitly restored by the user; still verify unresolved status,
  current focus and competing work before recommending it.
Absent entries are eligible for investigation, never automatically selected.

Filter in_progress, handled and excluded before ranking and recheck the final
candidate IDs against the registry. Fetch replacement candidates rather than
silently returning a repeated issue; report a shortage if necessary. Existing
fork work is also a duplicate even when it was not yet recorded. Do not assume
silence, a low ranking, an old recommendation, a closed fork PR or elapsed time
means exclusion or restoration. Never label a user-rejected issue without user
evidence. Record the user's actual rejection/re-enable wording and time in history.

On user selection set in_progress; on verified completed processing set handled;
on explicit rejection set excluded; re-enable only on explicit user request.
Preserve earlier reasons/evidence/history, especially excluded decisions, during
updates. Background discovery must not undo an existing exclusion. Registry
updates do not select new issues, start development, or stop PR tracking.
An explicit request to revisit an issue may be handled as follow-up; it does not
silently re-enable weekly recommendations.

Maintain this JSON as a data-only exception to the scheduled skill-edit ban.
Use the shared state/run.lock for interactive updates; scheduled jobs already
hold it and must not acquire it recursively. Validate and atomically replace
only issues.json. If sandbox denies access, report the pending registry update;
do not escalate or bypass security. A missing, malformed, unsupported-version,
wrong-repository or unknown-status registry blocks shortlist publication; never
treat read failure as an empty exclusion list. Do not reset it from STATE.md.
On skill upgrades, preserve the installed registry; merge new seed IDs without
overwriting existing entries/history. Record evidence rather than fabricate dates.

Historical reports remain snapshots. If today's saved shortlist includes a now
excluded entry, do not present it unchanged as the current plan: regenerate the
candidate artifacts under the usual validation rules and preserve Result.md's
actual selections/tracking. In this conversation, the earlier October 19 issue
7718 recommendation predates this registry and is now excluded from new plans.

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

Result.md contains only current actual selections, the four-stage issue progress,
and PR tracking with check times, blockers, next steps and supporting evidence.
Do not include historical candidate lists, original shortlist/history sections,
previous-report navigation, cron/sandbox diagnostics, manual-backfill narratives
or execution logs. Keep these in internal STATE.md and cron logs; issues.json
remains the exclusion registry. When carrying forward a report, remove these
legacy sections rather than copying them. API read failures relevant to a tracked
PR still belong briefly in that row, with its last successful check time.

Every Asia/Taipei calendar day must have a Result.md, even when all PR states
are unchanged or no issues are selected. Run at the confirmed daily 04:00 time.
Use executorch/YYYY-MM-DD_HHmmss/Result.md; reuse today's existing snapshot on
reruns (choose the latest if multiple exist), otherwise create one at run time.
Carry forward all tracked PRs, completed rows, actual selections and evidence
from the latest snapshot; reconcile any older rows absent from it, deduplicating
by repository/PR and preserving newer verified facts. Recheck current states.
Never overwrite prior days to record today's progress. Record report date and check time. Keep prior snapshot and original shortlist
links in internal STATE.md; relative evidence links in Result.md must resolve
from the new directory. No-change days still publish today's snapshot.
On API failure publish the snapshot with prior status/last successful check time
and a clearly dated failed-check note. Do not fabricate checks or missing dates.
Only same-day identical reruns may skip a commit. Unchanged results can remain
silent in notifications; this never suppresses the daily file output.
On shortlist days include the HTML/PDF plus Result.md; other days publish only
Result.md, without duplicating slides. A new shortlist must preserve existing
tracking/selected rows, while its new candidates remain unselected.

## Schedule

設定定時器使用 [set-daily-cron](../../../operations/set-daily-cron/SKILL.md) 的 [4 行 Codex cron 範本](../../../operations/set-daily-cron/references/template/codex.cron)。任務內容以本 skill 為準；範本與現有 launcher 擇一安裝，避免重複執行。

Timezone: `Asia/Taipei`. Every Monday at 04:00 collect 10 candidates; every day
at 04:00 check PR progress. Monday performs both jobs once. Collection waits
for user selection before development. Skill instructions do not activate a
scheduler. The user has explicitly authorized and enabled local cron for the
daily Result job; see [cron operations](references/cron-operations.md) for current
state, limitations and verification. `references/scripts/add-cron.sh` installs the daily and Monday entries.
`references/scripts/run-cron.sh` is a nine-line Codex launcher, not the report
implementation. Task logic is specified in this skill. Installation does not
prove execution or notification delivery; see cron operations for actual status.
Use the supported automation API when available, deduplicate jobs,
and read back enabled state before claiming activation. Otherwise record
`not_enabled` internally; never silently install cron. The confirmed intent is
in [references/schedule.json](references/schedule.json), never copied to daily.

## Workflow

1. Read STATE.md, the project policy, and the existing batch's PDF dispatch
   and Result.md. Use `references/template/STATE.template.md` for a new internal run.
   Determine shortlist, selection, draft maintenance, or PR-check mode.
   Verify source access and the personal output repository before mutation.
2. For a shortlist, load issues.json and apply its exclusions, then apply Focus part searches and relevance checks first,
   paginate open issues from `pytorch/executorch`, exclude PRs
   and duplicates, and read candidate bodies, all comments and linked work.
   Prefer actionable unresolved issues without an active assignee or fix PR.
   Explain exceptions and coordination needs; exclude already resolved work.
   Fetch more candidates until 10 are found or eligible results are exhausted.
   Report shortages honestly. Do not implement or select on the user's behalf.
3. Read [template/issue-disptach.html](template/issue-disptach.html) and write the
   batch's `issue-disptach.html`, then export `issue-disptach.pdf`: up to 10
   numbered topics, exactly two consecutive slides each, following the two-page
   issue introduction above. Both pages retain `(<scope>) <summary>` headings
   and a redirect issue link. Use only the active Focus part scopes: currently
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
7. Validate today's Result.md (and HTML/PDF on shortlist days), exactly two
   consecutive pages per topic, all four first-page sections, the appropriate
   bug/feat requirements on page two, `1 + 2N` total pages, index targets, headings, three-status tracking rows, four stage columns, actual
   selection evidence and redirect links. New shortlists use new timestamped
   batches; progress updates preserve historical snapshots and selection history.
   Commit and push directly to verified `yenhao-huang/daily` main, as
   authorized by the user; do not create a daily PR. Never copy JSON snapshots, STATE.md, schedules, templates,
   progress.md or development logs to daily. Record publication evidence in
   internal STATE.md. Notify only for meaningful changes or required action;
   keep unchanged daily checks quiet.

## Scheduled execution

The user requested daily progress and Monday shortlist scheduling. For `daily`,
execute Daily Result snapshot and workflow steps 6–7; for `weekly`, execute
Focus part and workflow steps 1–4 and 7, including shared Humanizer and frontend-slides.
Use the current Asia/Taipei date. The launcher holds the checkout lock: do not
call it again. Both modes preserve the latest same-day selections and artifacts;
if today's validated shortlist is already published and still passes issues.json exclusions, return its links without
generating another batch. Weekly always waits for the user's selection.

Verify this checkout's origin is https://github.com/yenhao-huang/daily.git,
branch main and no unrelated local changes. Publish only permitted daily
artifacts using HEAD:refs/heads/main; reconcile concurrent changes without reset
or force push. Never write to a community repo, initiate development, alter
cron/skill instructions/credentials (issues.json updates above are permitted), or bypass sandbox restrictions. Missing access or tools
is a blocker, not permission to change security settings.

End with Traditional Chinese verified links or the exact blocker. Cron records
this in MODE-last-message.txt. It does not deliver a message to this chat; neither
exit 0 nor a saved final response is sufficient evidence of publication.
