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
- Docker daemon: internal Docker-in-Docker daemon at
  `unix:///var/run/docker.sock`.
- Docker data volume: `codex-sandbox-${REPO_SLUG}-docker-data`, mounted at
  `/var/lib/docker`.
- Docker storage driver: `overlay2`.
- SSH host port: the first unbound port in `3417-3499`, forwarded to container
  port `22`.

SSH port selection is configurable:

```text
SSH_PORT=
SSH_PORT_RANGE_START=3417
SSH_PORT_RANGE_END=3499
PORT_PROBE_PYTHON=
```

When `SSH_PORT` is empty, the host script probes the configured range and uses
the first port that can bind on both IPv4 and IPv6 when IPv6 is available.
When `SSH_PORT` is set, the script validates that exact port before creating
the container and fails if another process already binds it. Port discovery
requires `python3` or `python` on the host.
Set `PORT_PROBE_PYTHON` to an explicit interpreter path when neither command
name resolves to the intended Python installation.

The sandbox runs with `--privileged` so the internal daemon can manage nested
containers. Do not mount the host Docker socket; inner Docker bind paths must
resolve against the sandbox filesystem.

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
