#!/usr/bin/env python3
"""Set the fixm4b version in every source-controlled location."""

from __future__ import annotations

import re
import sys
from pathlib import Path

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:[A-Za-z0-9.-]+)?$")
ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"
INIT = ROOT / "src" / "fixm4b" / "__init__.py"


def update_version(path: Path, pattern: str, replacement: str) -> None:
    text = path.read_text()
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise RuntimeError(f"Expected exactly one version declaration in {path}")
    path.write_text(updated)


def main() -> int:
    if len(sys.argv) != 2 or not VERSION_RE.fullmatch(sys.argv[1]):
        print(f"Usage: {Path(sys.argv[0]).name} VERSION", file=sys.stderr)
        print("VERSION must be in the form MAJOR.MINOR.PATCH.", file=sys.stderr)
        return 2

    version = sys.argv[1]
    update_version(
        PYPROJECT,
        r'^(version\s*=\s*")[^"]+(")$',
        rf"\g<1>{version}\g<2>",
    )
    update_version(
        INIT,
        r'^(__version__\s*=\s*")[^"]+(")$',
        rf"\g<1>{version}\g<2>",
    )
    print(f"Set fixm4b version to {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
