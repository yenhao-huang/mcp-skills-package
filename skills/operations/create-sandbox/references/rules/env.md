# Environment Rules

Use this reference before changing image/container defaults, runtime file
placement, agent package settings, or Docker execution behavior.

## Runtime Paths

- Runtime files belong under the target project's `.runtime/` directory.
- Generated sandbox scripts should be named `.runtime/build_codex_sandbox.sh`.
- Prepared SSH files should live under `.runtime/.ssh`.

## Docker Defaults

- Docker image: `codex-sandbox:local`
- Container name: `codex-sandbox-${REPO_SLUG}`
- Container workdir: `/workspace`
- Container home: `/home/${USERNAME}`
- GPU devices: `all` unless explicitly disabled or overridden.

`REPO_SLUG` is derived from the confirmed repo directory, lowercased, stripped
of a trailing `_forked` or `-forked`, and normalized to alphanumeric plus
hyphen.

## Build Identity

Build with:

- Host UID from `id -u`
- Host primary GID from `id -g`
- Supplementary group IDs from `id -G`
- Host username from `id -un`

## Agent Package Bootstrap

Agent package initialization defaults:

```text
RUN_AGENT_PACKAGE_INIT=1
AGENT_PACKAGE_REPO=git@github.com:yenhao-huang/mcp-skills-package.git
AGENT_PACKAGE_DIRNAME=mcp-skills-package
AGENT_PACKAGE_REF=
```

Post-create bootstrap belongs in `src/after_create_container.sh`, not inline in
the main build/run script.

## Docker Execution Boundary

Do not run Docker unless the user explicitly asks. Creating or updating scripts
is allowed without running Docker.
