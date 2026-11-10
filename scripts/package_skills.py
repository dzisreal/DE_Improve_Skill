#!/usr/bin/env python3
"""Build a portable ZIP from exactly the manifest-listed files and installer."""
import argparse
import hashlib
from pathlib import Path
import zipfile
from validate_bundle import validate


def build(bundle, output):
    manifest, _ = validate(bundle)
    files = ['README.md', 'install.py', 'manifest.json']
    for entry in manifest['skills']:
        files.extend(f'skills/{entry["name"]}/{relative}' for relative in entry['files'])
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for relative in sorted(files):
            info = zipfile.ZipInfo('codex-global-skills/' + relative, date_time=(2020, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, (bundle / relative).read_bytes())
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix + '.sha256').write_text(f'{digest}  {output.name}\n')
    return digest


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=root / 'dist' / 'codex-global-skills.zip')
    args = parser.parse_args()
    digest = build(root / 'codex-global-skills', args.output)
    print(f'Created {args.output}\nSHA-256: {digest}')
