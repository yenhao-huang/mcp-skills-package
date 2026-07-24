#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${IMAGE_NAME:-codex-sandbox:local}"
USERNAME="${USERNAME:-$(id -un)}"
HOST_GROUP_IDS="${HOST_GROUP_IDS:-$(id -G)}"
CONTAINER_HOME="${CONTAINER_HOME:-/home/${USERNAME}}"
CONTAINER_WORKDIR="${CONTAINER_WORKDIR:-/workspace}"
BUILD_CONTEXT="${BUILD_CONTEXT:-${SCRIPT_DIR}}"
WORKSPACE_DIR="${WORKSPACE_DIR:-}"
HOST_SSH_DIR="${HOST_SSH_DIR:-${HOME}/.ssh}"
SSH_DIR="${SSH_DIR:-${SCRIPT_DIR}/.ssh}"
MODEL_DIR="${MODEL_DIR:-}"
DATA_DIR="${DATA_DIR:-}"
CONTAINER_MODEL_DIR="${CONTAINER_MODEL_DIR:-/models}"
CONTAINER_DATA_DIR="${CONTAINER_DATA_DIR:-/data}"
DIND_DOCKER_SOCK="${DIND_DOCKER_SOCK:-/var/run/docker.sock}"
DIND_STORAGE_DRIVER="${DIND_STORAGE_DRIVER:-overlay2}"
EXTRA_MOUNTS="${EXTRA_MOUNTS:-}"
GPU_DEVICES="${GPU_DEVICES:-all}"
SSH_PORT="${SSH_PORT:-}"
SSH_PORT_RANGE_START="${SSH_PORT_RANGE_START:-3417}"
SSH_PORT_RANGE_END="${SSH_PORT_RANGE_END:-3499}"
PREPARE_SSH_DIR="${PREPARE_SSH_DIR:-1}"
RUN_SERVICE_TESTS="${RUN_SERVICE_TESTS:-1}"
AFTER_CREATE_CONTAINER_SCRIPT="${AFTER_CREATE_CONTAINER_SCRIPT:-${BUILD_CONTEXT}/after_create_container.sh}"
TEST_SERVICE_SCRIPT="${TEST_SERVICE_SCRIPT:-${BUILD_CONTEXT}/test_service.sh}"
RUN_AGENT_PACKAGE_INIT="${RUN_AGENT_PACKAGE_INIT:-1}"
AGENT_PACKAGE_REPO="${AGENT_PACKAGE_REPO:-git@github.com:yenhao-huang/mcp-skills-package.git}"
AGENT_PACKAGE_DIRNAME="${AGENT_PACKAGE_DIRNAME:-mcp-skills-package}"
AGENT_PACKAGE_REF="${AGENT_PACKAGE_REF:-}"
PORT_PROBE_PYTHON="${PORT_PROBE_PYTHON:-}"

validate_dir() {
  local label="$1"
  local path="$2"
  local require_write="$3"

  if [[ -z "${path}" ]]; then
    return
  fi
  if [[ ! -d "${path}" ]]; then
    echo "${label} must be an existing directory: ${path}" >&2
    exit 1
  fi
  if [[ ! -r "${path}" || ! -x "${path}" ]]; then
    echo "${label} must be readable and executable/searchable by the current user: ${path}" >&2
    exit 1
  fi
  if [[ "${require_write}" == "1" && ! -w "${path}" ]]; then
    echo "${label} must be writable by the current user: ${path}" >&2
    exit 1
  fi
}

validate_port_number() {
  local label="$1"
  local port="$2"

  if [[ ! "${port}" =~ ^[0-9]+$ ]] || ((port < 1 || port > 65535)); then
    echo "${label} must be an integer from 1 through 65535: ${port}" >&2
    exit 1
  fi
}

