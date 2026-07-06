#!/usr/bin/env bash
set -euo pipefail

echo "請自行確認目前是在 project 根目錄下。"
echo "將從 mcp-skills-package 補齊 package、skills/hooks 到 .codex 與 .claude，並保留既有內容。"

if [[ ! -d mcp-skills-package ]]; then
  echo "FAIL: 找不到 mcp-skills-package，請確認目前是在 project 根目錄下。"
  exit 1
fi

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

list_skills() {
  local target="$1"
  local skills_dir="$target/skills"

  if [[ ! -d "$skills_dir" ]]; then
    return 0
  fi

  find "$skills_dir" -mindepth 2 -maxdepth 2 -name SKILL.md -printf '%P\n' \
    | sed 's#/SKILL.md$##' \
    | sort
}

list_hooks() {
  local target="$1"
  local hooks_dir="$target/hooks"

  if [[ ! -d "$hooks_dir" ]]; then
    return 0
  fi

  find "$hooks_dir" -type f -printf '%P\n' | sort
}

list_package_root_files() {
  local target="$1"

  if [[ ! -d "$target" ]]; then
    return 0
  fi

  find "$target" -maxdepth 1 -type f -printf '%P\n' | sort
}

print_list() {
  local title="$1"
  local file="$2"

  echo "$title"
  if [[ -s "$file" ]]; then
    sed 's/^/  - /' "$file"
  else
    echo "  - (無)"
  fi
}

snapshot_target() {
  local target="$1"
  local label="$2"

  list_skills "$target" > "$tmp_dir/${label}_skills_before"
  list_hooks "$target" > "$tmp_dir/${label}_hooks_before"
  list_package_root_files "$target" > "$tmp_dir/${label}_package_root_before"
}

install_tree_contents() {
  local source_dir="$1"
  local target_dir="$2"

  mkdir -p "$target_dir"
  find "$source_dir" -mindepth 1 -maxdepth 1 -print0 | while IFS= read -r -d '' item; do
    cp -Rn "$item" "$target_dir/"
  done
}

install_package_root_files() {
  local target="$1"

  mkdir -p "$target"
  find mcp-skills-package -mindepth 1 -maxdepth 1 -type f -not -name 'hooks.json' -print0 | while IFS= read -r -d '' item; do
    cp -n "$item" "$target/"
  done
}

install_git_repo() {
  local target="$1"
  local source_git="mcp-skills-package/.git"
  local target_git="$target/.git"

  if [[ ! -e "$source_git" ]]; then
    echo "WARN: 找不到 $source_git，略過 $target 的 Git repo 初始化。"
    return 0
  fi

  if [[ -e "$target_git" ]]; then
    echo "INFO: $target_git 已存在，保留既有 Git repo。"
    return 0
  fi

  cp -a "$source_git" "$target_git"
  echo "OK: 已複製 $source_git 到 $target_git，$target 現在可獨立 git pull/push。"
}

