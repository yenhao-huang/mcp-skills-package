---
name: codex-sandbox
description: Use when the user asks to create, set up, build, update, or run a Codex sandbox. Use this skill's bundled src/ directory as the canonical Codex sandbox source path, including src/Dockerfile and src/build_and_exec.sh. Create or update a bash script the user can execute later to build the Docker image, prepare SSH files, start a persistent Codex sandbox container, and enter it. Do not execute Docker commands unless the user explicitly asks. Trigger on requests such as "建立 codex sandbox", "create a codex sandbox", "幫我開 codex sandbox", or "make a sandbox for Codex".
---

# Codex Sandbox

When the user asks to create or update a Codex sandbox, use the bundled `src/` directory beside this `SKILL.md` as the source of truth.

Expected skill layout:

```text
codex-sandbox/
├── SKILL.md
├── issues/
└── src/
    ├── Dockerfile
    ├── README.md
    ├── build_and_exec.sh
    └── shell/
```

The normal deliverable is a `.sh` file the user can run later. Do not run it yourself unless the user explicitly requests execution.

## Known Issues

- Before creating, updating, or running a sandbox script, check whether this skill
  has an `issues/` directory beside `SKILL.md`. If it exists, read the relevant
  `issues/*.md` notes and apply them to the current task.
- In particular, known issues may describe host-specific Docker mount behavior
  that is not captured by the generic script template. Do not rely only on the
  template when an issue note documents a safer local convention.

## Path Rules

- Treat `src/` as the Codex sandbox project root.
- Use `src/Dockerfile` as the Docker build definition.
- Use `src/build_and_exec.sh` as the default script to update when working inside this installed skill.
- If the user wants a sandbox in another project, copy or adapt files from this skill's `src/` path into the target path instead of using stale repo paths.
- Put generated runtime files in the target project's `.runtime/` directory. This includes generated sandbox shell scripts such as `.runtime/build_codex_sandbox.sh` and prepared SSH files under `.runtime/.ssh`.
- Do not place generated sandbox scripts at the target project root unless the user explicitly requests that location.
- When adding `.runtime/` files to a target project, ensure the target project's `.gitignore` contains `.runtime/`.
- Do not refer to the old skill name `codex-sandbox-script`.

## Required Questions

Before writing a script, updating a script, or running any sandbox command, ask these questions unless the user already provided explicit answers in the current request. Do not infer the repo/workspace from `cwd`, a parent directory, or a search result.

1. Which repo/workspace directory should be mounted? Ask for the host path and container path. Default container path only after confirmation: `/workspace`.
2. Which model directory should be mounted? Ask for the host path and container path, or confirm no model mount. Default container path only after confirmation: `/models`.
3. Which skills directory should be mounted? Ask for the host path and container path. Default container path only after confirmation: `${CONTAINER_HOME}/.agents/skills`.
4. Which SSH directory or prepared SSH files should be mounted? Ask for the host path and container path, or confirm no SSH mount. Default container path only after confirmation: `${CONTAINER_HOME}/.ssh:ro`.
5. Which data directory should be mounted? Ask for the host path and container path, or confirm no data mount. Default container path only after confirmation: `/data`.
6. Besides the repo, model, skills, SSH, and data directories, ask whether any extra mounted directories are needed. If yes, ask for each mount as `host_path:container_path` or `host_path:container_path:ro`.

If the user wants to proceed without answering, do not run the sandbox. Create only a configurable script with empty `WORKSPACE_DIR`, `MODEL_DIR`, `SKILLS_DIR`, `SSH_DIR`, `DATA_DIR`, and `EXTRA_MOUNTS` variables, and make the script fail with a clear error until `WORKSPACE_DIR` and `SKILLS_DIR` are configured.

## Mount Validation

After the required mount questions are answered, validate every non-empty host path before writing a script, updating a script, or running any sandbox command.

