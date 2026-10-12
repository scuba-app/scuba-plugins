#!/usr/bin/env python3
"""Build platform package archives."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parent.parent
FILES = {
    'openai': ('plugin.json', 'mcp.json', 'README.md', 'LICENSE', 'assets/icon.png', 'assets/icon.svg'),
    'cursor': ('.cursor-plugin/plugin.json', 'mcp.json', 'README.md', 'LICENSE', 'assets/icon.svg'),
    'claude': ('.claude-plugin/plugin.json', '.mcp.json', 'README.md', 'LICENSE', 'assets/icon.svg'),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    subprocess.run([sys.executable, str(ROOT / 'scripts/sync-platform-skills.py'), '--check'], check=True)
    args.output.mkdir(parents=True, exist_ok=True)
    checksums = []
    for platform, names in FILES.items():
        package = ROOT / platform
        for name in names:
            if name.endswith('.json'):
                json.loads((package / name).read_text())
        sources = {name: package / name for name in names}
        sources.update({str(path.relative_to(ROOT)): path for path in sorted((ROOT / 'skills').rglob('*')) if path.is_file()})
        archive = args.output / f'scuba-{platform}.zip'
        with ZipFile(archive, 'w', compression=ZIP_DEFLATED) as output:
            for name in sorted(sources):
                info = ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
                info.compress_type = ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                output.writestr(info, sources[name].read_bytes())
        with ZipFile(archive) as output:
            assert set(output.namelist()) == set(sources)
            assert output.testzip() is None
        checksums.append(f'{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}')
        print(f'{archive}: {len(sources)} files, verified')
    (args.output / 'SHA256SUMS').write_text('\n'.join(checksums) + '\n')


if __name__ == '__main__':
    main()
