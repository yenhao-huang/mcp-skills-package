---
name: executorch-pm
description: Manage ExecuTorch weekly issue selection, community message drafts, and daily PR progress. Use for the weekly 20-issue shortlist, user selection handoff to executorch-dev, templates, or read-only PR tracking; never post to the community.
---

# ExecuTorch PM

Read [references/project-policy.md](references/project-policy.md) for all runs.
Read [references/community-templates.md](references/community-templates.md)
when drafting or maintaining templates. All user-facing reports use Traditional Chinese.

## Schedule

Timezone: `Asia/Taipei`. Every Monday at 04:00 collect 20 issue candidates.
Every day at 04:00 check PR progress. On Monday perform both jobs once, with
separate outputs. Weekly collection waits for user selection before development.
Skill instructions do not activate a scheduler. Use the supported automation
API only when available; inspect existing jobs and avoid duplicates. Never
claim activation without reading back an enabled schedule. If unavailable,
record `not_enabled` and report the limitation; do not silently install cron.
See [references/schedule.json](references/schedule.json) for the confirmed intent.

## Workflow

1. Read `STATE.md`, the policy, and the latest daily records. For a new run use
   `references/template/STATE.template.md`; preserve old evidence in its dated
   archive. Determine the requested mode: shortlist, selection, templates, or
   PR check. Verify read access and output repository before acting.
2. For the weekly shortlist, query open issues in `pytorch/executorch` using
   authenticated read-only GitHub tools. Paginate, exclude PR entries and
   deduplicate. Inspect each candidate's body, full discussion and linked PRs
   before recommending it. Prefer reproducible, actionable issues without an
   active assignee or existing fix; explain exceptions, complexity, environment
   requirements and uncertainty. Rank for tractability, relevance and activity.
   Fetch additional candidates until 20 eligible issues are found or the source
   is exhausted. If fewer are eligible, report the actual count and reason;
   never pad with fabricated, closed, or already resolved issues.
3. Save the 20-item snapshot and readable table with number, title, labels,
   update time, evidence, rationale, estimated difficulty and redirect link.
   Initialize the selection record per policy. Present the shortlist in this
   chat and ask the user to select issues. End collection in
   `awaiting_user_selection`; neither the schedule nor the ranking selects work.
4. On an actual user selection, validate the numbers against the identified
   batch, record selection time and evidence, and recheck current issue status.
   Hand off only selected unresolved issues to `$executorch-dev` with batch
   path, discussion evidence and acceptance context. Do not create new chats
   unless asked. Do not select replacements for resolved issues automatically.
5. For template maintenance, edit the referenced draft templates and archive a
   copy in the dated daily run. Fill placeholders only with verified facts.
   Never post, send or request a review from a community maintainer.
6. For a daily PR check, inspect open PRs authored by `yenhao-huang` in
   `pytorch/executorch` and `yenhao-huang/executorch`, plus every PR recorded in
   prior progress files, including those now closed or merged. Paginate and
   deduplicate. Read PR state, CI checks and full review feedback; compare to
   the previous successful snapshot. Record changes, blockers and proposed
   next actions. No code changes, reruns, comments, pushes, merges or new PRs
   are authorized by this monitoring mode. Notify the user only about meaningful
   changes, completion, failure or required action; keep unchanged runs quiet.
7. Save and validate the mode's files under `executorch/<time>/` in the daily
   checkout. Check data completeness, valid JSON, source timestamps and redirect
   links. Publish only to the verified personal repository when authorized and
   verify the remote result. Update STATE.md with paths, counts, commands,
   selection state and publication evidence; report pending work honestly.
