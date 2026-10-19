#!/bin/bash
# One-file daily Result job; requires bash, gh, git, jq and GNU coreutils.
set -euo pipefail
export TZ=Asia/Taipei GIT_TERMINAL_PROMPT=0
umask 077
state=${EXECUTORCH_CRON_STATE:-/home/howard/.local/state/executorch-cron}
if [[ ${1:-} != --worker ]]; then
    mkdir -p "$state/logs"; exec 9>"$state/run.lock"; flock -n 9 || exit 0
    exec >>"$state/logs/$(date +%F).log" 2>&1
    trap 'rc=$?; echo "Finished $(date -Iseconds) exit=$rc"' EXIT
    echo "Started $(date -Iseconds)"
    timeout 15m bash "$0" --worker "$@"
    [[ ${1:-} == --dry-run ]] || date -Iseconds > "$state/last-success"
    exit 0
fi
shift
[[ $# == 0 || ( $# == 1 && $1 == --dry-run ) ]] || { echo 'Usage: run-cron.sh [--dry-run]'; exit 2; }
publish=true; [[ ${1:-} != --dry-run ]] || publish=false
repo=$state/daily; remote=https://github.com/yenhao-huang/daily.git
base=https://github.com/yenhao-huang/daily/blob/main
fail() { echo "$*" >&2; exit 1; }
[[ -d $repo ]] || git clone --branch main --single-branch "$remote" "$repo"
cd "$repo"
[[ $(git remote get-url origin) == "$remote" && $(git branch --show-current) == main ]] || fail 'Unexpected destination/branch'
[[ -z $(git status --porcelain) ]] || fail 'Dirty checkout; preserve files and inspect'
git pull --ff-only origin main
if [[ $(git rev-list --count origin/main..HEAD) != 0 ]]; then
    # Inspect every pending commit, not only its net diff, before retrying a push.
    while read -r commit; do
        git diff-tree --no-commit-id --name-only -r "$commit" | grep -Ev '^executorch/[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{6}/Result\.md$' && fail 'Unexpected pending files'
        git show "$commit" | grep -Eq 'https://github\.com/pytorch/executorch/(pull|issues)/|pytorch/executorch#' && fail 'Unsafe pending reference'
    done < <(git rev-list origin/main..HEAD)
    $publish && git push origin HEAD:refs/heads/main
fi
shopt -s nullglob
files=(executorch/????-??-??_??????/Result.md)
((${#files[@]})) || fail 'No prior Result.md'
today=$(date +%F); stamp=$(date '+%F %T Asia/Taipei'); source=${files[-1]}
current=(executorch/"$today"_??????/Result.md)
target=executorch/$(date +%F_%H%M%S)/Result.md
((${#current[@]} == 0)) || target=${current[-1]}
previous='無（首次追蹤日期）'
for f in "${files[@]}"; do [[ ${f:11:10} < $today ]] && previous="[前次 Result.md]($base/$f)"; done
work=$(mktemp -d); trap 'rm -rf "$work"' EXIT
# Five-column tracking rows only; selected-issue rows have a different shape.
awk -F '|' 'NF==7 && $3 ~ /redirect.github.com\/pytorch\/executorch\/pull\/[0-9]+/ {print}' "${files[@]}" |
 jq -Rs 'split("\n") | map(select(length>0) | split("|")[1:6] | map(gsub("^ +| +$";""))) | reduce .[] as $r ({}; .[($r[1]|capture("/pull/(?<n>[0-9]+)").n)]=$r)' > "$work/rows.json"
[[ $(jq length "$work/rows.json") != 0 ]] || fail 'No tracked PRs'
while read -r number; do
    if gh api --method GET "repos/pytorch/executorch/pulls/$number" > "$work/pr.json" &&
       jq -e --argjson n "$number" '.number==$n and (.merged|type=="boolean") and (.state=="open" or .state=="closed") and (.draft|type=="boolean") and (if .merged then (.merged_at|type=="string") else true end)' "$work/pr.json" >/dev/null; then
        jq --arg n "$number" --arg stamp "$stamp" --slurpfile pr "$work/pr.json" '
          .[$n] |= (. as $old | ($pr[0]) as $p |
          .[2]=(if $p.merged then "Done" else "PR 未 merge" end) |
          .[3]=((if $p.merged then "已 merge："+$p.merged_at elif $p.state=="closed" then "Closed 但未 merge；需用戶確認後續，不能視為 Done。" elif $p.draft then "Draft；尚未 merge，等待準備完成與審查。" else "Open；尚未 merge，持續追蹤審查與合併狀態。" end)
          +"〔前次紀錄："+(if $old[3]|contains("〔前次紀錄：") then ($old[3]|split("〔前次紀錄：")[1]|split("〔本次查核失敗：")[0]) else $old[4]+"；"+($old[3]|split("〔本次查核失敗：")[0])+"〕" end)) | .[4]=$stamp)' "$work/rows.json" > "$work/next.json"
    else
        jq --arg n "$number" --arg stamp "$stamp" '.[$n][3] |= (split("〔本次查核失敗：")[0]+"〔本次查核失敗："+$stamp+"；保留上次狀態〕")' "$work/rows.json" > "$work/next.json"
    fi
    mv "$work/next.json" "$work/rows.json"
done < <(jq -r 'keys[]' "$work/rows.json")
jq -r '.[] | "| "+join(" | ")+" |"' "$work/rows.json" > "$work/rows.md"
# Resolve relative Markdown links against the source batch before carrying it forward.
link_re='\]\(([^[:space:])]+)\)'
while IFS= read -r line || [[ -n $line ]]; do
    rest=$line; output=''
    while [[ $rest =~ $link_re ]]; do
        match=${BASH_REMATCH[0]}; link=${BASH_REMATCH[1]}; output+=${rest%%"$match"*}; rest=${rest#*"$match"}
        if [[ $link != *:* && $link != \#* && $link != /* ]]; then
            resolved=$(realpath -m "$(dirname "$source")/$link"); [[ $resolved == "$PWD/"* ]] || fail 'Link escapes repo'
            match="]($base/${resolved#"$PWD/"})"
        fi
        output+=$match
    done
    printf '%s\n' "$output$rest"
done < "$source" > "$work/source.md"
awk -v rows="$work/rows.md" -v batch="$(basename "$(dirname "$target")")" -v stamp="$stamp" -v today="$today" -v prev="$previous" '
 /^批次：/ {print "批次：" batch; next}
 /^更新時間：/ {print "更新時間：" stamp "\n報告日期：" today " Asia/Taipei\n前次紀錄：" prev; next}
 /^(報告日期|前次紀錄)：/ {next}
 /^\| 追蹤項目 \| 社群 PR \| 進度 \| 目前狀況／下一步 \| 查核時間 \|$/ {found=1; table=1; print; getline; print; while ((getline r < rows)>0) print r; close(rows); next}
 table && /^\|/ {if ($0 !~ /redirect.github.com\/pytorch\/executorch\/pull\/[0-9]+/) print; next}
 {table=0; print}
 END {if (!found) exit 1}' "$work/source.md" > "$work/Result.md"
grep -Eq 'https://github\.com/pytorch/executorch/(pull|issues)/|pytorch/executorch#' "$work/Result.md" && fail 'Unsafe community reference'
if ! $publish; then echo "Dry-run: $target"; cat "$work/Result.md"; exit 0; fi
mkdir -p "$(dirname "$target")"; cp "$work/Result.md" "$target"
git add -- "$target"
if ! git diff --cached --quiet; then
    [[ $(git diff --cached --name-only) == "$target" ]] || fail 'Unexpected staged files'
    git -c user.name=yenhao-huang -c user.email=46972327+yenhao-huang@users.noreply.github.com commit -m "chore(executorch): update daily PR progress $today"
    git push origin HEAD:refs/heads/main
fi
[[ $(git rev-parse HEAD) == $(git ls-remote origin refs/heads/main | cut -f1) ]] || fail 'Remote verification failed'
echo "Published: $base/$target ($(git rev-parse HEAD))"
