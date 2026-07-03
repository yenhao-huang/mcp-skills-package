#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="${CONTAINER_NAME:-}"
CONTAINER_WORKDIR="${CONTAINER_WORKDIR:-/workspace}"
RUN_AGENT_PACKAGE_INIT="${RUN_AGENT_PACKAGE_INIT:-1}"
AGENT_PACKAGE_REPO="${AGENT_PACKAGE_REPO:-git@github.com:yenhao-huang/mcp-skills-package.git}"
AGENT_PACKAGE_DIRNAME="${AGENT_PACKAGE_DIRNAME:-mcp-skills-package}"
AGENT_PACKAGE_REF="${AGENT_PACKAGE_REF:-}"

if [[ -z "${CONTAINER_NAME}" ]]; then
  echo "CONTAINER_NAME must be set." >&2
  exit 1
fi

running="$(docker inspect -f '{{.State.Running}}' "${CONTAINER_NAME}")"
if [[ "${running}" != "true" ]]; then
  echo "Container is not running: ${CONTAINER_NAME}" >&2
  exit 1
fi

if [[ "${RUN_AGENT_PACKAGE_INIT}" != "1" ]]; then
  exit 0
fi

docker exec \
  -e "CONTAINER_WORKDIR=${CONTAINER_WORKDIR}" \
  -e "AGENT_PACKAGE_REPO=${AGENT_PACKAGE_REPO}" \
  -e "AGENT_PACKAGE_DIRNAME=${AGENT_PACKAGE_DIRNAME}" \
  -e "AGENT_PACKAGE_REF=${AGENT_PACKAGE_REF}" \
  "${CONTAINER_NAME}" bash -lc '
    set -euo pipefail
    cd "${CONTAINER_WORKDIR}"

    if [[ -d "${AGENT_PACKAGE_DIRNAME}" && ! -d "${AGENT_PACKAGE_DIRNAME}/.git" ]]; then
      echo "AGENT_PACKAGE_DIRNAME exists but is not a git checkout: ${CONTAINER_WORKDIR}/${AGENT_PACKAGE_DIRNAME}" >&2
      exit 1
    fi

    if [[ ! -d "${AGENT_PACKAGE_DIRNAME}/.git" ]]; then
      git clone --depth 1 "${AGENT_PACKAGE_REPO}" "${AGENT_PACKAGE_DIRNAME}"
    else
      git -C "${AGENT_PACKAGE_DIRNAME}" fetch --depth 1 origin
    fi

    if [[ -n "${AGENT_PACKAGE_REF}" ]]; then
      git -C "${AGENT_PACKAGE_DIRNAME}" fetch --depth 1 origin "${AGENT_PACKAGE_REF}"
      git -C "${AGENT_PACKAGE_DIRNAME}" checkout --detach FETCH_HEAD
    else
      git -C "${AGENT_PACKAGE_DIRNAME}" pull --ff-only
    fi

    bash "${AGENT_PACKAGE_DIRNAME}/init.sh"
  '
