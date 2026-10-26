#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="${SCRIPT_DIR}/../references/template"

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

docker exec -i "${CONTAINER_NAME}" bash -s <<'BASH'
set -euo pipefail

touch "${HOME}/.bashrc"
for alias_line in \
  'alias codex-bypass="codex --dangerously-bypass-approvals-and-sandbox"' \
  'alias claude-bypass="claude --allow-dangerously-skip-permissions"'; do
  if ! grep -qxF -- "${alias_line}" "${HOME}/.bashrc"; then
    printf '\n%s\n' "${alias_line}" >> "${HOME}/.bashrc"
  fi
done
BASH

install_global_instruction() {
  local target="$1"
  local template="$2"

  docker exec -i "${CONTAINER_NAME}" bash -c '
    set -euo pipefail
    target="${HOME}/$1"
    mkdir -p "$(dirname "${target}")"
    if [[ ! -s "${target}" ]]; then
      cat > "${target}"
    else
      while IFS= read -r line || [[ -n "${line}" ]]; do
        if ! grep -qxF -- "${line}" "${target}"; then
          printf "\n%s\n" "${line}" >> "${target}"
        fi
      done
    fi
  ' bash "${target}" < "${template}"
}

install_global_instruction ".codex/AGENTS.md" "${TEMPLATE_DIR}/AGENTS.md"
install_global_instruction ".claude/CLAUDE.md" "${TEMPLATE_DIR}/CLAUDE.md"

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