- Check that each confirmed host path exists.
- Check that the repo/workspace host path is readable, writable, and executable/searchable.
- Check that model, skills, SSH, data, and extra mount host paths are readable and executable/searchable. Also check writability for every mount that will be mounted read-write; Docker `-v host:container` mounts are read-write unless `:ro` is explicitly confirmed.
- If a host path does not exist, do not guess silently or continue. Ask a correction question in this form: `repo 找不到，你想找的是不是 <candidate>?` Replace `repo` with the mount label (`model`, `skills`, `ssh`, `data`, or `extra mount`) and include the best nearby candidate when one is discoverable. If no candidate is discoverable, ask for the corrected host path without writing or running the sandbox.
- When looking for a candidate for a missing path, prefer a narrow parent-directory check and common typo correction over broad filesystem scans. For example, if `/mnat/share_data_78/howard/data` is missing but `/mnt/share_data_78/howard/data` exists, ask whether the user meant `/mnt/share_data_78/howard/data`.
- If a host path exists but lacks required read, write, or execute/search permission, do not change permissions automatically. Ask whether it is acceptable to copy the needed files into the target project's `.runtime/` directory and mount that copy instead. Only copy after explicit confirmation.
- If the user confirms copying into `.runtime/`, copy only the confirmed directory or prepared files needed for the mount, preserve restrictive permissions for SSH material, and mount the `.runtime/` copy instead of the inaccessible original.
- If validation fails for any mount, stop before script creation or Docker execution unless the user explicitly provides a corrected path or confirms the `.runtime/` copy fallback.
- Generated scripts should also fail fast with clear errors when configured mount paths are missing or lack the permissions required by their mount mode.

## Workflow

1. Locate this skill's `src/` directory beside `SKILL.md`; confirm `src/Dockerfile` exists.
2. Ask the required mount questions above before editing files or running Docker, unless the user already answered them explicitly.
3. Validate confirmed mount host paths using the Mount Validation rules above. Resolve missing paths or permission issues with the user before continuing.
4. Update `src/build_and_exec.sh` when editing the installed skill. When creating a sandbox for another project, create a new `.runtime/build_codex_sandbox.sh`-style script in the user's requested target directory and base it on `src/build_and_exec.sh`.
5. Ensure the target project's `.gitignore` contains `.runtime/` before or while adding generated `.runtime/` files. Preserve existing `.gitignore` contents.
6. Make the script executable with `chmod +x <script>`.
7. Keep paths configurable through environment variables, with safe defaults.
8. Include `set -euo pipefail`.
9. Derive the default container name from the confirmed repo directory as `codex-sandox-${REPO_SLUG}`, where `REPO_SLUG` is lowercased, strips a trailing `_forked` or `-forked`, and replaces non-alphanumeric characters with `-`. If a container with the chosen name already exists, stop and remove it before starting a new one.
10. Build `codex-sandbox:local` using the host UID, GID, and username.
11. Prepare an SSH directory under `.runtime/.ssh` if SSH keys exist on the host and validation permits direct reading, or if the user confirms copying inaccessible SSH material into `.runtime/.ssh`. Copy `id_ed25519`, `id_ed25519.pub`, and `known_hosts` only when present; set strict permissions.
12. Write the script so that, when the user runs it later, it starts a detached container that sleeps forever and mounts exactly the confirmed repo, SSH, skills, model, data, and extra mount directories. Do not add unconfirmed broad parent directories.
13. Write the script so that, when the user runs it later, it ends with `docker exec -it "${CONTAINER_NAME}" bash` and lands inside the container.
14. Stop after creating and syntax-checking the `.sh` file. Do not run the script or any Docker commands unless the user explicitly asks you to run it.

## Script Template

Use this structure unless the repo already has stronger conventions:

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${IMAGE_NAME:-codex-sandbox:local}"
USERNAME="${USERNAME:-$(id -un)}"
CONTAINER_HOME="${CONTAINER_HOME:-/home/${USERNAME}}"
CONTAINER_WORKDIR="${CONTAINER_WORKDIR:-/workspace}"
BUILD_CONTEXT="${BUILD_CONTEXT:-/home/howard/.agents/skills/codex-sandbox/src}"
WORKSPACE_DIR="${WORKSPACE_DIR:-}"
SSH_DIR="${SSH_DIR:-}"
SKILLS_DIR="${SKILLS_DIR:-}"
MODEL_DIR="${MODEL_DIR:-}"
DATA_DIR="${DATA_DIR:-}"
CONTAINER_SKILLS_DIR="${CONTAINER_SKILLS_DIR:-${CONTAINER_HOME}/.agents/skills}"
CONTAINER_MODEL_DIR="${CONTAINER_MODEL_DIR:-/models}"
CONTAINER_DATA_DIR="${CONTAINER_DATA_DIR:-/data}"
EXTRA_MOUNTS="${EXTRA_MOUNTS:-}"
GPU_DEVICES="${GPU_DEVICES:-all}"

if [[ -z "${WORKSPACE_DIR}" ]]; then
  echo "WORKSPACE_DIR must be set to the confirmed repo/workspace host path." >&2
  exit 1
