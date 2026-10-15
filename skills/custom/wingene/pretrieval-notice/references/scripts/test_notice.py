import json
from pathlib import Path
import tempfile
import unittest
import notice


def issue(n, user='howard', state='open', pr=None):
    return dict(number=n, title=f'Issue {n}', state=state, pull_request=pr, assignees=[{'login': user}])


class NoticeTests(unittest.TestCase):
    def test_pagination_short_pages_null_pr_and_filtering(self):
        pages = [[issue(1), issue(2, user='leo'), issue(3, pr={'url': 'pr'})],
                 [issue(4), issue(5, state='closed')], []]
        calls = []
        def get(path):
            calls.append(path)
            return pages.pop(0)
        self.assertEqual([x['number'] for x in notice.collect(get)], [1, 4])
        self.assertEqual(len(calls), 3)

    def test_pagination_failure_does_not_return_partial_data(self):
        with self.assertRaises(ValueError):
            notice.collect(lambda _: [issue(1)])
        pages = iter([[issue(1)], {'message': 'error'}])
        with self.assertRaises(ValueError):
            notice.collect(lambda _: next(pages))

    def test_user_order_and_inactive_priorities(self):
        items = [issue(706), issue(705), issue(691)]
        self.assertEqual([x['number'] for x in notice.ordered(items, [705, 999, 691])], [705, 691, 706])
        self.assertEqual([x['number'] for x in notice.ordered(items, [])], [706, 705, 691])

    def test_preferences_persist_clear_and_preserve_other_fields(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'preferences.json'
            self.assertEqual(notice.read_priorities(path), [])
            path.write_text(json.dumps({'unrelated': 'keep'}))
            notice.write_priorities(path, [705, 706, 705])
            self.assertEqual(notice.read_priorities(path), [705, 706])
            self.assertEqual(json.loads(path.read_text())['unrelated'], 'keep')
            notice.write_priorities(path, [])
            self.assertEqual(notice.read_priorities(path), [])
            with self.assertRaises(ValueError):
                notice.write_priorities(path, [-1])
            self.assertEqual(notice.read_priorities(path), [])

    def test_empty_and_priority_output(self):
        self.assertIn('目前沒有指派給 howard', notice.render([], []))
        report = notice.render([issue(706)], [706])
        self.assertIn('【重要】', report)
        self.assertIn('/issues/706', report)
        self.assertIn('共 1 筆', report)


if __name__ == '__main__':
    unittest.main()
