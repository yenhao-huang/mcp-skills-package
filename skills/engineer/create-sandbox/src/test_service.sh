#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="${CONTAINER_NAME:-}"
CONTAINER_WORKDIR="${CONTAINER_WORKDIR:-/workspace}"
CONTAINER_MODEL_DIR="${CONTAINER_MODEL_DIR:-/models}"
CONTAINER_DATA_DIR="${CONTAINER_DATA_DIR:-/data}"
DIND_DOCKER_SOCK="${DIND_DOCKER_SOCK:-/var/run/docker.sock}"
DIND_DATA_DIR="${DIND_DATA_DIR:-/mnt/share_data_78/howard/docker}"
DIND_DATA_ROOT="${DIND_DATA_ROOT:-/var/lib/docker}"
ENABLE_HOST_DOCKER="${ENABLE_HOST_DOCKER:-0}"
CONTAINER_HOST_DOCKER_SOCK="${CONTAINER_HOST_DOCKER_SOCK:-/var/run/host-docker.sock}"
RESTART_POLICY="${RESTART_POLICY:-unless-stopped}"
RUN_AGENT_PACKAGE_INIT="${RUN_AGENT_PACKAGE_INIT:-0}"

if [[ -z "${CONTAINER_NAME}" ]]; then
  echo "CONTAINER_NAME must be set." >&2
  exit 1
fi

pass() {
  printf '[pass] %s\n' "$1"
}

skip() {
  printf '[skip] %s\n' "$1"
}

check_container_running() {
  local running
  running="$(docker inspect -f '{{.State.Running}}' "${CONTAINER_NAME}")"
  if [[ "${running}" != "true" ]]; then
    echo "Container is not running: ${CONTAINER_NAME}" >&2
    exit 1
  fi
  pass "container is running"
}

check_restart_policy() {
  local actual_policy
  actual_policy="$(docker inspect -f '{{.HostConfig.RestartPolicy.Name}}' "${CONTAINER_NAME}")"
  if [[ "${actual_policy}" != "${RESTART_POLICY}" ]]; then
    echo "Unexpected restart policy: expected=${RESTART_POLICY} actual=${actual_policy}" >&2
    exit 1
  fi
  pass "container restart policy is ${RESTART_POLICY}"
}

check_exec() {
  docker exec "${CONTAINER_NAME}" bash -lc 'id -un >/dev/null && test -n "${HOME}"'
  pass "docker exec works"
}

check_agent_clis() {
  docker exec "${CONTAINER_NAME}" bash -lc '
    set -euo pipefail
    command -v codex >/dev/null
    command -v claude >/dev/null
  '
  pass "codex and claude CLIs are installed"
}

check_mounts() {
  docker exec \
    -e "CONTAINER_WORKDIR=${CONTAINER_WORKDIR}" \
    "${CONTAINER_NAME}" bash -lc '
    set -euo pipefail
    test -d "${CONTAINER_WORKDIR}"
    tmp="${CONTAINER_WORKDIR}/.codex-sandbox-write-test.$$"
    : > "${tmp}"
    rm -f "${tmp}"
  '
  pass "workspace mount is writable: ${CONTAINER_WORKDIR}"

  if docker exec "${CONTAINER_NAME}" test -d "${CONTAINER_MODEL_DIR}"; then
    pass "model mount exists: ${CONTAINER_MODEL_DIR}"
  else
    skip "model mount not present: ${CONTAINER_MODEL_DIR}"
  fi

  if docker exec "${CONTAINER_NAME}" test -d "${CONTAINER_DATA_DIR}"; then
    pass "data mount exists: ${CONTAINER_DATA_DIR}"
  else
    skip "data mount not present: ${CONTAINER_DATA_DIR}"
  fi
}

