#!/usr/bin/env python3
"""Install the pinned bundle as user-global Codex skills, without overwriting files."""
import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path


def digest_tree(path):
    if path.is_symlink():
        raise ValueError(f'Refusing symlink: {path}')
    result = {}
    for file in sorted(path.rglob('*')):
        if file.is_symlink():
            raise ValueError(f'Refusing symlink: {file}')
        if file.is_file():
            result[str(file.relative_to(path))] = hashlib.sha256(file.read_bytes()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, default=Path.home()/'.agents'/'skills')
    parser.add_argument('--check', action='store_true', help='Validate bundle and report installation state without writing')
    args = parser.parse_args()
    bundle = Path(__file__).resolve().parent
    manifest = json.loads((bundle/'manifest.json').read_text())
    destination = args.destination.expanduser()
    if any(p.is_symlink() for p in [destination, *destination.parents]):
        raise ValueError('Destination must not contain symlinks; pass its resolved path explicitly.')
    pending = []
    for entry in manifest['skills']:
        name = entry['name']
        if Path(name).name != name or name in ('.', '..'):
            raise ValueError(f'Invalid skill name: {name}')
        source = bundle/'skills'/name
        target = destination/name
        if digest_tree(source) != entry['files']:
            raise ValueError(f'Bundle checksum mismatch: {name}')
        if target.exists() or target.is_symlink():
            if not target.is_dir() or digest_tree(target) != entry['files']:
                raise ValueError(f'Existing skill differs; no files were changed: {target}')
            print(f'Already installed: {name}')
        else:
            pending.append((source, target, entry))
    if args.check:
        print(f'Bundle verified. {len(pending)} skills not installed at {destination}.')
        return
    created = []
    try:
        destination.mkdir(parents=True, exist_ok=True)
        for source, target, entry in pending:
            # mkdir is exclusive, so a concurrent install cannot be overwritten.
            target.mkdir()
            created.append(target)
            shutil.copytree(source, target, dirs_exist_ok=True)
            if digest_tree(target) != entry['files']:
                raise ValueError(f'Installed checksum mismatch: {target.name}')
            print(f'Installed: {target.name}')
    except Exception:
        for target in reversed(created):
            shutil.rmtree(target)
        raise
    print(f'Global skills directory: {destination}')
    print('Start a new Codex chat to refresh skill discovery.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError) as exc:
        print(f'Installation stopped: {exc}', file=sys.stderr)
        sys.exit(1)
