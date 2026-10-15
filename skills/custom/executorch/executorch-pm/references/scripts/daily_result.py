#!/usr/bin/env python3
"""Read upstream PRs and publish only the personal daily Result snapshot."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import subprocess
from zoneinfo import ZoneInfo

REMOTE = 'https://github.com/yenhao-huang/daily.git'
BASE = 'https://github.com/yenhao-huang/daily/blob/main/'
TABLE = '| 追蹤項目 | 社群 PR | 進度 | 目前狀況／下一步 | 查核時間 |'
SEPARATOR = '| --- | --- | --- | --- | --- |'
PR = re.compile(r'https://redirect\.github\.com/pytorch/executorch/pull/(\d+)')


def command(*args, cwd=None):
    return subprocess.check_output(args, cwd=cwd, text=True, stderr=subprocess.PIPE, timeout=180).strip()


def status(pr):
    return 'Done' if pr['merged'] else 'PR 未 merge'


def rows(text):
    result = {}
    for line in text.splitlines():
        if line.startswith('| ') and (match := PR.search(line)):
            cells = [x.strip() for x in line.strip().strip('|').split('|')]
            if len(cells) == 5:
                result[match[1]] = cells
    return result


def absolute_links(text, source, repo):
    def replace(m):
        link = m[1]
        if ':' in link or link.startswith(('#', '/')):
            return m[0]
        target = (source.parent / link).resolve().relative_to(repo.resolve())
        return '](' + BASE + target.as_posix() + ')'
    return re.sub(r'\]\(([^\s)]+)\)', replace, text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    repo = args.repo.resolve()
    if not repo.exists():
        command('git', 'clone', '--branch', 'main', '--single-branch', REMOTE, str(repo))
    if command('git', 'remote', 'get-url', 'origin', cwd=repo) != REMOTE:
        raise RuntimeError('Unexpected destination repository')
    if command('git', 'status', '--porcelain', cwd=repo):
        raise RuntimeError('Checkout is dirty; preserve files and inspect before retry')
    command('git', 'pull', '--ff-only', 'origin', 'main', cwd=repo)
    # A prior push may have failed after commit; publish that safe pending commit first.
    if command('git', 'rev-list', '--count', 'origin/main..HEAD', cwd=repo) != '0':
        pending = command('git', 'diff', '--name-only', 'origin/main...HEAD', cwd=repo).splitlines()
        if not all(re.fullmatch(r'executorch/\d{4}-\d{2}-\d{2}_\d{6}/Result\.md', p) for p in pending):
            raise RuntimeError('Unexpected pending files')
        if args.publish:
            command('git', 'push', 'origin', 'HEAD:refs/heads/main', cwd=repo)
    files = sorted(repo.glob('executorch/????-??-??_??????/Result.md'))
    if not files:
        raise RuntimeError('No Result.md to carry forward')
    now = dt.datetime.now(ZoneInfo('Asia/Taipei'))
    stamp = now.strftime('%Y-%m-%d %H:%M:%S Asia/Taipei')
    today = now.strftime('%Y-%m-%d')
    current = [p for p in files if p.parent.name.startswith(today + '_')]
    source = files[-1]
    target = current[-1] if current else repo / 'executorch' / now.strftime('%Y-%m-%d_%H%M%S') / 'Result.md'
    text = absolute_links(source.read_text(), source, repo)
    tracked = {}
    for path in files:
        tracked.update(rows(path.read_text()))
    if not tracked:
        raise RuntimeError('No tracked PR rows; inspect report format')
    for number, cells in tracked.items():
        try:
            pr = json.loads(command('gh', 'api', '--method', 'GET', f'repos/pytorch/executorch/pulls/{number}'))
            if pr['number'] != int(number):
                raise ValueError('PR identity mismatch')
            cells[2] = status(pr)
            if pr['merged']:
                note = '已 merge：' + pr['merged_at']
            elif pr['state'] == 'closed':
                note = 'Closed 但未 merge；需用戶確認後續，不能視為 Done。'
            elif pr['draft']:
                note = 'Draft；尚未 merge，等待準備完成與審查。'
            else:
                note = 'Open；尚未 merge，持續追蹤審查與合併狀態。'
            # Preserve earlier review/CI facts and comment links as dated history.
            prior = cells[3].split('〔前次紀錄：', 1)
            history = prior[1] if len(prior) == 2 else cells[4] + '；' + cells[3] + '〕'
            cells[3] = note + '〔前次紀錄：' + history
            cells[4] = stamp
        except (subprocess.SubprocessError, ValueError, KeyError) as exc:
            # Do not overwrite the last verified state or timestamp on failure.
            old = cells[3].split('〔本次查核失敗：', 1)[0]
            cells[3] = old + f'〔本次查核失敗：{stamp}，{type(exc).__name__}；保留上次狀態〕'
    # Replace existing PR table rows, preserving all other sections and selected rows.
    lines = text.splitlines()
    start = lines.index(TABLE)
    end = start + 2
    existing_unissued = []
    while end < len(lines) and lines[end].startswith('|'):
        if not PR.search(lines[end]):
            existing_unissued.append(lines[end])
        end += 1
    lines[start:end] = [TABLE, SEPARATOR] + existing_unissued + ['| ' + ' | '.join(cells) + ' |' for cells in tracked.values()]
    text = '\n'.join(lines) + '\n'
    text = re.sub(r'^批次：.*$', '批次：' + target.parent.name, text, flags=re.M)
    text = re.sub(r'^更新時間：.*$', '更新時間：' + stamp, text, flags=re.M)
    text = re.sub(r'^(報告日期|前次紀錄)：.*\n', '', text, flags=re.M)
    previous = [p for p in files if p.parent.name[:10] < today]
    prev = '[前次 Result.md](' + BASE + previous[-1].relative_to(repo).as_posix() + ')' if previous else '無（首次追蹤日期）'
    text = text.replace('更新時間：' + stamp, f'更新時間：{stamp}\n報告日期：{today} Asia/Taipei\n前次紀錄：{prev}')
    if re.search(r'https://github\.com/pytorch/executorch/(pull|issues)/|pytorch/executorch#', text):
        raise RuntimeError('Unsafe community reference')
    if not args.publish:
        print(json.dumps({'target': str(target), 'PRs': {n: c[2] for n,c in tracked.items()}, 'mode': 'dry-run'}, ensure_ascii=False))
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)
    relative = target.relative_to(repo).as_posix()
    command('git', 'add', '--', relative, cwd=repo)
    if command('git', 'diff', '--cached', '--name-only', cwd=repo) != relative:
        raise RuntimeError('Unexpected staged files')
    command('git', '-c', 'user.name=yenhao-huang', '-c', 'user.email=46972327+yenhao-huang@users.noreply.github.com', 'commit', '-m', 'chore(executorch): update daily PR progress ' + today, cwd=repo)
    command('git', 'push', 'origin', 'HEAD:refs/heads/main', cwd=repo)
    local = command('git', 'rev-parse', 'HEAD', cwd=repo)
    remote = command('git', 'ls-remote', 'origin', 'refs/heads/main', cwd=repo).split()[0]
    if local != remote:
        raise RuntimeError('Remote verification failed')
    print(json.dumps({'report': BASE + relative, 'commit': local, 'PRs': {n:c[2] for n,c in tracked.items()}}, ensure_ascii=False))


if __name__ == '__main__':
    main()
