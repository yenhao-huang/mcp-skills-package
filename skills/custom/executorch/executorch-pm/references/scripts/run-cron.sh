#!/bin/sh
set -eu
umask 077
export TZ=Asia/Taipei GIT_TERMINAL_PROMPT=0
case "${1:-}" in daily|weekly) ;; *) echo 'Usage: run-cron.sh daily|weekly' >&2; exit 2;; esac
state=${EXECUTORCH_CRON_STATE:-/home/howard/.local/state/executorch-cron}
mkdir -p "$state/logs"
exec 9>"$state/run.lock"; flock -w 7200 9
exec >>"$state/logs/$(date +%F)-$1.log" 2>&1
timeout 90m codex exec --sandbox danger-full-access -c 'approval_policy="never"' --ephemeral --skip-git-repo-check -C /workspace/executorch-worktrees/daily -o "$state/$1-last-message.txt" "Read /home/howard/.codex/skills/executorch-pm/SKILL.md and follow Scheduled execution for $1 mode. Never invoke this launcher recursively."
