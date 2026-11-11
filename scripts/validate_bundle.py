#!/usr/bin/env python3
"""Check the vendored bundle's provenance, inventory and SHA-256 digests."""
import argparse
import hashlib
import json
from pathlib import Path
import re


def validate(bundle):
    manifest = json.loads((bundle / 'manifest.json').read_text())
    if manifest.get('format') != 1 or not manifest.get('skills'):
        raise ValueError('Unsupported or empty manifest')
    names = set()
    count = 0
    for entry in manifest['skills']:
        name = entry['name']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or name in names:
            raise ValueError(f'Invalid or duplicate skill name: {name}')
        names.add(name)
        if not re.fullmatch(r'[0-9a-f]{40}', entry['commit']):
            raise ValueError(f'Missing pinned Git commit: {name}')
        if not entry['repository'].startswith('https://github.com/'):
            raise ValueError(f'Unexpected source repository: {name}')
        folder = bundle / 'skills' / name
        if folder.is_symlink() or not folder.is_dir():
            raise ValueError(f'Missing skill directory or symlink: {name}')
        actual = {}
        for file in sorted(folder.rglob('*')):
            if file.is_symlink():
                raise ValueError(f'Symlink in bundle: {file}')
            if file.is_file():
                actual[file.relative_to(folder).as_posix()] = hashlib.sha256(file.read_bytes()).hexdigest()
        if actual != entry['files']:
            raise ValueError(f'File inventory/checksum mismatch: {name}')
        text = (folder / 'SKILL.md').read_text()
        if not text.startswith('---\n') or '\n---' not in text[4:]:
            raise ValueError(f'Missing frontmatter: {name}')
        frontmatter = text[4:].split('\n---', 1)[0]
        declared = re.search(r'^name:\s*[\"\']?([a-z0-9-]+)', frontmatter, re.M)
        if not declared or declared.group(1) != name or not re.search(r'^description:', frontmatter, re.M):
            raise ValueError(f'Invalid skill metadata: {name}')
        if not list(folder.glob('UPSTREAM-LICENSE*')):
            raise ValueError(f'Missing upstream license: {name}')
        provenance = json.loads((folder / 'INSTALL-SOURCE.json').read_text())
        if provenance != {k: v for k, v in entry.items() if k != 'files'}:
            raise ValueError(f'Provenance differs from manifest: {name}')
        count += len(actual)
    discovered = {p.parent.name for p in (bundle / 'skills').rglob('SKILL.md')}
    if discovered != names:
        raise ValueError(f'Unexpected/missing discoverable skills: {discovered ^ names}')
    return manifest, count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, default=Path(__file__).resolve().parents[1] / 'codex-global-skills')
    args = parser.parse_args()
    manifest, count = validate(args.bundle)
    print(f'Validated {len(manifest["skills"])} skills and {count} pinned files.')
