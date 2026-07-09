#!/usr/bin/env bash
set -euo pipefail

bashrc="${HOME}/.bashrc"
alias_name="codex-bypass"
alias_line="alias ${alias_name}='codex --dangerously-bypass-approvals-and-sandbox'"
marker_begin="# >>> codex-bypass alias >>>"
marker_end="# <<< codex-bypass alias <<<"

mkdir -p "$(dirname "$bashrc")"
touch "$bashrc"

if grep -Fqx "$alias_line" "$bashrc"; then
  printf 'Already configured: %s\n' "$alias_line"
  printf 'Run this to load it in the current shell: source ~/.bashrc\n'
  exit 0
fi

backup="${bashrc}.bak.$(date +%Y%m%d%H%M%S)"
cp "$bashrc" "$backup"

tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

if grep -Fqx "$marker_begin" "$bashrc" && grep -Fqx "$marker_end" "$bashrc"; then
  awk -v begin="$marker_begin" -v end="$marker_end" -v line="$alias_line" '
    $0 == begin {
      print begin
      print line
      in_block = 1
      next
    }
    $0 == end {
      print end
      in_block = 0
      next
    }
    !in_block {
      print
    }
  ' "$bashrc" > "$tmp"
  mv "$tmp" "$bashrc"
  printf 'Updated existing %s block in %s\n' "$alias_name" "$bashrc"
else
  {
    printf '\n%s\n' "$marker_begin"
    printf '%s\n' "$alias_line"
    printf '%s\n' "$marker_end"
  } >> "$bashrc"
  printf 'Added %s to %s\n' "$alias_name" "$bashrc"
fi

printf 'Backup: %s\n' "$backup"
printf 'Run this to load it in the current shell: source ~/.bashrc\n'
