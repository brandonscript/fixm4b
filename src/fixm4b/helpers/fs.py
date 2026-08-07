"""Filename / path helpers."""

from __future__ import annotations

from pathlib import Path

AUDIO_EXTS = [".mp3", ".m4a", ".m4b", ".aac", ".wma"]

_UNSAFE_FILENAME_CHARS: dict[str, str] = {
    ":": " - ",
    "/": "-",
    "\\": "-",
    "*": "",
    "?": "",
    '"': "'",
    "<": "",
    ">": "",
    "|": "-",
}


def ensure_dot(s: str) -> str:
    s = (s or "").strip()
    return s if s.startswith(".") else f".{s}"


def safe_filename(name: str) -> str:
    for bad, good in _UNSAFE_FILENAME_CHARS.items():
        name = name.replace(bad, good)
    return " ".join(name.split())


def ensure_audio_ext(name: str, ext: str = ".m4b") -> str:
    safe = safe_filename(name)
    lower = safe.lower()
    target = ensure_dot(ext).lower()
    for audio_ext in AUDIO_EXTS:
        if lower.endswith(audio_ext):
            return safe[: -len(audio_ext)] + ensure_dot(ext)
    if lower.endswith(target):
        return safe
    return safe + ensure_dot(ext)


def try_relative_to(p: str | Path, root: str | Path) -> Path | None:
    try:
        return Path(p).relative_to(Path(root))
    except ValueError:
        return None