fi
if [[ -z "${SKILLS_DIR}" ]]; then
  echo "SKILLS_DIR must be set to the confirmed skills host path." >&2
  exit 1
fi

REPO_NAME="$(basename "${WORKSPACE_DIR}")"
REPO_SLUG="$(printf '%s' "${REPO_NAME}" | sed -E 's/(_forked|-forked)$//I; s/[^A-Za-z0-9]+/-/g; s/^-+|-+$//g' | tr '[:upper:]' '[:lower:]')"
CONTAINER_NAME="${CONTAINER_NAME:-codex-sandox-${REPO_SLUG}}"

if [[ -n "${SSH_DIR}" ]]; then
  mkdir -p "${SSH_DIR}"
fi
mkdir -p "${SKILLS_DIR}"

if [[ -n "${SSH_DIR}" && -f "${HOME}/.ssh/id_ed25519" ]]; then
  cp "${HOME}/.ssh/id_ed25519" "${SSH_DIR}/"
fi
if [[ -n "${SSH_DIR}" && -f "${HOME}/.ssh/id_ed25519.pub" ]]; then
  cp "${HOME}/.ssh/id_ed25519.pub" "${SSH_DIR}/"
fi
if [[ -n "${SSH_DIR}" && -f "${HOME}/.ssh/known_hosts" ]]; then
  cp "${HOME}/.ssh/known_hosts" "${SSH_DIR}/"
fi

if [[ -n "${SSH_DIR}" ]]; then
  chmod 700 "${SSH_DIR}"
fi
if [[ -n "${SSH_DIR}" && -f "${SSH_DIR}/id_ed25519" ]]; then
  chmod 600 "${SSH_DIR}/id_ed25519"
fi
if [[ -n "${SSH_DIR}" && -f "${SSH_DIR}/id_ed25519.pub" ]]; then
  chmod 644 "${SSH_DIR}/id_ed25519.pub"
fi
if [[ -n "${SSH_DIR}" && -f "${SSH_DIR}/known_hosts" ]]; then
  chmod 644 "${SSH_DIR}/known_hosts"
fi

if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  docker stop "${CONTAINER_NAME}"
  docker rm "${CONTAINER_NAME}"
fi

docker build \
  --build-arg UID="$(id -u)" \
  --build-arg GID="$(id -g)" \
  --build-arg USERNAME="${USERNAME}" \
  -t "${IMAGE_NAME}" \
  "${BUILD_CONTEXT}"

docker_args=(
  run -d
  --name "${CONTAINER_NAME}"
  -w "${CONTAINER_WORKDIR}"
  -e "HOME=${CONTAINER_HOME}"
  -e "NVIDIA_VISIBLE_DEVICES=${GPU_DEVICES}"
  -e "NVIDIA_DRIVER_CAPABILITIES=compute,utility"
  -v "${WORKSPACE_DIR}:${CONTAINER_WORKDIR}"
  -v "${SKILLS_DIR}:${CONTAINER_SKILLS_DIR}"
)

if [[ -n "${SSH_DIR}" ]]; then
  docker_args+=(-v "${SSH_DIR}:${CONTAINER_HOME}/.ssh:ro")
fi
if [[ -n "${GPU_DEVICES}" && "${GPU_DEVICES}" != "none" ]]; then
  docker_args+=(--gpus "${GPU_DEVICES}")
fi

if [[ -n "${MODEL_DIR}" ]]; then
  docker_args+=(-v "${MODEL_DIR}:${CONTAINER_MODEL_DIR}")
fi
if [[ -n "${DATA_DIR}" ]]; then
  docker_args+=(-v "${DATA_DIR}:${CONTAINER_DATA_DIR}")
fi
if [[ -n "${EXTRA_MOUNTS}" ]]; then
  IFS=',' read -r -a extra_mounts <<< "${EXTRA_MOUNTS}"
  for mount_spec in "${extra_mounts[@]}"; do
    if [[ -n "${mount_spec}" ]]; then
      docker_args+=(-v "${mount_spec}")
    fi
  done
fi

docker "${docker_args[@]}" "${IMAGE_NAME}" sleep infinity
docker exec -it "${CONTAINER_NAME}" bash
```

## Validation

After writing the script:

```bash
bash -n <script>
```

Also verify the target project's `.gitignore` contains:

```gitignore
.runtime/
```

Report the script path and the command the user can run. Do not execute the script or any Docker commands unless the user explicitly asks for execution.
