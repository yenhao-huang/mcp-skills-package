#!/usr/bin/env python3
"""Publish fixed daily reports and run the W78 08:30 scheduler."""
import argparse
from datetime import datetime, timedelta
import fcntl
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time
from zoneinfo import ZoneInfo

import notice

ZONE = ZoneInfo('Asia/Taipei')
REMOTE = 'git@github.com:yenhao-huang/daily.git'
REPORT_DIR = Path('wingene/pretrieval')
REPORT_NAME = re.compile(r'(?:(?P<id>\d{6})_)?(?P<timestamp>\d{4}-\d{2}-\d{2}_\d{6}\.md)')


class PublishError(RuntimeError):
    pass


def now():
    return datetime.now(ZONE)


def slot_today(at):
    return at.astimezone(ZONE).replace(hour=8, minute=30, second=0, microsecond=0)


def next_slot(at):
    slot = slot_today(at)
    return slot if at < slot else slot + timedelta(days=1)


def latest_slot(at):
    slot = slot_today(at)
    return slot if at >= slot else slot - timedelta(days=1)


def git(*args, cwd=None):
    env = {**os.environ, 'GIT_TERMINAL_PROMPT': '0',
           'GIT_AUTHOR_NAME': 'yenhao-huang',
           'GIT_AUTHOR_EMAIL': '46972327+yenhao-huang@users.noreply.github.com',
           'GIT_COMMITTER_NAME': 'yenhao-huang',
           'GIT_COMMITTER_EMAIL': '46972327+yenhao-huang@users.noreply.github.com'}
    result = subprocess.run(['git', *args], cwd=cwd, env=env, capture_output=True,
                            text=True, timeout=120)
    if result.returncode:
        # Git's stderr may contain remote messages or credential-helper output.
        raise PublishError(f'git {args[0]} failed (exit {result.returncode})')
    return result.stdout.strip()


def report_path(checkout, filename):
    reports = []
    for path in (checkout / REPORT_DIR).glob('*.md'):
        match = REPORT_NAME.fullmatch(path.name)
        if path.is_file() and match:
            reports.append((path, match))
    existing = [path for path, match in reports if match['timestamp'] == filename]
    if len(existing) > 1:
        raise FileExistsError('Multiple reports exist for this timestamp')
    if existing:
        return existing[0].relative_to(checkout)
    ids = [int(match['id']) for _, match in reports if match['id'] is not None]
    report_id = min(ids) - 1 if ids else 999999
    if report_id < 0:
        raise ValueError('Report IDs exhausted; refusing to wrap or renumber')
    return REPORT_DIR / f'{report_id:06d}_{filename}'


def publish(text, filename, remote=REMOTE, before_push=None):
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}_\d{6}\.md', filename):
        raise ValueError('Invalid report filename')
    for attempt in range(3):
        try:
            with tempfile.TemporaryDirectory(prefix='pretrieval-publish-') as temp:
                checkout = Path(temp) / 'daily'
                git('clone', '--quiet', '--depth', '1', '--branch', 'main', remote, str(checkout))
                relative = report_path(checkout, filename)
                destination = checkout / relative
                if destination.exists():
                    if destination.read_text(encoding='utf-8') == text:
                        return str(relative)
                    raise FileExistsError('Refusing to replace an existing report')
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(text, encoding='utf-8')
                git('add', '--', str(relative), cwd=checkout)
                git('commit', '--quiet', '-m', f'docs(pretrieval): add {relative.stem} issue report', cwd=checkout)
                if before_push:
                    before_push(attempt)
                git('push', '--quiet', 'origin', 'HEAD:main', cwd=checkout)
                # A fresh clone verifies remote contents, including an uncertain push result.
            with tempfile.TemporaryDirectory(prefix='pretrieval-verify-') as temp:
                git('clone', '--quiet', '--depth', '1', '--branch', 'main', remote, temp)
                if (Path(temp) / relative).read_text(encoding='utf-8') != text:
                    raise PublishError('Remote report verification failed')
            return str(relative)
        except (PublishError, subprocess.TimeoutExpired):
            if attempt == 2:
                raise PublishError('Publish failed after 3 attempts; pending report retained') from None
    raise AssertionError('unreachable')


