# Target Repository Git Rules

Use this reference when `repo-create` writes `docs/rules/git.md` for a target
repository.

## Purpose

`docs/rules/git.md` should define version-control behavior for humans and
agents. It should prevent accidental commits of unrelated work, generated
files, secrets, or pushes to shared remotes.

## Recommended Rules

Include these rules unless the user gives a different workflow:

- When a requested implementation or documentation task is complete and
  validation has passed, create a focused local git commit unless the user says
  not to commit.
- Keep each commit scoped to one self-contained feature, fix, refactor,
  documentation update, skill update, or maintenance step.
- Before committing:
  1. Check `git status --short`.
  2. Stage only files related to the completed unit of work.
  3. Inspect staged changes with `git diff --cached`.
  4. Confirm unrelated dirty files are not staged.
  5. Commit with a focused message.
- Preserve unrelated user changes. If unrelated files are dirty, leave them
  unstaged and mention them only when relevant.
- Do not commit generated outputs, cache files, local env files, secrets, model
  files, datasets, or runtime logs unless the repo explicitly tracks them.
- Never push to `origin`, `upstream`, or any shared remote unless the user
  explicitly asks for a push.

## Commit Messages

Recommend Conventional Commits:

```text
feat: add new behavior
fix: correct broken behavior
refactor: restructure code without behavior change
docs: update documentation or reports
test: add or update tests
chore: maintain tooling, packaging, or repository metadata
```

## Nested Repositories

If the repo contains nested git repositories, require agents to verify the
target repository root before staging or committing:

```bash
git rev-parse --show-toplevel
```

Run git commands from the intended repository root. A parent repository may
ignore or treat nested repositories differently, so do not assume staging from
the parent will include nested repo files.

## Remote Operations

Document the rule clearly:

```text
Local commits are allowed after validation. Network pushes require explicit
user instruction.
```