check_ssh() {
  docker exec "${CONTAINER_NAME}" bash -lc '
    set -euo pipefail
    ssh -V >/dev/null 2>&1
    sudo /usr/sbin/sshd -t
    for _ in $(seq 1 15); do
      timeout 1 bash -lc "</dev/tcp/127.0.0.1/22" && break
      sleep 1
    done
    timeout 1 bash -lc "</dev/tcp/127.0.0.1/22"

    if [[ -f "${HOME}/.ssh/id_ed25519" && -f "${HOME}/.ssh/authorized_keys" ]]; then
      ssh -i "${HOME}/.ssh/id_ed25519" \
        -o BatchMode=yes \
        -o ConnectTimeout=5 \
        -o StrictHostKeyChecking=accept-new \
        -o UserKnownHostsFile="${HOME}/.ssh/known_hosts" \
        "$(id -un)@127.0.0.1" true
    fi
  '

  if docker exec "${CONTAINER_NAME}" bash -lc '[[ -f "${HOME}/.ssh/id_ed25519" && -f "${HOME}/.ssh/authorized_keys" ]]'; then
    pass "ssh server accepts key login"
  else
    pass "ssh server config is valid"
    skip "ssh key login not tested because id_ed25519 or authorized_keys is absent"
  fi
}

check_docker() {
  local actual_data_source

  if ! docker exec "${CONTAINER_NAME}" test -S "${DIND_DOCKER_SOCK}"; then
    echo "Docker-in-Docker socket is not present: ${DIND_DOCKER_SOCK}" >&2
    exit 1
  fi

  docker exec "${CONTAINER_NAME}" bash -lc '
    set -euo pipefail
    docker version >/dev/null
    docker info >/dev/null
    test "$(docker info --format "{{.Driver}}")" = "overlay2"
    test "$(docker info --format "{{.DockerRootDir}}")" = "${DIND_DATA_ROOT}"
  '

  actual_data_source="$(
    docker inspect -f \
      "{{range .Mounts}}{{if eq .Destination \"${DIND_DATA_ROOT}\"}}{{.Source}}{{end}}{{end}}" \
      "${CONTAINER_NAME}"
  )"
  if [[ "${actual_data_source}" != "${DIND_DATA_DIR}" ]]; then
    echo "Unexpected Docker data mount: expected=${DIND_DATA_DIR} actual=${actual_data_source}" >&2
    exit 1
  fi

  pass "Docker-in-Docker daemon is ready with overlay2 data at ${DIND_DATA_DIR}"

  if [[ "${ENABLE_HOST_DOCKER}" == "1" ]]; then
    docker exec "${CONTAINER_NAME}" test -S "${CONTAINER_HOST_DOCKER_SOCK}"
    docker exec "${CONTAINER_NAME}" \
      docker -H "unix://${CONTAINER_HOST_DOCKER_SOCK}" info >/dev/null
    pass "host Docker daemon is available through the opt-in socket"
  else
    skip "host Docker disabled"
  fi
}

check_agent_package() {
  if [[ "${RUN_AGENT_PACKAGE_INIT}" != "1" ]]; then
    skip "agent package init disabled"
    return
  fi

  docker exec \
    -e "CONTAINER_WORKDIR=${CONTAINER_WORKDIR}" \
    "${CONTAINER_NAME}" bash -lc '
    set -euo pipefail
    test -d "${CONTAINER_WORKDIR}/mcp-skills-package/.git"
    test -f "${CONTAINER_WORKDIR}/.codex/skills/operations/create-sandbox/SKILL.md" \
      || test -f "${CONTAINER_WORKDIR}/.codex/skills/create-sandbox/SKILL.md" \
      || test -f "${CONTAINER_WORKDIR}/.codex/skills/codex-sandbox/SKILL.md"
    test -f "${CONTAINER_WORKDIR}/.claude/skills/operations/create-sandbox/SKILL.md" \
      || test -f "${CONTAINER_WORKDIR}/.claude/skills/create-sandbox/SKILL.md" \
      || test -f "${CONTAINER_WORKDIR}/.claude/skills/codex-sandbox/SKILL.md"
    test -f "${CONTAINER_WORKDIR}/.codex/hooks.json"
  '
  pass "mcp-skills-package initialized .codex/.claude in workspace"
}

check_container_running
check_restart_policy
check_exec
check_agent_clis
check_mounts
check_ssh
check_docker
check_agent_package