def save_json(path, value):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def make_report(preferences, scheduled_at=None):
    queried_at = now()
    error = None
    issues, priorities = [], []
    try:
        priorities = notice.read_priorities(preferences)
        issues = notice.collect(notice.authenticated_get())
    except Exception as exc:
        # Never publish arbitrary exception messages or credential output.
        error = type(exc).__name__
    return notice.render(issues, priorities, queried_at=queried_at,
                         scheduled_at=scheduled_at, error=error)


def run_once(state_dir, preferences, scheduled_at=None, remote=REMOTE):
    state_dir.mkdir(parents=True, exist_ok=True)
    with (state_dir / 'run.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        pending = state_dir / 'pending.json'
        if pending.exists():
            payload = json.loads(pending.read_text())
        else:
            slot = scheduled_at or now()
            payload = {'filename': slot.astimezone(ZONE).strftime('%Y-%m-%d_%H%M%S.md'),
                       'scheduled_at': scheduled_at.isoformat() if scheduled_at else None,
                       'report': make_report(preferences, scheduled_at)}
            save_json(pending, payload)
        path = publish(payload['report'], payload['filename'], remote)
        payload['path'] = path
        payload['filename'] = Path(path).name
        save_json(state_dir / 'last-published.json', payload)
        pending.unlink()
        print(json.dumps({'published': path, 'scheduled_at': payload['scheduled_at']}, ensure_ascii=False), flush=True)
        return payload


def serve(state_dir, preferences, remote=REMOTE):
    state_dir.mkdir(parents=True, exist_ok=True)
    # Prevent two scheduler instances with the same state from running at once.
    with (state_dir / 'scheduler.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        state_path = state_dir / 'scheduler.json'
        state = json.loads(state_path.read_text()) if state_path.exists() else {
            'next_run': next_slot(now()).isoformat(), 'last_error': None}
        while True:
            current = now()
            state['heartbeat'] = current.isoformat()
            save_json(state_path, state)
            due = datetime.fromisoformat(state['next_run'])
            pending = state_dir / 'pending.json'
            if pending.exists() or current >= due:
                try:
                    # Recover a prior published slot if interrupted after push but before state update.
                    slot = latest_slot(current) if current >= due else due
                    last_path = state_dir / 'last-published.json'
                    last = json.loads(last_path.read_text()) if last_path.exists() else {}
                    if not pending.exists() and last.get('scheduled_at') == slot.isoformat():
                        payload = last
                    else:
                        payload = run_once(state_dir, preferences, slot if current >= due else None, remote)
                    if payload['scheduled_at']:
                        published_slot = datetime.fromisoformat(payload['scheduled_at'])
                        state['next_run'] = next_slot(published_slot).isoformat()
                    state['last_published'] = payload['path']
                    state['last_error'] = None
                except Exception as exc:
                    state['last_error'] = type(exc).__name__
                    print(json.dumps({'publish_error': type(exc).__name__, 'retry_seconds': 60}), flush=True)
                state['heartbeat'] = now().isoformat()
                save_json(state_path, state)
            time.sleep(60)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['once', 'serve', 'health'])
    parser.add_argument('--state-dir', type=Path, default=Path('/state'))
    parser.add_argument('--preferences', type=Path, default=Path('/preferences/preferences.json'))
    args = parser.parse_args()
    if args.command == 'health':
        state = json.loads((args.state_dir / 'scheduler.json').read_text())
        age = (now() - datetime.fromisoformat(state['heartbeat'])).total_seconds()
        raise SystemExit(0 if age < 300 and not state.get('last_error') else 1)
    if args.command == 'once':
        run_once(args.state_dir, args.preferences)
    else:
        serve(args.state_dir, args.preferences)


if __name__ == '__main__':
    main()
