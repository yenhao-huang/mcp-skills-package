# Community CI summary and read-only triage

Use this procedure for Result.md's `目前社群 CI 情況` column and keep any CI
conclusion repeated in the PR tracking table consistent. Do not replace the
four stage columns or their selection evidence.

## Workflow

1. Resolve the actual community PR and its current head SHA. Fetch its diff,
   current Actions runs/checks and prior investigation records. Verify that a
   run belongs to this PR/head or its associated tested merge ref; do not use
   fork CI, another PR's run or stale head results. Paginate all result lists.
2. Count **workflows**, not individual matrix jobs or a mixture of units. For
   each workflow ID and event, select its latest run for the current PR/head,
   then its latest attempt. Count completed success as `CI sucess`; count
   failure, timed_out or startup_failure as `CI fail`. Keep pending, skipped,
   cancelled, neutral and action_required separate, briefly in Evidence when
   material. Check-run-only CI not covered by this Actions inventory must be
   disclosed separately; do not count a bot's aggregate verdict as another
   workflow. State the head SHA and workflow-counting unit in Evidence. If the inventory is incomplete, use unknown counts with the last
   successful check time rather than reporting partial counts as complete.
3. For each failed workflow enumerate all failed jobs and matrix variants.
   Compare their identities against `ci-investigations.json` before deep
   investigation. An unchanged reviewed head/run/attempt/job and failure
   signature reuses its dated evidence. A different head, run, attempt, tested
   merge SHA, relevant diff, error or test stage requires rechecking. Verify
   the new error before reusing a matching older root cause; do not repeat a
   full investigation when verified current evidence is unchanged. Group failed jobs
   only when their current logs establish the same cause; retain every job
   identity/link so distinct failures are not hidden by grouping.
4. Investigate a new/unreviewed failure read-only: read the failed step, error
   context and job log/annotations, then compare the failing operation with
   the actual PR diff and relevant source. Locate the terminal fatal failure;
   a recoverable earlier curl/download error is not necessarily the root cause.
   A test job name alone, such as WebGPU, cannot prove the fix is unrelated.
   Where available, compare the same failure on base/main, prior successful
   attempts, or other verified runs. Distinguish observed facts from inference.
5. Record each judgement with the failed job URL, exact error snippet/stage,
   relevant changed/unchanged source or baseline evidence, reasoning, reviewed
   timestamp and head/run/attempt identity. Link evidence with redirect.github.com
   in published output. Raw logs and detailed investigation remain internal.
6. Render the row in this exact order (date is Asia/Taipei; spelling intentional):

   ```text
   YYYY/MM/DD; CI fail: <count>; CI sucess: <count>; Require fix: <yes/no>; Evidence: <links, error and causal reasoning>
   ```

   `yes` means evidence connects at least one current failure to our fix; name
   the required correction. `no` means no current failures were observed in a
   complete finished inventory, or every failure has evidence showing it is
   unrelated to our fix. A no verdict on unrelated failures does not mean CI is
   green: retain their fail count. Incomplete inventory, unfinished CI or an
   unclassified failure makes the verdict `unknown` unless a related failure
   already proves `yes`. Missing community PR uses `n/a`, not fork results.
   Never force yes/no when evidence is insufficient. Multiple root causes
   must all be represented; do not dismiss the entire PR from one error.
7. Save the reviewed record atomically under the existing shared run.lock
   (scheduled callers already hold it; never recursively acquire it). If the
   cache is absent, initialize it; if malformed, preserve/backup it and treat
   affected failures as unreviewed until recovery. Never silently discard older
   investigations. Fetch failures retain last verified facts and dates and add
   a dated limitation. Do not mark an unread log as investigated successfully. An unknown record
   does not complete causal triage: check for new evidence/access on later runs,
   but do not repeatedly download the same known-expired log without a change.
   Escape Markdown table pipes and keep the summary in one cell/line.

## Cache contract

`ci-investigations.json` has schema_version 1, repository pytorch/executorch and
an `investigations` array. Each record identifies PR number, head SHA, tested
merge SHA when present, workflow ID, run ID, run_attempt, job ID/name/matrix,
failed step and error signature. Include checked_at, verdict (yes/no/unknown),
evidence URLs/snippets, diff/base evidence and the causal rationale. Keep a
history of rechecks instead of overwriting a prior verdict without evidence.
Source contains only an empty installation seed; preserve installed data.

Old Result notes may seed a record only when identities and evidence can be
verified. A summary such as "curl: (22)" is not enough to infer a root cause.
For expired/inaccessible logs (for example HTTP 410), use trustworthy existing
annotations or prior same-job evidence if sufficient; otherwise explicitly
record the access limitation and `unknown`. Never manufacture a clean verdict.

Investigation is not authorization to edit code, create a fix PR, rerun or
approve Actions, alter credentials/workflows, or contact the community. Propose
any needed fix with evidence and leave execution to a separately authorized task.
