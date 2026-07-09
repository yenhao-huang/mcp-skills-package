# Target Repository Filetree Rules

Use this reference when `repo-create` writes `docs/rules/filetree.md` for a
target repository. This file is about the target repo's structure, not the
layout of the `repo-create` skill itself.

## Goal

Create a filetree rule that teaches humans and agents:

- Which top-level directories are allowed.
- What each directory is responsible for.
- Where source, tests, docs, configs, scripts, generated outputs, data, and
  experiments belong.
- Which paths are generated or ignored and must not be committed.
- How to propose a new top-level directory.

## Recommended Default Tree

For a new Python/ML/LLM-style repository, start from this conservative shape
unless the user or existing repository conventions say otherwise:

```text
.
|-- AGENTS.md
|-- README.md
|-- .gitignore
|-- configs/          # config files, env templates, YAML/JSON defaults
|-- core/
|   |-- api/          # API, CLI, routes, entrypoints
|   `-- service/      # business logic, pipelines, orchestration
|-- data/             # project-local temporary or symlinked data only
|-- docs/
|   |-- feature-list.md
|   `-- rules/
|       |-- environment.md
|       |-- filetree.md
|       `-- git.md
|-- exp/              # experiments, spikes, research notes
|-- external/         # third-party service wrappers or local integrations
|-- lib/              # shared utilities
|-- logs/             # local runtime logs, ignored unless explicitly kept
|-- results/          # evaluation outputs and generated reports
|-- test/             # tests when the repo does not already use tests/
`-- ui/               # frontend or user interface code
```

If the existing repository already uses `tests/`, `src/`, `scripts/`, `app/`,
or another established layout, preserve it and document that as the active
layout instead of forcing the default tree.

## Required Sections In docs/rules/filetree.md

When writing the target repo's `docs/rules/filetree.md`, include:

1. `Allowed Structure`: a tree that matches actual or agreed directories.
2. `Directory Roles`: concise purpose for each directory.
3. `Creation Rules`: what must happen before adding directories.
4. `Generated Files`: paths that must not be committed.
5. `Change Procedure`: update `filetree.md` in the same change when the
   directory contract changes.

## Design Rules

- Do not create aspirational directories unless the user agrees they are part of
  the initial repo contract.
- Prefer the existing repo's conventions over generic defaults.
- Keep implementation code, tests, configs, docs, and generated artifacts in
  separate directories.
- Do not mix runtime output with source files.
- For model or dataset-heavy repos, prefer external/global storage with
  environment-variable paths or symlinks rather than committing large assets.
- For nested tools or subprojects, give them their own local `AGENTS.md` and
  `docs/rules/filetree.md` only when they have distinct rules.

## Example Creation Rule

```markdown
Before adding a new top-level directory, update `docs/rules/filetree.md` in the
same change with the directory's purpose, allowed contents, and validation
expectations. Do not add convenience directories that duplicate an existing
role.
```
