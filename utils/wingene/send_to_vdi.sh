#!/usr/bin/env bash
set -euo pipefail

SHARE='//192.168.1.2/Projects專案'
USER_NAME='howard.huang'
PASSWORD='bFgf95H3'
REMOTE_DIR='!AI專區/image'

usage() {
    cat <<'EOF'
Usage:
  send_to_vdi FILE [FILE ...]
      Upload file(s) to //192.168.1.2/Projects專案/!AI專區/image.

Examples:
  send_to_vdi ./report.tar.gz
EOF
}

case "${1:-}" in
    "")
        usage >&2
        exit 2
        ;;
    -h|--help)
        usage
        exit 0
        ;;
esac

for file in "$@"; do
    if [[ ! -f "$file" ]]; then
        echo "send_to_vdi: not a file: $file" >&2
        exit 1
    fi

    base_name="$(basename "$file")"
    smbclient "$SHARE" \
        -U "$USER_NAME" \
        --password "$PASSWORD" \
        -m SMB3 \
        -c "cd \"$REMOTE_DIR\"; put \"$file\" \"$base_name\""
done
