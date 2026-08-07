"""String comparison helpers."""

from __future__ import annotations

import os
from pathlib import Path


def find_greatest_common_string(
    strs: list[str] | list[Path], *, case_sensitive: bool = False, min_chars: int = 2
) -> str | None:
    if not strs:
        return ""

    base_names = [os.path.splitext(str(f))[0] for f in strs]
    if not case_sensitive:
        base_names = [name.lower() for name in base_names]

    shortest_name = min(base_names, key=len)
    gcs = ""
    for i in range(len(shortest_name)):
        for j in range(i + 1, len(shortest_name) + 1):
            substring = shortest_name[i:j]
            if all(substring in name for name in base_names) and len(substring) > len(gcs):
                gcs = substring
    return gcs if len(gcs) >= min_chars else None
