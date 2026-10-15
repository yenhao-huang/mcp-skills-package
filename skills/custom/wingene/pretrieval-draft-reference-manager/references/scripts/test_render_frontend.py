import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import render_frontend as helper


class FrontendRenderTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'pretrieval-draft-reference-a'
        self.root.mkdir()
        self.sha = 'a' * 40
        self.image = 'sha256:' + 'b' * 64
        self.api_image = 'sha256:' + 'c' * 64
        self.receipt = {'project': self.root.name, 'source_sha': self.sha,
                        'ports': {'api': 28178, 'postgres': 28173, 'qdrant': 28174},
                        'image_ids': {'api': self.api_image}}
        (self.root / 'receipt.json').write_text(json.dumps(self.receipt))
        self.api = {'Image': self.api_image, 'Config': {'Env': ['API_PORT=28178']},
                    'HostConfig': {'NetworkMode': 'host'}, 'State': {'Running': True}}
        self.labels = {'org.opencontainers.image.revision': self.sha, 'ai.pretrieval.source.dirty': 'false', 'ai.pretrieval.role': 'frontend'}
        self.api_labels = {'org.opencontainers.image.revision': self.sha, 'ai.pretrieval.source.dirty': 'false'}
        self.addCleanup(patch.stopall)
        patch.object(helper, 'inspect', side_effect=lambda kind, name: {'Config': {'Labels': self.api_labels if name == self.api_image else self.labels}} if kind == 'image' else self.api).start()
        self.docker = patch.object(helper.subprocess, 'check_output', return_value='').start()
        self.socket = patch.object(helper.socket, 'socket').start()

    def render(self, **kw):
        return helper.render(kw.get('root', self.root), kw.get('image', self.image), kw.get('port', 28179))

    def test_frontend_is_separate_and_has_no_data_mounts(self):
        before = (self.root / 'receipt.json').read_bytes()
        self.render()
        config = json.loads((self.root / 'frontend/docker-compose.yml').read_text())
        self.assertEqual(config['name'], self.root.name + '-ui')
        self.assertEqual(set(config['services']), {'frontend'})
        svc = config['services']['frontend']
        self.assertNotIn('volumes', svc)
        self.assertNotIn('depends_on', svc)
        self.assertEqual(svc['image'], self.image)
        self.assertEqual(svc['environment'], {'API_PORT': '28178', 'FRONTEND_PORT': '28179'})
        self.assertEqual((self.root / 'receipt.json').read_bytes(), before)

    def test_mismatched_source_is_rejected_before_output(self):
        self.labels['org.opencontainers.image.revision'] = 'd' * 40
        with self.assertRaises(ValueError): self.render()
        self.assertFalse((self.root / 'frontend').exists())

    def test_non_frontend_image_is_rejected(self):
        self.labels.pop('ai.pretrieval.role')
        with self.assertRaises(ValueError): self.render()

    def test_mutable_tag_is_rejected(self):
        with self.assertRaises(ValueError): self.render(image='pretrieval-frontend:latest')

    def test_live_api_drift_is_rejected(self):
        self.api['Image'] = 'sha256:' + 'd' * 64
        with self.assertRaises(ValueError): self.render()

    def test_inconsistent_api_receipt_sha_is_rejected(self):
        self.api_labels['org.opencontainers.image.revision'] = 'd' * 40
        with self.assertRaises(ValueError): self.render()

    def test_bridge_api_is_rejected(self):
        self.api['HostConfig']['NetworkMode'] = 'bridge'
        with self.assertRaises(ValueError): self.render()

    def test_database_port_collision_is_rejected(self):
        with self.assertRaises(ValueError): self.render(port=28173)

    def test_occupied_host_port_does_not_write_output(self):
        self.socket.return_value.__enter__.return_value.bind.side_effect = OSError('occupied')
        with self.assertRaises(OSError): self.render()
        self.assertFalse((self.root / 'frontend').exists())

    def test_stopped_existing_container_is_not_overwritten(self):
        self.docker.return_value = self.root.name + '-frontend\n'
        with self.assertRaises(ValueError): self.render()

    def test_existing_preparation_is_not_overwritten(self):
        self.render()
        file = self.root / 'frontend/docker-compose.yml'
        before = file.read_bytes()
        with self.assertRaises(ValueError): self.render()
        self.assertEqual(file.read_bytes(), before)

    def test_symlink_root_is_rejected(self):
        link = Path(self.tmp.name) / 'alias'
        link.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError): self.render(root=link)


if __name__ == '__main__':
    unittest.main()
