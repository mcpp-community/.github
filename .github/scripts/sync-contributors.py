#!/usr/bin/env python3
"""Copy the thanks-contributors block from a source README into other READMEs.

The thanks-contributors action only updates one README (`readme_path`), so the
translated READMEs are kept in sync by copying the block between the markers.

Usage: sync-contributors.py <source> <target>...
"""

import re
import sys
from pathlib import Path

BLOCK = re.compile(
    r"<!-- thanks-contributors-flag-start -->.*?<!-- thanks-contributors-flag-end -->",
    re.DOTALL,
)


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    source, *targets = sys.argv[1:]
    match = BLOCK.search(Path(source).read_text(encoding="utf-8"))
    if not match:
        print(f"error: no contributors block in {source}", file=sys.stderr)
        return 1
    block = match.group(0)

    status = 0
    for target in targets:
        path = Path(target)
        content = path.read_text(encoding="utf-8")
        if not BLOCK.search(content):
            print(f"error: no contributors block in {target}", file=sys.stderr)
            status = 1
            continue
        updated = BLOCK.sub(lambda _: block, content, count=1)
        if updated != content:
            path.write_text(updated, encoding="utf-8")
            print(f"updated {target}")
        else:
            print(f"unchanged {target}")
    return status


if __name__ == "__main__":
    sys.exit(main())