merge_codex_hooks_json() {
  local source_json="mcp-skills-package/hooks.json"
  local target_json=".codex/hooks.json"

  mkdir -p .codex
  if [[ ! -f "$target_json" ]]; then
    cp "$source_json" "$target_json"
    return 0
  fi

  python3 - "$source_json" "$target_json" <<'PY'
import json
import sys
from pathlib import Path

source_path = Path(sys.argv[1])
target_path = Path(sys.argv[2])

with source_path.open("r", encoding="utf-8") as fh:
    source = json.load(fh)

with target_path.open("r", encoding="utf-8") as fh:
    target = json.load(fh)

target_hooks = target.setdefault("hooks", {})
for event, source_entries in source.get("hooks", {}).items():
    target_entries = target_hooks.setdefault(event, [])
    for entry in source_entries:
        if entry not in target_entries:
            target_entries.append(entry)

with target_path.open("w", encoding="utf-8") as fh:
    json.dump(target, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
PY
}

report_target() {
  local target="$1"
  local label="$2"

  list_skills "$target" > "$tmp_dir/${label}_skills_after"
  list_hooks "$target" > "$tmp_dir/${label}_hooks_after"
  list_package_root_files "$target" > "$tmp_dir/${label}_package_root_after"

  comm -13 "$tmp_dir/${label}_skills_before" "$tmp_dir/${label}_skills_after" > "$tmp_dir/${label}_skills_added"
  comm -13 "$tmp_dir/${label}_hooks_before" "$tmp_dir/${label}_hooks_after" > "$tmp_dir/${label}_hooks_added"
  comm -13 "$tmp_dir/${label}_package_root_before" "$tmp_dir/${label}_package_root_after" > "$tmp_dir/${label}_package_root_added"

  echo
  echo "[$target] skills"
  print_list "原有:" "$tmp_dir/${label}_skills_before"
  print_list "新增:" "$tmp_dir/${label}_skills_added"

  echo
  echo "[$target] hooks"
  print_list "原有:" "$tmp_dir/${label}_hooks_before"
  print_list "新增:" "$tmp_dir/${label}_hooks_added"

  echo
  echo "[$target] package root files"
  print_list "原有:" "$tmp_dir/${label}_package_root_before"
  print_list "新增:" "$tmp_dir/${label}_package_root_added"
}

verify_package_items_exist() {
  local target="$1"
  local missing=0
  local source_skill
  local source_hook
  local rel

  while IFS= read -r source_skill; do
    rel="${source_skill#mcp-skills-package/skills/}"
    rel="${rel%/SKILL.md}"
    if [[ ! -f "$target/skills/$rel/SKILL.md" ]]; then
      echo "FAIL: $target 缺少 skill: $rel"
      missing=1
    fi
  done < <(find mcp-skills-package/skills -mindepth 2 -maxdepth 2 -name SKILL.md | sort)

  while IFS= read -r source_hook; do
    rel="${source_hook#mcp-skills-package/hooks/}"
    if [[ ! -f "$target/hooks/$rel" ]]; then
      echo "FAIL: $target 缺少 hook: $rel"
      missing=1
    fi
  done < <(find mcp-skills-package/hooks -type f | sort)

  if [[ "$missing" -ne 0 ]]; then
    exit 1
  fi

  echo "OK: $target 已包含 mcp-skills-package 的所有 skills/hooks。"
}

verify_package_root_files_exist() {
  local target="$1"
  local missing=0
  local source_file
  local rel

  while IFS= read -r source_file; do
    rel="${source_file#mcp-skills-package/}"
    if [[ "$rel" == "hooks.json" ]]; then
      if [[ "$target" == ".codex" && ! -f "$target/hooks.json" ]]; then
        echo "FAIL: $target 缺少檔案: hooks.json"
        missing=1
      fi
      continue
    fi
    if [[ ! -f "$target/$rel" ]]; then
      echo "FAIL: $target 缺少 package root 檔案: $rel"
      missing=1
    fi
  done < <(find mcp-skills-package -maxdepth 1 -type f | sort)

  if [[ "$missing" -ne 0 ]]; then
    exit 1
  fi

  echo "OK: $target 已包含 mcp-skills-package root 的所有檔案。"
}

snapshot_target ".codex" "codex"
snapshot_target ".claude" "claude"

for target in .codex .claude; do
  mkdir -p "$target"
  install_git_repo "$target"
  install_package_root_files "$target"
  install_tree_contents "mcp-skills-package/skills" "$target/skills"
  install_tree_contents "mcp-skills-package/hooks" "$target/hooks"
done

merge_codex_hooks_json

if [[ ! -f .codex/hooks.json ]]; then
  echo "FAIL: .codex/hooks.json 不存在，Codex hook 不會被註冊。"
  exit 1
fi

report_target ".codex" "codex"
report_target ".claude" "claude"

echo
echo "驗證 mcp-skills-package 的 skills/hooks 是否都已存在於目標。"
verify_package_items_exist ".codex"
verify_package_items_exist ".claude"
verify_package_root_files_exist ".codex"
verify_package_root_files_exist ".claude"
echo "OK: .codex/hooks.json 已保留既有設定並補齊 package hook 註冊。"
