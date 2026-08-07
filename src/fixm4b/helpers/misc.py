"""Shared tiny helpers for fixm4b (no auto-m4b deps)."""

from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any, TypeVar

T = TypeVar("T")
Mf = TypeVar("Mf")


def re_group(match: re.Match[str] | None, group: int | str = 1, *, default: str = "") -> str:
    if not match:
        return default
    try:
        value = match.group(group)
    except IndexError:
        return default
    return default if value is None else str(value)


def parse_bool(v: Any) -> bool:
    if isinstance(v, bool):
        return v
    if v is None:
        return False
    s = str(v).strip().lower()
    if s in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if s in {"0", "false", "f", "no", "n", "off", ""}:
        return False
    return bool(v)


def max_if(iterable: Iterable[T], fallback: Mf | None = None) -> T | Mf | None:
    items = list(iterable)
    return max(items) if items else fallback
