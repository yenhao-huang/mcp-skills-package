#!/usr/bin/env bash
set -euo pipefail

DEFAULT_GIT_HTTP_HOST="192.168.1.76:3000"
DEFAULT_GIT_HTTP_USER="howard"

read -r -p "Git HTTP host [$DEFAULT_GIT_HTTP_HOST]: " GIT_HTTP_HOST
GIT_HTTP_HOST="${GIT_HTTP_HOST:-$DEFAULT_GIT_HTTP_HOST}"

read -r -p "Git username [$DEFAULT_GIT_HTTP_USER]: " GIT_HTTP_USER
GIT_HTTP_USER="${GIT_HTTP_USER:-$DEFAULT_GIT_HTTP_USER}"

read -r -s -p "Git password/token: " GIT_HTTP_TOKEN
echo

if [ -z "$GIT_HTTP_TOKEN" ]; then
  echo "Password/token is required." >&2
  exit 1
fi

mkdir -p "$HOME/.config/git"
chmod 700 "$HOME/.config/git"

{
  printf 'GIT_HTTP_HOST=%q\n' "$GIT_HTTP_HOST"
  printf 'GIT_HTTP_USER=%q\n' "$GIT_HTTP_USER"
  printf 'GIT_HTTP_TOKEN=%q\n' "$GIT_HTTP_TOKEN"
} > "$HOME/.config/git/private.env"

chmod 600 "$HOME/.config/git/private.env"

MARKER_BEGIN="# >>> private git http credentials >>>"

if ! grep -qF "$MARKER_BEGIN" "$HOME/.bashrc" 2>/dev/null; then
  cat >> "$HOME/.bashrc" <<'EOF'

# >>> private git http credentials >>>
if [ -f "$HOME/.config/git/private.env" ]; then
  set -a
  . "$HOME/.config/git/private.env"
  set +a
fi

git config --global credential.helper 'cache --timeout=86400' >/dev/null 2>&1

if [ -n "$GIT_HTTP_USER" ] && [ -n "$GIT_HTTP_TOKEN" ] && [ -n "$GIT_HTTP_HOST" ]; then
  printf "protocol=http\nhost=%s\nusername=%s\npassword=%s\n\n" \
    "$GIT_HTTP_HOST" "$GIT_HTTP_USER" "$GIT_HTTP_TOKEN" | git credential approve
fi
# <<< private git http credentials <<<
EOF
fi

set -a
. "$HOME/.config/git/private.env"
set +a

git config --global credential.helper 'cache --timeout=86400'

printf "protocol=http\nhost=%s\nusername=%s\npassword=%s\n\n" \
  "$GIT_HTTP_HOST" "$GIT_HTTP_USER" "$GIT_HTTP_TOKEN" | git credential approve

echo "Done. Run: source ~/.bashrc"