require_port_probe() {
  if [[ -n "${PORT_PROBE_PYTHON}" ]]; then
    if ! "${PORT_PROBE_PYTHON}" -c 'import socket' >/dev/null 2>&1; then
      echo "PORT_PROBE_PYTHON cannot run the socket module: ${PORT_PROBE_PYTHON}" >&2
      exit 1
    fi
  elif command -v python3 >/dev/null 2>&1 \
    && python3 -c 'import socket' >/dev/null 2>&1; then
    PORT_PROBE_PYTHON="python3"
  elif command -v python >/dev/null 2>&1 \
    && python -c 'import socket' >/dev/null 2>&1; then
    PORT_PROBE_PYTHON="python"
  else
    echo "Automatic SSH port discovery requires python3 or python on the host." >&2
    exit 1
  fi
}

port_is_available() {
  local port="$1"

  "${PORT_PROBE_PYTHON}" - "${port}" <<'PY'
import errno
import socket
import sys

port = int(sys.argv[1])
sockets = []

try:
    ipv4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ipv4.bind(("0.0.0.0", port))
    sockets.append(ipv4)

    try:
        ipv6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        ipv6.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
        ipv6.bind(("::", port))
        sockets.append(ipv6)
    except OSError as exc:
        if exc.errno not in (errno.EAFNOSUPPORT, errno.EADDRNOTAVAIL):
            raise
except OSError:
    sys.exit(1)
finally:
    for sock in sockets:
        sock.close()
PY
}

resolve_ssh_port() {
  local candidate

  require_port_probe
  validate_port_number "SSH_PORT_RANGE_START" "${SSH_PORT_RANGE_START}"
  validate_port_number "SSH_PORT_RANGE_END" "${SSH_PORT_RANGE_END}"
  if ((SSH_PORT_RANGE_START > SSH_PORT_RANGE_END)); then
    echo "SSH_PORT_RANGE_START must not exceed SSH_PORT_RANGE_END." >&2
    exit 1
  fi

  if [[ -n "${SSH_PORT}" ]]; then
    validate_port_number "SSH_PORT" "${SSH_PORT}"
    if ! port_is_available "${SSH_PORT}"; then
      echo "Requested SSH_PORT is already bound: ${SSH_PORT}" >&2
      exit 1
    fi
  else
    printf 'Searching for an unbound SSH host port in %s-%s...\n' \
      "${SSH_PORT_RANGE_START}" "${SSH_PORT_RANGE_END}" >&2
    for ((candidate = SSH_PORT_RANGE_START; candidate <= SSH_PORT_RANGE_END; candidate++)); do
      if port_is_available "${candidate}"; then
        SSH_PORT="${candidate}"
        break
      fi
    done
    if [[ -z "${SSH_PORT}" ]]; then
      echo "No unbound SSH host port found in ${SSH_PORT_RANGE_START}-${SSH_PORT_RANGE_END}." >&2
      exit 1
    fi
  fi

  printf 'Forwarding host port %s to container port 22.\n' "${SSH_PORT}" >&2
}

if [[ -z "${WORKSPACE_DIR}" ]]; then
  echo "WORKSPACE_DIR must be set to the confirmed repo/workspace host path." >&2
  exit 1
fi

validate_dir "WORKSPACE_DIR" "${WORKSPACE_DIR}" 1
validate_dir "MODEL_DIR" "${MODEL_DIR}" 1
validate_dir "DATA_DIR" "${DATA_DIR}" 1
if [[ "${PREPARE_SSH_DIR}" == "1" ]]; then
  validate_dir "HOST_SSH_DIR" "${HOST_SSH_DIR}" 0
else
  validate_dir "SSH_DIR" "${SSH_DIR}" 1
fi

REPO_NAME="$(basename "${WORKSPACE_DIR}")"
REPO_SLUG="$(printf '%s' "${REPO_NAME}" | sed -E 's/(_forked|-forked)$//I; s/[^A-Za-z0-9]+/-/g; s/^-+|-+$//g' | tr '[:upper:]' '[:lower:]')"
CONTAINER_NAME="${CONTAINER_NAME:-codex-sandbox-${REPO_SLUG}}"
DIND_DATA_VOLUME="${DIND_DATA_VOLUME:-${CONTAINER_NAME}-docker-data}"

