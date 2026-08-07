"""Regex patterns used by OL lookup / parsers."""

from __future__ import annotations

import re

lastname_firstname_pattern = re.compile(r"^(?P<lastname>.*?), (?P<firstname>.*)$", re.I)
junk_chars_title_pattern = re.compile(r"[\(\)\[\]\{\}\|\~\@\^\–\—\*\=\+\_\?\/\\]")
title_chunk_pattern = re.compile(
    r"[,-:;–—_]\s*(?P<chunk>(?:vers?\.?|version|v\.|vol\.?|volume|bk\.|book|part|ch\.|pt\.|chapter|ep\.|episode|series)\s*\d+\W*$)",
    re.I,
)
open_library_user_agent_pattern = re.compile(
    r"^(?P<app>[^/]+)/(?P<version>[0-9.]+)? \((?P<email>[^\)]+)\)$"
)
