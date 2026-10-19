#!/bin/sh
set -eu
runner=/home/howard/.codex/skills/executorch-pm/references/scripts/run-cron.sh
[ -x "$runner" ]
[ "$(cat /etc/timezone)" = Etc/UTC ]
tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT
printf '%s\n' 'SHELL=/bin/sh' 'PATH=/usr/local/bin:/usr/bin:/bin' 'HOME=/home/howard' 'MAILTO=""' "0 20 * * * howard $runner daily" "0 20 * * 0 howard $runner weekly" > "$tmp"
sudo install -o root -g root -m 0644 "$tmp" /etc/cron.d/executorch-daily
sudo service cron start
