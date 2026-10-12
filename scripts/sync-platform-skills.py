#!/usr/bin/env python3
"""Generate platform skill copies from the canonical root skills directory."""
import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def files(directory):
    return {path.relative_to(directory): path.read_bytes()
            for path in directory.rglob('*') if path.is_file()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    canonical = ROOT / 'skills'
    for platform in ('openai', 'claude', 'cursor'):
        destination = ROOT / platform / 'skills'
        if args.check:
            if files(destination) != files(canonical):
                raise SystemExit(f'{platform}/skills is stale; run scripts/sync-platform-skills.py')
        else:
            if destination.exists():
                shutil.rmtree(destination)
            shutil.copytree(canonical, destination)
    print('Platform skills match canonical source.' if args.check else 'Generated platform skills.')


if __name__ == '__main__':
    main()
