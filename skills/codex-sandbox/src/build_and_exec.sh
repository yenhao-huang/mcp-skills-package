#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${IMAGE_NAME:-codex-sandbox:local}"
USERNAME="${USERNAME:-$(id -un)}"
CONTAINER_HOME="${CONTAINER_HOME:-/home/${USERNAME}}"
CONTAINER_WORKDIR="${CONTAINER_WORKDIR:-/workspace}"
BUILD_CONTEXT="${BUILD_CONTEXT:-${SCRIPT_DIR}}"
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

if [[ ! -f "${BUILD_CONTEXT}/Dockerfile" ]]; then
  echo "Missing Dockerfile in BUILD_CONTEXT: ${BUILD_CONTEXT}" >&2
  exit 1
fi

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
