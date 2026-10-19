#!/bin/sh
# This installer targets the existing howard account on the UTC Debian host.
set -eu
mode=${1:---install}
case "$mode" in --install|--print|--remove) ;; *) echo 'Usage: add-cron.sh [--install|--print|--remove]' >&2; exit 2;; esac
job=/etc/cron.d/executorch-daily
backup=/etc/cron.d/.executorch-daily.before-add-cron
if [ "$mode" = --remove ]; then
    if sudo test -e "$backup"; then sudo mv "$backup" "$job"
    elif sudo test -e "$job"; then sudo grep -q "^# Managed by executorch-pm/add-cron.sh" "$job"; sudo rm "$job"; fi
    exit 0
fi
runner=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/run-cron.sh
case "$runner" in *[!a-zA-Z0-9_./-]*) echo 'Unsupported cron path' >&2; exit 1;; esac
[ -x "$runner" ]; sh -n "$runner"
[ "$(cat /etc/timezone)" = Etc/UTC ] || { echo 'Requires UTC host cron timezone' >&2; exit 1; }
id howard >/dev/null
tmp=$(mktemp); trap 'rm -f "$tmp"' EXIT
cat > "$tmp" <<EOF
# Managed by executorch-pm/add-cron.sh; UTC Sunday 20:00 = Taipei Monday 04:00.
SHELL=/bin/sh
PATH=/usr/local/bin:/usr/bin:/bin
HOME=/home/howard
MAILTO=""
0 20 * * * howard "$runner" daily
0 20 * * 0 howard "$runner" weekly
EOF
if [ "$mode" = --print ]; then cat "$tmp"; exit 0; fi
command -v codex >/dev/null
[ -d /home/howard/.local/state/executorch-cron/daily/.git ]
sudo service cron status >/dev/null
if sudo test -e "$job" && ! sudo test -e "$backup" && ! sudo grep -q "^# Managed by executorch-pm/add-cron.sh" "$job"; then sudo cp -p "$job" "$backup"; fi
sudo install -o root -g root -m 0644 "$tmp" /etc/cron.d/.executorch-daily.new
sudo mv /etc/cron.d/.executorch-daily.new "$job"
sudo cat "$job"
