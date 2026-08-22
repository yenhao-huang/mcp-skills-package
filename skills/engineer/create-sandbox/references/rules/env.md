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
- Docker data host directory: `/mnt/share_data_78/howard/docker`, configurable
  with `DIND_DATA_DIR` and mounted at `/var/lib/docker`.
- Docker storage driver: `overlay2`.
- Data mount host directory: `/mnt/share_data_78/howard/data`, mounted at
  `/data`; explicitly set `DATA_DIR=` to disable it.
- Model mount host directory: `/mnt/share_data_78/howard/models`, mounted at
  `/models`; explicitly set `MODEL_DIR=` to disable it.

The sandbox runs with `--privileged` so the internal daemon can manage nested
containers. Host Docker is disabled by default with `ENABLE_HOST_DOCKER=0`;
when explicitly enabled, mount it at `/var/run/host-docker.sock`, separate
from the inner daemon at `/var/run/docker.sock`. Inner Docker bind paths must
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

Post-create bootstrap belongs in `src/after_create_container.sh`,
not inline in the main build/run script.

## Docker Execution Boundary

Do not run Docker unless the user explicitly asks. Creating or updating scripts
is allowed without running Docker.