if [[ "${PREPARE_SSH_DIR}" == "1" && -n "${SSH_DIR}" ]]; then
  mkdir -p "${SSH_DIR}"
fi

if [[ ! -f "${BUILD_CONTEXT}/Dockerfile" ]]; then
  echo "Missing Dockerfile in BUILD_CONTEXT: ${BUILD_CONTEXT}" >&2
  exit 1
fi
if [[ ! -x "${AFTER_CREATE_CONTAINER_SCRIPT}" ]]; then
  echo "Missing executable after-create-container script: ${AFTER_CREATE_CONTAINER_SCRIPT}" >&2
  exit 1
fi
if [[ "${PREPARE_SSH_DIR}" == "1" && -n "${SSH_DIR}" && -f "${HOST_SSH_DIR}/id_ed25519" ]]; then
  cp "${HOST_SSH_DIR}/id_ed25519" "${SSH_DIR}/"
fi
if [[ "${PREPARE_SSH_DIR}" == "1" && -n "${SSH_DIR}" && -f "${HOST_SSH_DIR}/id_ed25519.pub" ]]; then
  cp "${HOST_SSH_DIR}/id_ed25519.pub" "${SSH_DIR}/"
fi
if [[ "${PREPARE_SSH_DIR}" == "1" && -n "${SSH_DIR}" && -f "${HOST_SSH_DIR}/known_hosts" ]]; then
  cp "${HOST_SSH_DIR}/known_hosts" "${SSH_DIR}/"
fi
if [[ "${PREPARE_SSH_DIR}" == "1" && -n "${SSH_DIR}" && -f "${HOST_SSH_DIR}/authorized_keys" ]]; then
  cp "${HOST_SSH_DIR}/authorized_keys" "${SSH_DIR}/"
elif [[ "${PREPARE_SSH_DIR}" == "1" && -n "${SSH_DIR}" && -f "${SSH_DIR}/id_ed25519.pub" && ! -f "${SSH_DIR}/authorized_keys" ]]; then
  cp "${SSH_DIR}/id_ed25519.pub" "${SSH_DIR}/authorized_keys"
fi

if [[ "${PREPARE_SSH_DIR}" == "1" && -n "${SSH_DIR}" ]]; then
  chmod 700 "${SSH_DIR}"
fi
if [[ "${PREPARE_SSH_DIR}" == "1" && -n "${SSH_DIR}" && -f "${SSH_DIR}/id_ed25519" ]]; then
  chmod 600 "${SSH_DIR}/id_ed25519"
fi
if [[ "${PREPARE_SSH_DIR}" == "1" && -n "${SSH_DIR}" && -f "${SSH_DIR}/id_ed25519.pub" ]]; then
  chmod 644 "${SSH_DIR}/id_ed25519.pub"
fi
if [[ "${PREPARE_SSH_DIR}" == "1" && -n "${SSH_DIR}" && -f "${SSH_DIR}/known_hosts" ]]; then
  chmod 644 "${SSH_DIR}/known_hosts"
fi
if [[ "${PREPARE_SSH_DIR}" == "1" && -n "${SSH_DIR}" && -f "${SSH_DIR}/authorized_keys" ]]; then
  chmod 600 "${SSH_DIR}/authorized_keys"
fi

if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  docker stop "${CONTAINER_NAME}"
  docker rm "${CONTAINER_NAME}"
fi

docker build \
  --build-arg UID="$(id -u)" \
  --build-arg GID="$(id -g)" \
  --build-arg USERNAME="${USERNAME}" \
  --build-arg SUPPLEMENTARY_GIDS="${HOST_GROUP_IDS}" \
  -t "${IMAGE_NAME}" \
  "${BUILD_CONTEXT}"

resolve_ssh_port

