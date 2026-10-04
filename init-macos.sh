#!/usr/bin/env bash
set -euo pipefail

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

if [[ "$(uname -s)" != "Darwin" ]]; then
  fail "init-macos.sh 只能在 macOS 執行。"
fi

command -v rsync >/dev/null 2>&1 || fail "找不到 rsync。"
command -v python3 >/dev/null 2>&1 || fail "找不到 Python 3。"

# The package directory itself is the project home. The script can therefore
# be launched from any working directory without requiring a parent project.
project_home="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
skills_source="$project_home/skills"
hooks_source="$project_home/hooks"
utils_source="$project_home/utils"
hooks_config_source="$project_home/hooks.json"

[[ -d "$skills_source" ]] || fail "找不到 skills source: $skills_source"
[[ -d "$hooks_source" ]] || fail "找不到 hooks source: $hooks_source"
[[ -d "$utils_source" ]] || fail "找不到 utils source: $utils_source"
[[ -f "$hooks_config_source" ]] || fail "找不到 hooks config: $hooks_config_source"

codex_skills="$project_home/.agents/skills"
codex_hooks="$project_home/.codex/hooks"
codex_utils="$project_home/.codex/utils"
codex_hooks_config="$project_home/.codex/hooks.json"
claude_skills="$project_home/.claude/skills"
claude_hooks="$project_home/.claude/hooks"
claude_utils="$project_home/.claude/utils"

echo "Project home: $project_home"
echo "同步 package 內容；更新同名檔案並保留目標中的其他內容。"

sync_tree() {
  local source_dir="$1"
  local target_dir="$2"
  local label="$3"

  mkdir -p "$target_dir"
  rsync -a "$source_dir/" "$target_dir/"
  echo "OK: $label -> $target_dir"
}

sync_tree "$skills_source" "$codex_skills" "Codex skills"
sync_tree "$hooks_source" "$codex_hooks" "Codex hooks"
sync_tree "$utils_source" "$codex_utils" "Codex utils"

# Claude keeps its project-local skills under .claude/skills. Hook scripts and
# utilities are copied for compatibility, while Claude's own settings remain
# untouched.
sync_tree "$skills_source" "$claude_skills" "Claude skills"
sync_tree "$hooks_source" "$claude_hooks" "Claude hooks"
sync_tree "$utils_source" "$claude_utils" "Claude utils"

python3 - "$hooks_config_source" "$codex_hooks_config" "$project_home" <<'PY'
import json
import shlex
import sys
from pathlib import Path

source_path = Path(sys.argv[1])
target_path = Path(sys.argv[2])
project_home = Path(sys.argv[3])

source = json.loads(source_path.read_text(encoding="utf-8"))
if target_path.is_file():
    target = json.loads(target_path.read_text(encoding="utf-8"))
else:
    target = {}

target_hooks = target.setdefault("hooks", {})

# Remove the obsolete context-size gate while preserving unrelated user hooks.
prompt_entries = target_hooks.get("UserPromptSubmit", [])
prompt_entries = [
    entry
    for entry in prompt_entries
    if not any(
        "check_session_size.py" in str(handler.get("command", ""))
        for handler in entry.get("hooks", [])
    )
]
if prompt_entries:
    target_hooks["UserPromptSubmit"] = prompt_entries
else:
    target_hooks.pop("UserPromptSubmit", None)

# Use a stable absolute command because the package directory is the project
# home and Codex sessions may start from one of its subdirectories.
cron_script = project_home / ".codex" / "hooks" / "do-cron-tasks.py"
cron_command = f"python3 {shlex.quote(str(cron_script))}"
for entry in source.get("hooks", {}).get("SessionStart", []):
    for handler in entry.get("hooks", []):
        if "do-cron-tasks.py" in str(handler.get("command", "")):
            handler["command"] = cron_command

# Entries managed by this package are replaced on every sync. Other entries
# remain in their original order.
for event, source_entries in source.get("hooks", {}).items():
    managed_scripts = {
        Path(str(handler.get("command", "")).split()[-1].strip("'\"")).name
        for entry in source_entries
        for handler in entry.get("hooks", [])
        if handler.get("command")
    }
    existing_entries = target_hooks.get(event, [])
    preserved_entries = [
        entry
        for entry in existing_entries
        if not any(
            any(script in str(handler.get("command", "")) for script in managed_scripts)
            for handler in entry.get("hooks", [])
        )
    ]
    target_hooks[event] = preserved_entries + source_entries

target_path.parent.mkdir(parents=True, exist_ok=True)
target_path.write_text(
    json.dumps(target, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
PY

find "$project_home/.codex" "$project_home/.claude" \
  -type f -name '*.sh' -exec chmod +x {} +

echo "OK: Codex hooks 已合併到 $codex_hooks_config"
echo "OK: macOS project 初始化完成。重新啟動 Codex；若 hooks 尚未執行，請使用 /hooks 審查並信任。"
