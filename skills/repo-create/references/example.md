# Repo Create Examples

Use these examples to decide whether `repo-create` applies and what output is
expected.

## New Repository

User request:

```text
Help me set up repo rules before we start coding.
```

Expected behavior:

- Discuss the repository purpose, maintainers, languages, runtime services, and
  expected directory structure.
- Create `AGENTS.md`, `docs/rules/filetree.md`,
  `docs/rules/environment.md`, `docs/rules/git.md`, and
  `docs/feature-list.md`.
- Mark unknown runtime decisions explicitly instead of inventing them.

## Existing Repository Cleanup

User request:

```text
This repo is messy. Add rules for directories and feature tracking.
```

Expected behavior:

- Inspect existing top-level files and docs first.
- Preserve current required instructions.
- Add or revise repo governance docs without moving implementation files unless
  the user explicitly asks for a refactor.
- Define git rules that protect unrelated dirty changes and prevent accidental
  pushes.

## Feature Tracking

User request:

```text
Add a feature-list doc and keep major features maintained there.
```

Expected behavior:

- Create or update `docs/feature-list.md`.
- Track major user-visible or operational features only.
- Do not turn the file into a commit-by-commit changelog.
