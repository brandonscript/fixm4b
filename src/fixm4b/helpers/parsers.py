"""Small parsers used by the metadata planner."""

from __future__ import annotations

import re
from typing import Any, Literal, overload

from .patterns import lastname_firstname_pattern


@overload
def get_year_from_date(date: Any) -> str: ...


@overload
def get_year_from_date(date: Any, to_int: Literal[True]) -> int: ...


def get_year_from_date(date: Any, to_int: bool = False) -> str | int:
    m = re.search(r"\d{4}", str(date))
    y = m.group(0) if m else ""
    return int(y) if y and to_int else y


def swap_firstname_lastname(name: str) -> str:
    text = (name or "").strip()
    if not text or text.count(",") > 1 or " " not in text:
        return name
    if len(text.split()) > 4:
        return name
    m = lastname_firstname_pattern.match(text)
    if not m:
        return name
    lastname = m.group("lastname")
    firstname = m.group("firstname")
    if firstname and lastname:
        return f"{firstname} {lastname}"
    return name