docker_args=(
  run -d
  --name "${CONTAINER_NAME}"
  -w "${CONTAINER_WORKDIR}"
  --privileged
  -e "HOME=${CONTAINER_HOME}"
  -e "DIND_DOCKER_SOCK=${DIND_DOCKER_SOCK}"
  -e "DIND_STORAGE_DRIVER=${DIND_STORAGE_DRIVER}"
  -e "DOCKER_HOST=unix://${DIND_DOCKER_SOCK}"
  -e "DOCKER_TLS_CERTDIR="
  -e "NVIDIA_VISIBLE_DEVICES=${GPU_DEVICES}"
  -e "NVIDIA_DRIVER_CAPABILITIES=compute,utility"
  -v "${WORKSPACE_DIR}:${CONTAINER_WORKDIR}"
  -v "${DIND_DATA_VOLUME}:/var/lib/docker"
)

if [[ -n "${SSH_DIR}" ]]; then
  docker_args+=(-v "${SSH_DIR}:${CONTAINER_HOME}/.ssh")
fi
docker_args+=(-p "${SSH_PORT}:22")
if [[ -n "${GPU_DEVICES}" && "${GPU_DEVICES}" != "none" ]]; then
  docker_args+=(--gpus "${GPU_DEVICES}")
fi

for group_id in ${HOST_GROUP_IDS}; do
  docker_args+=(--group-add "${group_id}")
done

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

docker "${docker_args[@]}" "${IMAGE_NAME}" bash -lc '
  set -euo pipefail
  sudo sh -c "nohup dockerd --host=unix://${DIND_DOCKER_SOCK} --storage-driver=${DIND_STORAGE_DRIVER} >/var/log/dockerd.log 2>&1 &"

  for attempt in $(seq 1 60); do
    if docker info >/dev/null 2>&1; then
      break
    fi
    sleep 1
  done

  if ! docker info >/dev/null 2>&1; then
    echo "Docker-in-Docker daemon did not become ready." >&2
    sudo tail -n 100 /var/log/dockerd.log >&2 || true
    exit 1
  fi

  sudo /usr/sbin/sshd
  touch /tmp/codex-sandbox-ready
  exec sleep infinity
'

for attempt in $(seq 1 70); do
  if docker exec "${CONTAINER_NAME}" test -f /tmp/codex-sandbox-ready >/dev/null 2>&1; then
    break
  fi
  if [[ "$(docker inspect -f '{{.State.Running}}' "${CONTAINER_NAME}")" != "true" ]]; then
    echo "Sandbox container exited before Docker-in-Docker and SSH became ready." >&2
    docker logs "${CONTAINER_NAME}" >&2 || true
    exit 1
  fi
  sleep 1
done

if ! docker exec "${CONTAINER_NAME}" test -f /tmp/codex-sandbox-ready >/dev/null 2>&1; then
  echo "Timed out waiting for Docker-in-Docker and SSH readiness." >&2
  docker logs "${CONTAINER_NAME}" >&2 || true
  exit 1
fi

CONTAINER_NAME="${CONTAINER_NAME}" \
CONTAINER_WORKDIR="${CONTAINER_WORKDIR}" \
RUN_AGENT_PACKAGE_INIT="${RUN_AGENT_PACKAGE_INIT}" \
AGENT_PACKAGE_REPO="${AGENT_PACKAGE_REPO}" \
AGENT_PACKAGE_DIRNAME="${AGENT_PACKAGE_DIRNAME}" \
AGENT_PACKAGE_REF="${AGENT_PACKAGE_REF}" \
  "${AFTER_CREATE_CONTAINER_SCRIPT}"

if [[ "${RUN_SERVICE_TESTS}" == "1" ]]; then
  CONTAINER_NAME="${CONTAINER_NAME}" \
  CONTAINER_WORKDIR="${CONTAINER_WORKDIR}" \
  CONTAINER_MODEL_DIR="${CONTAINER_MODEL_DIR}" \
  CONTAINER_DATA_DIR="${CONTAINER_DATA_DIR}" \
  DIND_DOCKER_SOCK="${DIND_DOCKER_SOCK}" \
  SSH_PORT="${SSH_PORT}" \
  RUN_AGENT_PACKAGE_INIT="${RUN_AGENT_PACKAGE_INIT}" \
    "${TEST_SERVICE_SCRIPT}"
fi

docker exec -it "${CONTAINER_NAME}" bash
