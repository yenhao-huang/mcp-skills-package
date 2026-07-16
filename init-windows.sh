#!/usr/bin/env bash
set -euo pipefail

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

to_unix_path() {
  local path="$1"

  if [[ "$path" =~ ^[A-Za-z]:[\\/] ]]; then
    if command -v cygpath >/dev/null 2>&1; then
      cygpath -u "$path"
      return
    fi
    if command -v wslpath >/dev/null 2>&1; then
      wslpath -u "$path"
      return
    fi
    fail "無法轉換 Windows 路徑: $path"
  fi

  printf '%s\n' "$path"
}

os_name="$(uname -s 2>/dev/null || true)"
case "$os_name" in
  MINGW*|MSYS*|CYGWIN*)
    windows_shell="Git Bash"
    ;;
  Linux*)
    if grep -qi microsoft /proc/version 2>/dev/null; then
      windows_shell="WSL"
    else
      windows_shell="Linux Bash"
    fi
    ;;
  *)
    windows_shell="$os_name"
    ;;
esac

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
project_root="$(to_unix_path "${1:-$PWD}")"
[[ -d "$project_root" ]] || fail "project 根目錄不存在: $project_root"
project_root="$(cd -- "$project_root" && pwd -P)"

expected_package_dir="$project_root/mcp-skills-package"
[[ -d "$expected_package_dir" ]] || fail "找不到 $expected_package_dir"
expected_package_dir="$(cd -- "$expected_package_dir" && pwd -P)"
[[ "$script_dir" == "$expected_package_dir" ]] || \
  fail "請將 mcp-skills-package 放在目標 project 根目錄下再執行。"

echo "Windows shell: $windows_shell"
echo "Project root: $project_root"
echo "正在將 package 內的 shell scripts 轉換為 LF line endings。"

while IFS= read -r -d '' script; do
  sed -i 's/\r$//' "$script"
done < <(find "$script_dir" -type f -name '*.sh' -print0)

cd "$project_root"
bash "$script_dir/init.sh"

find .codex .claude -type f -name '*.sh' -exec chmod +x {} +
echo "OK: Windows 初始化完成。"
