"""Injectable runtime settings for the metadata planner / CLI."""

from __future__ import annotations

import os
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Fixm4bSettings:
    cleanup_filenames: bool = False
    goodscraps_user_agent: str | None = None
    goodscraps_timeout: float = 30.0
    open_library_user_agent: str | None = None
    open_library_timeout: float = 15.0
    bookpeek: bool = False
    cache_dir: Path | None = None
    inbox_folder: str = ""
    converted_folder: str = ""
    archive_folder: str = ""
    minimalist: bool | None = None
    app_name_path: Path | None = None

    def with_overrides(self, **kwargs: Any) -> Fixm4bSettings:
        return replace(self, **kwargs)


_settings: Fixm4bSettings | None = None


def get_settings() -> Fixm4bSettings:
    if _settings is not None:
        return _settings
    # Prefer XDG config when present; else env / defaults.
    try:
        from fixm4b.config import Fixm4bConfig

        return Fixm4bConfig.load().to_settings()
    except Exception:
        return Fixm4bSettings(
            goodscraps_user_agent=os.environ.get("GOODSCRAPS_USER_AGENT") or None,
            open_library_user_agent=os.environ.get("OPEN_LIBRARY_USER_AGENT") or None,
            cleanup_filenames=os.environ.get("CLEANUP_FILENAMES", "").lower() in {"1", "true", "y", "yes"},
            bookpeek=os.environ.get("BOOKPEEK", "").lower() in {"1", "true", "y", "yes"},
            inbox_folder=os.environ.get("CLI_INBOX_FOLDER", "") or "",
            converted_folder=os.environ.get("CLI_CONVERTED_FOLDER", "") or "",
            archive_folder=os.environ.get("CLI_ARCHIVE_FOLDER", "") or "",
        )


def set_settings(settings: Fixm4bSettings | None) -> None:
    global _settings
    _settings = settings


def settings_from_cfg(cfg: Any) -> Fixm4bSettings:
    """Adapt an auto-m4b-like ``cfg`` object (used by auto-m4b shims)."""
    meta_dir = getattr(cfg, "META_DIR", None)
    cache_dir = Path(meta_dir) if meta_dir is not None else None
    app_name = (cache_dir / "app_name") if cache_dir is not None else None
    return Fixm4bSettings(
        cleanup_filenames=bool(getattr(cfg, "CLEANUP_FILENAMES", False)),
        goodscraps_user_agent=(getattr(cfg, "GOODSCRAPS_USER_AGENT", None) or None) or None,
        goodscraps_timeout=float(getattr(cfg, "GOODSCRAPS_TIMEOUT", 30) or 30),
        open_library_user_agent=(getattr(cfg, "OPEN_LIBRARY_USER_AGENT", None) or None) or None,
        open_library_timeout=float(getattr(cfg, "OPEN_LIBRARY_TIMEOUT", 15) or 15),
        bookpeek=bool(getattr(cfg, "BOOKPEEK", False)),
        cache_dir=cache_dir,
        inbox_folder=os.environ.get("CLI_INBOX_FOLDER", "") or "",
        converted_folder=os.environ.get("CLI_CONVERTED_FOLDER", "") or "",
        archive_folder=os.environ.get("CLI_ARCHIVE_FOLDER", "") or "",
        minimalist=None,
        app_name_path=app_name,
    )
