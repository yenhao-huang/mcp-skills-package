---
name: repo-create
description: Create or refine repository governance docs through discussion with the user. Use when Codex needs to help set up a repo, define AGENTS.md instructions, define docs/rules such as filetree.md and environment.md, create or maintain docs/feature-list.md, or teach a user how to manage a repository with explicit rules and feature tracking.
---

# Repo Create

Use this skill to help a user design and create the management layer for a
repository before or while code is added. The core output is a small set of
repo-governance documents that explain how developers and agents should work in
the repo.

## Workflow

1. Inspect the repository first:
   - Read existing `AGENTS.md`, `README.md`, `docs/`, `.gitignore`, dependency
     files, and visible top-level directories.
   - Preserve existing conventions unless the user asks to replace them.
2. Read `STATE.md`; for a new run, reset it from
   `references/template/STATE.template.md`, then mark the active step
   `in_progress`.
3. Discuss scope with the user when it is not already clear:
   - Ask what the repo is for, who will maintain it, expected languages,
     runtime services, and what directories should be allowed.
   - If the user gave enough direction, proceed with conservative defaults and
     state the assumptions.
4. Create or update `AGENTS.md`:
   - Explain the repo purpose, operating rules, validation commands, and git
     hygiene.
   - Teach the user where the important docs live and how to update them.
   - Point agents to `docs/rules/filetree.md` before directory changes and to
     `docs/rules/environment.md` before environment changes.
   - Point agents to `docs/rules/git.md` before staging, committing, or
     changing branch/remotes.
5. Create or update `docs/rules/`:
   - `filetree.md`: allowed directory tree, directory roles, creation rules,
     generated-file rules, and how to propose new directories.
   - `environment.md`: language/runtime versions, package managers, services,
     secrets, data/model storage, and validation commands.
   - `git.md`: commit workflow, staging scope, dirty-worktree handling,
     Conventional Commit guidance, and remote/push rules.
6. Create or update `docs/feature-list.md`:
   - Track major user-visible or operational features.
   - Keep entries short, current, and linked to docs or implementation files
     when useful.
7. Validate the docs:
   - Check links and paths against the actual repo.
   - Run the smallest relevant validation command if the repo defines one.
   - Inspect `git diff --check` before committing or handing off.
8. Mark completed or blocked steps in `STATE.md` with evidence before the final
   response.

## Reference

- Read `references/example.md` to understand trigger examples and expected
  outputs.
- Read `references/governance-docs.md` when writing or revising the actual
  `AGENTS.md`, `docs/rules/filetree.md`, `docs/rules/environment.md`, or
  `docs/feature-list.md` content.
- Read `references/rules/filetree.md` before creating or moving governance
  files.
- Read `references/rules/env.md` before writing environment assumptions.
- Read `references/rules/git.md` before writing git workflow rules.
- Read `references/rules/state-rules.md` before changing `STATE.md`.

## Rules

- Do not invent services, package managers, credentials, ports, model paths, or
  deployment targets. Mark unknowns as decisions for the user.
- Do not overwrite existing repo instructions without preserving their required
  constraints.
- Keep governance docs practical: prefer rules that agents and developers can
  follow during day-to-day changes.
- Keep feature-list entries about significant features, not every minor commit.
- If creating a new repo from scratch, create the governance docs before adding
  broad implementation structure.

## Output

Final responses should include:

- Which governance docs were created or updated.
- The assumptions or user decisions encoded in those docs.
- Validation commands and results.
- Any remaining decisions the user still needs to make.
