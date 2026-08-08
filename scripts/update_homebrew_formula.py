#!/usr/bin/env python3
"""Update a Homebrew formula from a published PyPI source distribution."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.request import urlopen

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:[A-Za-z0-9.-]+)?$")
URL_RE = re.compile(r'(?m)^(\s*url\s+")([^"]+)(")')
SHA256_RE = re.compile(r'(?m)^(\s*sha256\s+")([0-9a-f]{64})(")')


def main() -> int:
    if len(sys.argv) != 4 or not VERSION_RE.fullmatch(sys.argv[2]):
        print(f"Usage: {Path(sys.argv[0]).name} FORMULA_PATH VERSION PACKAGE", file=sys.stderr)
        return 2

    formula_path = Path(sys.argv[1])
    version = sys.argv[2]
    package = sys.argv[3]
    with urlopen(f"https://pypi.org/pypi/{package}/{version}/json") as response:  # noqa: S310
        metadata = json.load(response)

    source = next(
        file
        for file in metadata["urls"]
        if file["packagetype"] == "sdist" and file["url"].endswith(".tar.gz")
    )
    with urlopen(source["url"]) as response:  # noqa: S310
        checksum = hashlib.sha256(response.read()).hexdigest()

    formula = formula_path.read_text(encoding="utf-8")
    updated, url_count = URL_RE.subn(rf"\g<1>{source['url']}\g<3>", formula, count=1)
    updated, sha_count = SHA256_RE.subn(rf"\g<1>{checksum}\g<3>", updated, count=1)
    if url_count != 1 or sha_count != 1:
        raise RuntimeError(f"Could not update URL and sha256 in {formula_path}")

    formula_path.write_text(updated, encoding="utf-8")
    print(f"Updated {formula_path} to {package} {version} ({checksum})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
