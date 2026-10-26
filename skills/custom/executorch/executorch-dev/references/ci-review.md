# Read-only community CI review

PM owns inventory/counts and publishing. Dev owns the causal assessment.
Read project-policy.md first. Accept selected PR/head, all failed job identities,
diff/base, cached evidence and access limits. Check actual current identities;
never equate a bot label or a job name with a root cause.

## Workflow

1. Round 1 — establish facts: inspect failed steps, terminal error context and
   changed source; enumerate competing hypotheses. Reflect on missing evidence,
   then record the next deeper probe and what could disprove the leading cause.
2. Round 2 — challenge the explanation: follow the failing call/build path,
   compare base/main, earlier attempts or an independently verified equivalent
   job where available. Reflect on counterevidence and select another probe.
3. Round 3 — resolve remaining risk: inspect shared helpers, registrations,
   dependency/build interactions or alternate primary evidence targeting the
   unresolved hypothesis. Reflect again and state what could change the verdict.
   Add rounds when a material accessible gap remains. Each round must add a new
   observation or a documented distinct probe/result; repeating the same query,
   retrying the same unavailable log, or three paraphrases is not three rounds.
4. Return every failed job's identity and classification to PM, plus the PR-wide
   probability that at least one observed failure requires correcting our change.
   Use `Require fix: <P(true)>% (true|false)`; above 50% means true, below 50%
   false. Never output unknown or exactly 50%; choose 51/49 for nearly balanced
   evidence and label it weak. This is subjective confidence, not a measurement.
   Do not average away one proven code-related failure among environment failures.
   No observed failures with pending approval is only a tentative false direction,
   not proof of passing CI. Keep pending/non-success statuses visible.
5. Evidence for the report is one short sentence, preferably <=100 Chinese
   characters excluding URLs, stating the cause or leading hypothesis, material
   limitation and 1–2 primary links. Put full analysis in internal cache/state:
   each round's observation, source, reflection, next probe/result; head/run/
   attempt/job IDs, failed step/signature, direction, p_require_fix_true,
   review_complete and checked_at. Preserve prior records. Unread logs remain
   unread; unavailable probes cannot be called successful verification.

Existing completed three-round reviews can be reused for identical identities
and unchanged evidence. New head, attempt, signature, relevant source or contrary
evidence requires rechecking. If prior records lack the rounds, complete them.
Do not modify code or run a reproducer that changes the environment without a
separately authorized implementation task. Never rerun/approve CI or post to
the community. A recommended correction is a handoff, not an implemented fix.
