---
name: solve-issue
description: Resolve a GitHub issue end to end by reading its requirements, implementing and testing the change, reviewing the result, committing it, creating a pull request, and following through on CI and review. Use when the user asks to solve, fix, implement, or continue work on a specific GitHub issue.
license: MIT; adapted from canpok1/claude-code-plugins
---

# Solve Issue

Resolve one GitHub issue through a verified pull request. Treat the issue
number or URL supplied by the user as the target; if none is supplied, identify
the issue from the current conversation or ask the user before changing code.

## Notes

1. Never write anything to the upstream/public community repository (社群
   repo). This covers pull requests, issues, issue and pull-request comments,
   review replies, labels, assignees, and state changes — not pull requests
   alone. Send every such action to the user's designated fork instead:

   | community repo | fork to use |
   |---|---|
   | `nvidia/tensorrt` | `yenhao-huang/TensorRT` |
   | `pytorch/executorch` | `yenhao-huang/executorch` |

   For a community repository not listed here, ask for the fork before writing
   anything. Verify the destination before creating or retargeting a write; do
   not infer it from the issue URL or from GitHub's default upstream selection,
   and pass `--repo <fork>` explicitly rather than relying on the working
   directory's remote, whose `upstream` may point at the community repository
   with push enabled.

   Drafting a comment, review reply, or issue body for a community thread and
   handing the text back to the user is in scope. Posting it is not.

## Definition Of Done

A solved issue is a pull request on the user's designated fork, not a commit on
this machine. The run is complete only when both of these are true, and the
final report carries both:

1. the branch exists on the fork (`git ls-remote --heads <fork-remote>
   <branch>` finds it); and
2. a pull request for that branch exists on the fork, identified by URL.

Commits that exist only in the local repository are an unfinished run. Report
that state as `blocked` or `in_progress` in `STATE.md` with the reason, and say
plainly that nothing was published. Never describe such a run as complete,
delivered, or done, and never close it by offering to push as an optional extra
step.

Steps 5 and 6 are pre-authorized by this workflow: pushing a feature branch to
the designated fork and opening a pull request against that fork need no
further approval from the user, because the user asked for the issue to be
solved. Ask only when the fork is unknown, or when a push would overwrite
existing remote history.

## Workflow

1. Read `STATE.md`, reset it from `references/template/STATE.template.md` for
   a new run, and record the repository and target issue.
2. Use `github-issues` to fetch the issue, labels, comments, linked work, and
   current state. Stop and ask before proceeding if the issue is closed, cannot
   be identified, or has materially ambiguous requirements.
3. Read the full discussion before writing any code: every comment, linked or
   merged pull request, duplicate-issue link, and commit that references the
   issue number. Pay particular attention to the original reporter's own
   follow-up comments — reporters often post a workaround, root cause, or a
   working fix themselves after opening the issue, and that can be the
   fastest path to a correct answer or proof the issue no longer needs work.
   Determine whether the issue is already resolved — fixed on a branch,
   closed via a merged PR, declared a duplicate, resolved by a workaround the
   reporter confirmed works, or otherwise handled by someone else.
   - If already resolved: do not implement anything. Record the finding and
     its evidence (comment or PR link) in `STATE.md` as the run's outcome.
     If this issue was chosen from a backlog or list rather than pinned by
     the user, pick the next unresolved candidate from that list and repeat
     this check; if the user pinned this specific issue, report the finding
     to the user and ask how to proceed instead of silently substituting a
     different issue.
   - If not resolved, continue to implementation — but reuse the reporter's
     workaround or diagnosis as a starting point when it points to the fix.
