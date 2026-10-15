#!/usr/bin/env python3
"""Read-only Gitea briefing and local user priority preferences."""
import argparse
import base64
from datetime import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from zoneinfo import ZoneInfo

BASE = 'http://192.168.1.76:3000'
REPO = 'leo/PRetrieval'
ASSIGNEE = 'howard'
DEFAULT_PREFS = Path.home() / '.config/pretrieval-notice/preferences.json'


def read_priorities(path):
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding='utf-8'))
    values = data['priority_issues']
    if not isinstance(values, list) or any(type(n) is not int or n <= 0 for n in values):
        raise ValueError('Invalid priority_issues; expected positive issue numbers')
    return list(dict.fromkeys(values))


def write_priorities(path, values):
    if any(type(n) is not int or n <= 0 for n in values):
        raise ValueError('Issue numbers must be positive integers')
    data = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    data['priority_issues'] = list(dict.fromkeys(values))
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.preferences-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as out:
            json.dump(data, out, ensure_ascii=False, indent=2)
            out.write('\n')
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('Unexpected Gitea redirect; credentials were not forwarded')


def authenticated_get():
    result = subprocess.run(
        ['git', 'credential', 'fill'],
        input='protocol=http\nhost=192.168.1.76:3000\n\n',
        text=True, capture_output=True, timeout=20,
        env={**os.environ, 'GIT_TERMINAL_PROMPT': '0', 'GIT_ASKPASS': '/bin/false'},
    )
    if result.returncode:
        raise ValueError('Gitea credential unavailable; configure the existing Git helper')
    creds = dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)
    if not creds.get('username') or not creds.get('password'):
        raise ValueError('Incomplete Gitea credential')
    auth = base64.b64encode((creds['username'] + ':' + creds['password']).encode()).decode()
    opener = urllib.request.build_opener(NoRedirect)

    def get(path):
        req = urllib.request.Request(BASE + path, headers={'Authorization': 'Basic ' + auth})
        with opener.open(req, timeout=30) as response:
            return json.load(response)

    user = get('/api/v1/user')
    if not isinstance(user, dict) or not user.get('login'):
        raise ValueError('Could not verify authenticated Gitea user')
    return get


def collect(get):
    issues = {}
    seen = set()
    for page in range(1, 1001):
        rows = get(f'/api/v1/repos/{REPO}/issues?state=open&limit=50&page={page}')
        if not isinstance(rows, list):
            raise ValueError('Invalid issue list response')
        if not rows:
            return list(issues.values())
        numbers = {x['number'] for x in rows}
        if numbers <= seen:
            raise ValueError('Pagination made no progress; no partial report returned')
        seen.update(numbers)
        for issue in rows:
            # Gitea includes a null pull_request field on ordinary issues.
            if issue.get('pull_request') or issue.get('state') != 'open':
                continue
            assignees = issue.get('assignees') or ([issue['assignee']] if issue.get('assignee') else [])
            if any(a.get('login', '').casefold() == ASSIGNEE for a in assignees):
                issues[issue['number']] = issue
    raise ValueError('Pagination limit reached; no partial report returned')


def ordered(issues, priorities):
    ranks = {number: rank for rank, number in enumerate(priorities)}
    return sorted(issues, key=lambda x: (ranks.get(x['number'], len(ranks)), -x['number']))


def safe_title(title):
    title = ' '.join(title.split())
    for char in '\\`*_[]<>|':
        title = title.replace(char, '\\' + char)
    return title


def render(issues, priorities):
    timestamp = datetime.now(ZoneInfo('Asia/Taipei')).strftime('%Y-%m-%d %H:%M %Z')
    lines = [f'PRetrieval 未關閉 issue（{timestamp}）', f'負責人：{ASSIGNEE}；共 {len(issues)} 筆。', '']
    if not issues:
        lines.append('目前沒有指派給 howard 的未關閉 issue。')
    for issue in ordered(issues, priorities):
        number = issue['number']
        marker = '【重要】' if number in priorities else ''
        lines.append(f'- {marker}[#{number}]({BASE}/{REPO}/issues/{number}) {safe_title(issue["title"])}')
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preferences', type=Path, default=DEFAULT_PREFS)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('report')
    commands.add_parser('priorities')
    priority = commands.add_parser('prioritize')
    priority.add_argument('numbers', nargs='*', type=int)
    priority.add_argument('--clear', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'prioritize':
            if bool(args.numbers) == args.clear:
                raise ValueError('Provide issue numbers or --clear, exclusively')
            write_priorities(args.preferences, args.numbers)
        priorities = read_priorities(args.preferences)
        if args.command == 'report':
            print(render(collect(authenticated_get()), priorities))
        else:
            print(json.dumps({'priority_issues': priorities}, ensure_ascii=False))
    except urllib.error.HTTPError as error:
        print(f'查詢失敗：Gitea HTTP {error.code}；未產生 issue 摘要。', file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError, urllib.error.URLError) as error:
        # Do not echo arbitrary remote error bodies, credential-helper output, or secrets.
        print(f'執行失敗（{type(error).__name__}）；請檢查連線、既有認證及優先順序設定。未產生摘要。', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
