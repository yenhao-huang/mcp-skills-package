#!/bin/sh
set -eu
export TZ=Asia/Taipei GIT_TERMINAL_PROMPT=0
umask 077
scripts=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
state=${EXECUTORCH_CRON_STATE:-/home/howard/.local/state/executorch-cron}
mkdir -p "$state/logs"
exec 9>"$state/run.lock"
flock -n 9 || exit 0
exec >>"$state/logs/$(date +%F).log" 2>&1
trap 'rc=$?; echo "Finished $(date -Iseconds) exit=$rc"' EXIT
echo "Started $(date -Iseconds)"
timeout 15m python3 "$scripts/daily_result.py" --repo "$state/daily" --publish
date -Iseconds > "$state/last-success"
