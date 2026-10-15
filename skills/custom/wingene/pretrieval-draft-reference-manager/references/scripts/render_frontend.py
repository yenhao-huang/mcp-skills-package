#!/usr/bin/env python3
"""Prepare an isolated A/B frontend Compose on W78; never start or stop services."""
import argparse
import json
from pathlib import Path
import re
import socket
import subprocess


def inspect(kind, name):
    return json.loads(subprocess.check_output(['docker', kind, 'inspect', name], text=True))[0]


def render(consumer_dir, image_id, frontend_port):
    root = Path(consumer_dir)
    if not root.is_absolute() or root.resolve() != root or root.name not in {
        'pretrieval-draft-reference-a', 'pretrieval-draft-reference-b'
    }:
        raise ValueError('use an absolute, non-symlink A/B consumer directory on W78')
    receipt = json.loads((root / 'receipt.json').read_text())
    project = root.name
    sha = receipt['source_sha']
    if receipt['project'] != project or not re.fullmatch(r'[0-9a-f]{40}', sha):
        raise ValueError('consumer identity/source mismatch')
    if not re.fullmatch(r'sha256:[0-9a-f]{64}', image_id):
        raise ValueError('frontend image must be an immutable local image ID')
    image = inspect('image', image_id)
    labels = image['Config'].get('Labels') or {}
    if (labels.get('org.opencontainers.image.revision') != sha
            or labels.get('ai.pretrieval.source.dirty') != 'false'
            or labels.get('ai.pretrieval.role') != 'frontend'):
        raise ValueError('frontend source must match the consumer receipt')
    api = inspect('container', project + '-api')
    api_labels = inspect('image', api['Image'])['Config'].get('Labels') or {}
    if (api_labels.get('org.opencontainers.image.revision') != sha
            or api_labels.get('ai.pretrieval.source.dirty') != 'false'):
        raise ValueError('live API image provenance differs from the consumer receipt')
    api_env = dict(entry.split('=', 1) for entry in api['Config']['Env'] if '=' in entry)
    api_port = int(receipt['ports']['api'])
    if (api['Image'] != receipt['image_ids']['api'] or api_env.get('API_PORT') != str(api_port)
            or api['HostConfig']['NetworkMode'] != 'host' or not api['State']['Running']):
        raise ValueError('live API differs from the receipt or is not a running host-network service')
    if not 1024 <= frontend_port <= 65535 or frontend_port in receipt['ports'].values():
        raise ValueError('frontend port must be distinct and unprivileged')
    names = subprocess.check_output(['docker', 'ps', '-a', '--format', '{{.Names}}'], text=True).splitlines()
    if project + '-frontend' in names:
        raise ValueError('frontend already exists; use its saved Compose/receipt')
    # This CLI must run over SSH on W78, not inside the agent sandbox.
    with socket.socket() as probe:
        probe.bind(('0.0.0.0', frontend_port))
    output = root / 'frontend'
    if output.exists() or output.is_symlink():
        raise ValueError('frontend output already exists; inspect it rather than overwrite')
    compose = {
        'name': project + '-ui',
        'services': {'frontend': {
            'image': image_id, 'pull_policy': 'never',
            'container_name': project + '-frontend', 'network_mode': 'host',
            'environment': {'FRONTEND_PORT': str(frontend_port), 'API_PORT': str(api_port)},
            'restart': 'unless-stopped',
            'logging': {'driver': 'json-file', 'options': {'max-size': '10m', 'max-file': '3'}},
            'healthcheck': {'test': ['CMD-SHELL', f'wget -q -O /dev/null http://127.0.0.1:{frontend_port}/ && wget -q -O /dev/null http://127.0.0.1:{frontend_port}/api/health'],
                            'interval': '15s', 'timeout': '5s', 'retries': 6, 'start_period': '10s'},
        }},
    }
    record = {'project': project + '-ui', 'container_name': project + '-frontend',
              'source_sha': sha, 'image_id': image_id, 'api_image_id': api['Image'],
              'api_port': api_port, 'frontend_port': frontend_port,
              'consumer_dir': str(root), 'compose_file': str(output / 'docker-compose.yml')}
    output.mkdir(mode=0o755)
    # Preserve any partial preparation for inspection; never touch consumer data.
    (output / 'docker-compose.yml').write_text(json.dumps(compose, indent=2) + '\n')
    (output / 'receipt.json').write_text(json.dumps(record, indent=2) + '\n')
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--consumer-dir', required=True)
    parser.add_argument('--image-id', required=True)
    parser.add_argument('--frontend-port', required=True, type=int)
    args = parser.parse_args()
    print(json.dumps(render(args.consumer_dir, args.image_id, args.frontend_port), indent=2))


if __name__ == '__main__':
    main()
