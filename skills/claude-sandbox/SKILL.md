---
name: claude-sandbox
description: >
  Use when the user asks to set up, start, enter, or repair a Claude Code
  sandbox Docker container. Guide or create scripts for `docker pull`,
  `docker run`, and `docker exec` workflows that launch an isolated Claude Code
  environment with `bypassPermissions`. Trigger on "開 claude sandbox",
  "start claude sandbox", "run claude in docker", "create claude sandbox", or
  "進 claude 容器".
---

# Claude Sandbox

Use this skill to run Claude Code inside an isolated Docker container with a
prepared runtime home, SSH files, workspace mounts, model/data mounts, and
`bypassPermissions` behavior.

## When To Use

Use this skill when the user asks to:

- Create, set up, start, restart, or enter a Claude Code sandbox container.
- Generate or update the bundled `src/build_and_exec.sh` or `src/run.sh`
  helpers for the Claude sandbox.
- Pull, tag, build, or publish the Claude sandbox image.
- Debug whether the `claude-docker` container is running or usable.

Do not use this skill when:

- The request is about Codex sandbox setup; use `codex-sandbox` instead.
- The user only wants generic Docker guidance unrelated to Claude Code.
- The task would run Docker but the user has not explicitly asked you to run it.

## Workflow

1. Identify whether the task is setup, start/enter, restart/debug, or image
   build/publish.
2. For setup tasks, create or update `src/build_and_exec.sh` or `src/run.sh` in
   the `claude-sandbox` skill directory using the current runtime conventions
   below.
3. Prepare runtime files under `/tmp/claude-sandbox-runtime`, not directly in
   the skill directory.
4. Copy only the Claude credentials/settings and SSH files needed by the
   container.
5. Start the container as `claude-docker` with the confirmed mounts.
6. Enter Claude from the caller's current project-relative path under
   `/workspace`.
7. Validate with `docker ps`, `docker exec`, or the smallest command that proves
   the requested behavior.

## References

- Use `src/build_and_exec.sh` as the setup/start helper.
- Use `src/run.sh` as the persistent-container enter helper.
- Use Docker image `yenhao123/claude-sandbox:latest` by default, tagged locally
  as `claude-sandbox`.

## Environment

- Container name: `claude-docker`.
- Runtime directory: `/tmp/claude-sandbox-runtime`.
- Claude home mount: `/tmp/claude-sandbox-runtime/claude-home` to
  `/claude-home`.
- SSH mount: `/tmp/claude-sandbox-runtime/ssh` to `/claude-home/.ssh:ro`.
- Workspace mount: `/tmp2/howard` to `/workspace`.
- Model mount: `/mnt/share_data_78/howard/models` to `/models`.
- Data mount: `/mnt/share_data_78/howard/data` to `/data`.
- Container working directory defaults to `/workspace`.
- Run Claude as the host UID/GID with `HOME=/claude-home`.

## Rules

- Keep bundled helper scripts executable and aligned with the environment
  defaults above.
- Use `set -euo pipefail` in generated shell scripts.
- Preserve restrictive permissions for copied credentials and private keys.
- Remove an existing `claude-docker` container before starting a replacement
  only when the user is asking to start or restart it.
- Do not expose or print credential file contents.
- Do not run Docker commands unless the user explicitly asked for execution.

## Output

Final responses should include:

- What script or container action was created or performed.
- The helper path or Docker command the user can run.
- Validation command and result.
- Whether Docker was executed.
