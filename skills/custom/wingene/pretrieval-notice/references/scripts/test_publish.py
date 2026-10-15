from contextlib import redirect_stdout
from io import StringIO
from datetime import datetime
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import notice
import publish


class ReportTests(unittest.TestCase):
    def test_fixed_format_priority_and_failure(self):
        at = datetime(2026, 10, 15, 8, 30, tzinfo=publish.ZONE)
        items = [dict(number=706, title='Docling'), dict(number=705, title='Analysis')]
        report = notice.render(items, [705], queried_at=at, scheduled_at=at)
        headings = [line for line in report.splitlines() if line.startswith('## ')]
        self.assertEqual(headings, ['## 摘要', '## 重要議題', '## 其他未關閉議題', '## 執行說明'])
        self.assertLess(report.index('[#705]'), report.index('[#706]'))
        self.assertIn('2026-10-15 08:30:00 Asia/Taipei', report)
        failure = notice.render([], [], queried_at=at, error='HTTPError')
        self.assertIn('未關閉總數：無法確認', failure)
        self.assertNotIn('共 0 筆', failure)
        self.assertNotIn('目前沒有指派給', failure)

    def test_failure_report_does_not_publish_exception_secrets(self):
        with patch('notice.authenticated_get', side_effect=ValueError('secret-token')):
            report = publish.make_report(Path('/nonexistent/preferences.json'))
        self.assertIn('ValueError', report)
        self.assertNotIn('secret-token', report)

    def test_manual_query_failure_has_same_report_format(self):
        output = StringIO()
        with patch('sys.argv', ['notice.py', '--preferences', '/missing/prefs.json', 'report']):
            with patch('notice.authenticated_get', side_effect=ValueError('secret')):
                with redirect_stdout(output):
                    self.assertEqual(notice.main(), 1)
        self.assertTrue(output.getvalue().startswith('# PRetrieval 每日 Issue 提醒'))
        self.assertIn('未關閉總數：無法確認', output.getvalue())
        self.assertNotIn('secret', output.getvalue())

    def test_taipei_schedule_and_downtime(self):
        before = datetime.fromisoformat('2026-10-15T00:29:00+00:00')
        self.assertEqual(publish.next_slot(before).isoformat(), '2026-10-15T08:30:00+08:00')
        exact = datetime.fromisoformat('2026-10-15T00:30:00+00:00')
        self.assertEqual(publish.next_slot(exact).isoformat(), '2026-10-16T08:30:00+08:00')
        self.assertEqual(publish.latest_slot(before).isoformat(), '2026-10-14T08:30:00+08:00')
        self.assertEqual(publish.latest_slot(exact).isoformat(), '2026-10-15T08:30:00+08:00')

    def test_pending_retry_reuses_exact_report(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with patch('publish.make_report', return_value='fixed report') as create:
                with patch('publish.publish', side_effect=publish.PublishError('offline')):
                    with self.assertRaises(publish.PublishError):
                        publish.run_once(root, root/'prefs.json')
                pending = json.loads((root/'pending.json').read_text())
                with patch('publish.publish', return_value='wingene/pretrieval/a.md') as push:
                    publish.run_once(root, root/'prefs.json')
                create.assert_called_once()
                self.assertEqual(push.call_args.args[:2], ('fixed report', pending['filename']))
                self.assertFalse((root/'pending.json').exists())


class GitPublisherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.remote = self.root/'remote.git'
        self.seed = self.root/'seed'
        publish.git('init', '--bare', '--initial-branch=main', str(self.remote))
        publish.git('clone', str(self.remote), str(self.seed))
        (self.seed/'keep.md').write_text('existing user content\n')
        publish.git('add', '.', cwd=self.seed)
        publish.git('commit', '-m', 'initial', cwd=self.seed)
        publish.git('push', 'origin', 'main', cwd=self.seed)

    def test_publish_idempotent_and_no_overwrite(self):
        filename = '2026-10-15_083000.md'
        relative = publish.publish('hello\n', filename, str(self.remote))
        sha = publish.git('--git-dir', str(self.remote), 'rev-parse', 'main')
        self.assertEqual(publish.publish('hello\n', filename, str(self.remote)), relative)
        self.assertEqual(publish.git('--git-dir', str(self.remote), 'rev-parse', 'main'), sha)
        self.assertEqual(publish.git('--git-dir', str(self.remote), 'show', 'main:keep.md'), 'existing user content')
        with self.assertRaises(FileExistsError):
            publish.publish('changed\n', filename, str(self.remote))
        with self.assertRaises(ValueError):
            publish.publish('evil', '../README.md', str(self.remote))

    def test_push_race_keeps_concurrent_commit(self):
        def concurrent(attempt):
            if attempt == 0:
                (self.seed/'concurrent.md').write_text('another writer\n')
                publish.git('add', 'concurrent.md', cwd=self.seed)
                publish.git('commit', '-m', 'concurrent', cwd=self.seed)
                publish.git('push', 'origin', 'main', cwd=self.seed)
        publish.publish('report\n', '2026-10-15_083000.md', str(self.remote), concurrent)
        self.assertEqual(publish.git('--git-dir', str(self.remote), 'show', 'main:concurrent.md'), 'another writer')
        self.assertEqual(publish.git('--git-dir', str(self.remote), 'show', 'main:wingene/pretrieval/2026-10-15_083000.md'), 'report')


class StopTick(Exception):
    pass


class SchedulerTests(unittest.TestCase):
    def run_tick(self, directory, at, publication=None):
        with patch('publish.now', return_value=at), patch('publish.time.sleep', side_effect=StopTick):
            with patch('publish.run_once', return_value=publication) as run:
                with self.assertRaises(StopTick):
                    publish.serve(directory, directory/'prefs.json')
                return run

    def test_first_start_waits_for_future_slot(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            at = datetime.fromisoformat('2026-10-15T11:00:00+08:00')
            run = self.run_tick(root, at)
            run.assert_not_called()
            self.assertEqual(json.loads((root/'scheduler.json').read_text())['next_run'],
                             '2026-10-16T08:30:00+08:00')

    def test_restart_catches_latest_due_slot(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            publish.save_json(root/'scheduler.json', {'next_run': '2026-10-13T08:30:00+08:00'})
            at = datetime.fromisoformat('2026-10-15T11:00:00+08:00')
            slot = publish.latest_slot(at)
            result = {'scheduled_at': slot.isoformat(), 'path': 'wingene/pretrieval/2026-10-15_083000.md'}
            run = self.run_tick(root, at, result)
            self.assertEqual(run.call_args.args[2], slot)
            self.assertEqual(json.loads((root/'scheduler.json').read_text())['next_run'],
                             '2026-10-16T08:30:00+08:00')

    def test_restart_after_success_does_not_republish(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            publish.save_json(root/'scheduler.json', {'next_run': '2026-10-15T08:30:00+08:00'})
            publish.save_json(root/'last-published.json', {
                'scheduled_at': '2026-10-15T08:30:00+08:00',
                'path': 'wingene/pretrieval/2026-10-15_083000.md'})
            run = self.run_tick(root, datetime.fromisoformat('2026-10-15T11:00:00+08:00'))
            run.assert_not_called()
            self.assertEqual(json.loads((root/'scheduler.json').read_text())['next_run'],
                             '2026-10-16T08:30:00+08:00')


if __name__ == '__main__':
    unittest.main()
