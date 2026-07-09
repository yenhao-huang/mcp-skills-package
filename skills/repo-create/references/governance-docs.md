# Repository Governance Docs

Use these patterns when creating or updating repo-management docs. Adapt them to
the actual repository instead of copying blindly.

## AGENTS.md

Purpose: teach developers and agents how to operate in the repo.

Recommended sections:

- `Repository Purpose`: what the repo is for and what success looks like.
- `Start Here`: files to read before making changes.
- `Directory Rules`: require reading `docs/rules/filetree.md` before creating,
  moving, or deleting directories.
- `Environment Rules`: require reading `docs/rules/environment.md` before
  installing packages, changing runtimes, starting services, or assuming paths.
- `Feature Tracking`: require updating `docs/feature-list.md` when major
  features are added, removed, or materially changed.
- `Validation`: common test, lint, type-check, build, or smoke commands.
- `Git Hygiene`: preserve unrelated changes, stage scoped files only, and use
  focused commits.

Keep `AGENTS.md` short enough to read before every task. Put detailed rules in
`docs/rules/`.

## docs/rules/filetree.md

Purpose: define which directories are allowed and what each directory is for.

Include:

- Current top-level tree.
- Role of each directory.
- Where source, tests, docs, configs, generated outputs, scripts, data, and
  experiments belong.
- Which generated directories are ignored and must not be committed.
- Rule that new top-level directories require updating `filetree.md` in the same
  change.

Avoid:

- Aspirational directories that do not exist and are not part of the agreed
  structure.
- Framework-default paths that conflict with the repo's chosen organization.

## docs/rules/environment.md

Purpose: define runtime and service assumptions.

Include:

- Primary languages and required versions.
- Package managers and lockfiles.
- Virtual environment rules.
- Service manager such as Docker Compose, if any.
- Required local services, ports, and health checks when known.
- Where secrets, datasets, models, logs, and generated artifacts should live.
- Commands for setup and validation.

Mark unknowns explicitly, for example:

```text
Decision needed: choose Python version before adding runtime-specific tooling.
```

## docs/feature-list.md

Purpose: maintain a concise list of major features.

Recommended columns:

```markdown
| Feature | Status | Owner | Docs / Entry Points | Notes |
| --- | --- | --- | --- | --- |
| Example feature | planned | TBD | `path/to/doc.md` | One-line scope. |
```

Status values should stay simple:

- `planned`
- `in_progress`
- `available`
- `deprecated`
- `removed`

Update this file when a change adds, removes, renames, or materially changes a
major feature. Do not use it as a full changelog.