4. Read the repository instructions and
   [references/report_template.md](references/report_template.md). Create an
   issue report at the repository's established report location (for example,
   `docs/howard/<issue-number>.md`) and record its path in `STATE.md`. Goal and
   report files always live under the repository's `docs/` tree — goal files in
   `docs/goals/`, reports at the established report location — never at the
   repository root and never in a top-level `goals/` directory. A repository
   that documents its own layout wins; follow it and record the chosen path.
   Before implementation, organize acceptance criteria from the issue and
   discussion: give each criterion an ID, expected behavior, verification
   method, and required evidence. Then use `dev` with these ordered development
   substeps:

   1. **reproduce**: Run the smallest reproducer on the unmodified baseline.
      Record the commit, environment, exact command, expected versus actual
      behavior, exit code, and relevant output. If reproduction is blocked or
      unsuccessful, record the limitation and investigate before claiming a
      reproduced bug; never invent baseline evidence.
   2. **dev**: Diagnose the root cause and implement the smallest complete fix.
      Explain the changed behavior and map the changes to acceptance criteria
      in the report. Review the diff and resolve actionable findings.
   3. **regression test**: Add or update a focused regression test for the
      original failure and run it against both baseline and fixed code where
      feasible, recording failure before and success after. Rerun the original
      reproducer on the fix and check relevant adjacent behavior. Record exact
      commands, results, and any checks that could not run with their reasons.

   Complete the report's fixed demo and acceptance table with evidence for
   every criterion. Mark each as passed, failed, or blocked; unexecuted checks
   are blocked, not passed. Do not claim acceptance while any required
   criterion is failed or blocked. Keep `STATE.md` aligned with this evidence.
5. Commit, then push the branch to the user's designated fork. Confirm the
   remote points to that fork, not to the community repository, and push
   without pausing for approval — this step is pre-authorized. Read the push
   back with `git ls-remote --heads <fork-remote> <branch>` and record the
   result in `STATE.md`. A run that ends here has not solved the issue.
6. Use `github-pr-workflow` to open a pull request only against that fork,
   linking the issue and acceptance report and reporting validation
   evidence and remaining blockers. Specify the destination explicitly (for example, `gh pr create --repo
   yenhao-huang/TensorRT`) so the PR cannot default to the community upstream.
   Opening this fork pull request is pre-authorized; do not stop to ask for it.
   If the fork is unknown, ask for it before publishing.
   Then read the pull request back with `gh pr view --repo <fork> <number>
   --json url,state,headRefName` and record the URL and state in `STATE.md`;
   an unverified `gh pr create` is not evidence that the PR exists.
   Do not offer or request approval to publish a community PR as part of this
   workflow.
7. Monitor CI and review feedback on the fork's pull request, address failures
   or actionable comments, and merge only when the user explicitly requested
   merging or repository policy clearly grants that authority. Review feedback
   that lives on a community thread is answered by handing a draft reply to the
   user, never by posting to that thread.
8. Summarize the result, validation, and any follow-up or residual risk, and
    quote the fork branch name and the pull request URL from step 6. Mark the
    run complete in `STATE.md` only when the `Definition Of Done` above holds;
    if it does not, state which of the two conditions is missing.

## Guardrails

- Use a purpose-built installed skill for each workflow phase when available.
- Keep concise work notes in `STATE.md` at meaningful checkpoints so later
  turns can resume without reconstructing context.
- After a command returns empty or unexpected output, run a read-only state
  check before taking the next mutating action. For example, retry `gh issue
  view` or `gh pr view` with `--json`, inspect `git status` after file-moving
  commands, and verify a remote branch before deleting it.
- If code changes, make each commit a coherent logical unit and validate it in
  proportion to risk.
- Committing, pushing, and opening the PR in the user's designated fork are in
  scope when solving an issue. Never create or retarget a PR against the
  upstream/public community repository, and never comment on, label, or change
  the state of anything there; follow `Notes` and explicitly verify every write
  destination.
- Do not merge, close an issue, force-push, delete a branch, or perform another
  consequential remote action unless the user's request or established
  repository workflow authorizes it. This does not cover pushing the feature
  branch to the designated fork or opening a pull request against that fork:
  both are authorized by this workflow and are required by
  `Definition Of Done`. It does cover every write to the community repository,
  which stays forbidden regardless of authorization.
- Never start implementation before reading the issue's comments and linked
  work in full. An issue whose discussion shows it is already fixed,
  duplicated, or resolved elsewhere is a bypass, not a coding task: record it
  and move to the next candidate instead of re-solving already-solved work.

## Provenance

Adapted from `plugins/base-tools/skills/solve-issue` in
`canpok1/claude-code-plugins` at commit
`04f81f5ffc0d83dab157171203520e1d635742cb`. See
`references/LICENSE.txt` for the upstream MIT license.
