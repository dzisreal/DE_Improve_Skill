#!/usr/bin/env python3
"""Check global skill discovery through Codex app-server without calling a model."""
import argparse
import json
import os
from pathlib import Path
import selectors
import shutil
import subprocess
import tempfile
import time


def verify(cwds):
    if shutil.which('codex') is None:
        raise RuntimeError('Codex CLI is not on PATH; verify in a new Codex chat instead.')
    bundle = Path(__file__).resolve().parents[1] / 'codex-global-skills'
    expected = {e['name'] for e in json.loads((bundle / 'manifest.json').read_text())['skills']}
    with tempfile.TemporaryFile() as errors:
        proc = subprocess.Popen(['codex', 'app-server', '--stdio'], stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=errors)
        selector = selectors.DefaultSelector()
        selector.register(proc.stdout, selectors.EVENT_READ)
        buffered = bytearray()

        def send(message):
            proc.stdin.write((json.dumps(message) + '\n').encode())
            proc.stdin.flush()

        def request(request_id, method, params):
            send({'id': request_id, 'method': method, 'params': params})
            deadline = time.monotonic() + 25
            while time.monotonic() < deadline:
                while b'\n' in buffered:
                    raw, _, rest = buffered.partition(b'\n')
                    buffered[:] = rest
                    message = json.loads(raw)
                    if message.get('id') == request_id:
                        if 'error' in message:
                            raise RuntimeError(f'{method}: {message["error"]}')
                        return message['result']
                if not selector.select(timeout=1):
                    continue
                chunk = os.read(proc.stdout.fileno(), 65536)
                if not chunk:
                    raise RuntimeError('Codex app-server exited. Check CLI compatibility and write access to its state directory.')
                buffered.extend(chunk)
            raise TimeoutError(f'Timed out waiting for {method}')

        try:
            request(1, 'initialize', {
                'clientInfo': {'name': 'de_skill_discovery', 'version': '1.0'},
                'capabilities': {'experimentalApi': True},
            })
            send({'method': 'initialized'})
            result = request(2, 'skills/list', {'cwds': cwds, 'forceReload': True})
            rows = result.get('data', [])
            if len(rows) != len(cwds):
                raise RuntimeError('Codex did not return one result per requested directory.')
            for row in rows:
                skills = [s for s in row['skills'] if s['name'] in expected]
                if row.get('errors'):
                    raise RuntimeError(f'Skill discovery errors: {row["errors"]}')
                if {s['name'] for s in skills} != expected:
                    raise RuntimeError(f'Missing selected skills in {row.get("cwd")}')
                if any(s.get('scope') != 'user' or not s.get('enabled') for s in skills):
                    raise RuntimeError('A selected skill is disabled or shadowed by a non-global installation.')
                print(json.dumps({'cwd': row.get('cwd'), 'skills': [s['name'] for s in skills],
                                  'scope': 'user', 'enabled': True}))
        finally:
            selector.close()
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
            proc.stdin.close()
            proc.stdout.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directories', nargs='*', type=Path)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='de-skill-discovery-') as separate:
        cwds = [str(p.resolve()) for p in args.directories] if args.directories else [str(Path.cwd().resolve()), str(Path(separate).resolve())]
        verify(cwds)
