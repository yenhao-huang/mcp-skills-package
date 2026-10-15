#!/bin/sh
set -eu
export PATH=/usr/local/bin:/usr/bin:/bin
export HOME=/home/howard
export TZ=Asia/Taipei
export GIT_TERMINAL_PROMPT=0
umask 077
state=/home/howard/.local/state/executorch-cron
exec 9>"$state/run.lock"
/usr/bin/flock -n 9 || exit 0
log="$state/logs/$(date +%F).log"
printf '\nStarted %s\n' "$(date -Iseconds)" >> "$log"
if /usr/bin/timeout 15m /usr/bin/python3 /home/howard/.codex/skills/executorch-pm/references/scripts/daily_result.py --repo "$state/daily" --publish >> "$log" 2>&1; then
  printf 'Success %s\n' "$(date -Iseconds)" >> "$log"
  date -Iseconds > "$state/last-success"
else
  result=$?
  printf 'Failed %s (exit %s)\n' "$(date -Iseconds)" "$result" >> "$log"
  exit "$result"
fi
