# State Rules

Before each new PR workflow, reset `STATE.md` from
`references/template/STATE.template.md` and fill in repository, branch, and
issue identifiers.

Use only these statuses: `pending`, `in_progress`, `completed`, `blocked`, and
`skipped`. Record commands, commit SHAs, test results, push output, PR URL, and
read-back fields as evidence. Never mark creation complete before `gh pr view`
confirms the resulting pull request.
