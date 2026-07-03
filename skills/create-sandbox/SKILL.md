---
name: create-sandbox
description: >
  Use when the user asks to create, set up, build, update, repair, validate, or
  run an agent sandbox Docker environment for Codex and Claude. Trigger on
  requests such as "建立 sandbox", "建立 codex sandbox", "create a sandbox",
  "create a codex sandbox", "幫我開 sandbox", "make a sandbox for Codex",
  "make a sandbox for Claude", sandbox mounts, sandbox SSH, sandbox Docker
  socket access, custom skills/hooks bootstrap, or project-specific sandbox
  setup such as Pretrieval. Create or update a project-local
  `.runtime/build_codex_sandbox.sh` script from this skill's bundled `src/`
  files. Do not execute Docker commands unless the user explicitly asks.
---

# Create Sandbox

Use this skill to create repeatable Codex/Claude Docker sandbox scripts from
the bundled Docker source in `src/`. Keep `SKILL.md` focused on the workflow;
load detailed rules from `references/` only when needed.

## When To Use

Use this skill when the user asks to:

- Create, update, repair, or run a Codex/Claude agent sandbox container.
- Build a project-local `.runtime/build_codex_sandbox.sh` script.
- Configure sandbox mounts for a repo, models, SSH files, data, Docker socket,
  GPUs, or extra directories.
- Configure or explain post-create custom skills/hooks bootstrap.
- Validate sandbox services such as SSH server, Docker socket access, and
  mounted workspace paths.

Do not use this skill when:

- The task is general Docker advice unrelated to Codex/Claude sandbox behavior.
- The user asks to delete or reset unrelated containers.
- The request requires running Docker but the user has not explicitly asked to
  run it.

## Workflow

1. Read the user's request and identify whether this is a skill update,
   project-local script generation, sandbox repair, or run/validation task.
2. Read `STATE.md`; for a new run, reset it from
   `references/template/STATE.template.md`.
3. Load only the relevant reference files listed below.
4. Mark the current step `in_progress` in `STATE.md`.
5. For project-local script generation, sandbox repair, or sandbox run tasks,
   ask the required mount questions defined in
   `references/rules/mounts.md` before writing or running anything unless the
   user's request already provides explicit answers. Do not silently create a
   blank configurable script just because answers are missing.
6. If the user explicitly asks to proceed without answering the mount
   questions, create only a configurable script with empty optional mounts and
   clear fail-fast behavior for missing `WORKSPACE_DIR`, as defined in
   `references/rules/mounts.md`.
7. Validate every confirmed non-empty host path before writing or running a
   script.
8. If updating this skill, edit bundled files in `src/`, `references/`, and
   this `SKILL.md` as needed.
9. If creating a sandbox for another project, create or update only that
   project's `.runtime/build_codex_sandbox.sh`, based on
   `src/build_and_exec.sh`.
10. Ensure the target project's `.gitignore` contains `.runtime/`.
11. Validate changed shell scripts with `bash -n`; make generated scripts
    executable with `chmod +x`.
12. Mark the step `completed`, `blocked`, or `skipped` in `STATE.md` with
    evidence.

## References

- Read `references/rules/lifecycle.md` before changing build/run/post-create
  behavior or explaining which work happens before vs. after container create.
- Read `references/rules/mounts.md` before asking mount questions, validating
  paths, preparing SSH files, or handling Docker socket/extra mounts.
- Read `references/rules/runtime-mount-permissions.md` when Docker bind mounts
  fail or when host paths are under `/home`/NFS.
- Read `references/rules/env.md` before changing image/container defaults,
  agent package bootstrap settings, or runtime file placement.
- Read `references/rules/service-tests.md` before changing validation behavior.
- Read `references/rules/filetree.md` before adding, moving, or removing files
  in this skill directory.
- Read `references/rules/state-rules.md` when updating `STATE.md`.
- Read `references/tools.md` when the user asks about installed tools, common
  utilities, Dockerfile package choices, or network/debug tooling.
- Use `src/Dockerfile` as the canonical Docker build definition.
- Use `src/build_and_exec.sh` as the canonical executable template for
  generated project-local scripts.
- Use `src/after_create_container.sh` for post-create bootstrap in the running
  container.
- Use `src/test_service.sh` for post-start service checks.

## Environment

Follow `references/rules/env.md` for image/container defaults, runtime paths,
agent package settings, and Docker execution boundaries. Do not run Docker
unless the user explicitly requests it.

## Rules

### State Rules

Keep `STATE.md` as per-run working state. Reset it from
`references/template/STATE.template.md` for new executions, and do not claim a
workflow step is complete unless `STATE.md` was updated with concrete evidence.
Read `references/rules/state-rules.md` for status values and update rules.

### Reference Rules

- Keep `SKILL.md` focused on trigger conditions and core workflow.
- Put detailed sandbox lifecycle, mount, SSH, environment, and validation rules
  in `references/rules/`.
- Put deterministic executable tooling in `src/`.
- Load only the reference files needed for the current request.

## Output

Final responses should include:

- What changed or what was investigated.
- Script path or skill file path when relevant.
- Validation commands and results.
- Whether Docker was executed.
- Any blocker or remaining risk.
