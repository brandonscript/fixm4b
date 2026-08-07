"""XDG user configuration for fixm4b."""

from __future__ import annotations

import os
import tomllib
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from .errors import ConfigurationError
from .settings import Fixm4bSettings


class Fixm4bConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    cleanup_filenames: bool = False
    bookpeek: bool = False
    goodscraps_user_agent: str | None = None
    goodscraps_timeout: float = Field(default=30.0, gt=0)
    open_library_user_agent: str | None = None
    open_library_timeout: float = Field(default=15.0, gt=0)
    inbox_folder: str = ""
    converted_folder: str = ""
    archive_folder: str = ""
    minimalist: bool | None = None

    @classmethod
    def load(cls, path: Path | None = None) -> Fixm4bConfig:
        config_path = path or default_config_path()
        if not config_path.exists():
            return cls(
                goodscraps_user_agent=os.environ.get("GOODSCRAPS_USER_AGENT") or None,
                open_library_user_agent=os.environ.get("OPEN_LIBRARY_USER_AGENT") or None,
                cleanup_filenames=os.environ.get("CLEANUP_FILENAMES", "").lower()
                in {"1", "true", "y", "yes"},
                bookpeek=os.environ.get("BOOKPEEK", "").lower() in {"1", "true", "y", "yes"},
                inbox_folder=os.environ.get("CLI_INBOX_FOLDER", "") or "",
                converted_folder=os.environ.get("CLI_CONVERTED_FOLDER", "") or "",
                archive_folder=os.environ.get("CLI_ARCHIVE_FOLDER", "") or "",
            )
        with config_path.open("rb") as config_file:
            data = tomllib.load(config_file)
        cfg = cls.model_validate(data)
        return cfg.model_copy(
            update={
                "goodscraps_user_agent": os.environ.get("GOODSCRAPS_USER_AGENT")
                or cfg.goodscraps_user_agent,
                "open_library_user_agent": os.environ.get("OPEN_LIBRARY_USER_AGENT")
                or cfg.open_library_user_agent,
                "cleanup_filenames": (
                    os.environ["CLEANUP_FILENAMES"].lower() in {"1", "true", "y", "yes"}
                    if "CLEANUP_FILENAMES" in os.environ
                    else cfg.cleanup_filenames
                ),
                "bookpeek": (
                    os.environ["BOOKPEEK"].lower() in {"1", "true", "y", "yes"}
                    if "BOOKPEEK" in os.environ
                    else cfg.bookpeek
                ),
                "inbox_folder": os.environ.get("CLI_INBOX_FOLDER") or cfg.inbox_folder,
                "converted_folder": os.environ.get("CLI_CONVERTED_FOLDER") or cfg.converted_folder,
                "archive_folder": os.environ.get("CLI_ARCHIVE_FOLDER") or cfg.archive_folder,
            }
        )

    def to_settings(self) -> Fixm4bSettings:
        cache_root = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "fixm4b"
        return Fixm4bSettings(
            cleanup_filenames=self.cleanup_filenames,
            goodscraps_user_agent=self.goodscraps_user_agent,
            goodscraps_timeout=self.goodscraps_timeout,
            open_library_user_agent=self.open_library_user_agent,
            open_library_timeout=self.open_library_timeout,
            bookpeek=self.bookpeek,
            cache_dir=cache_root,
            inbox_folder=self.inbox_folder,
            converted_folder=self.converted_folder,
            archive_folder=self.archive_folder,
            minimalist=self.minimalist,
            app_name_path=cache_root / "app_name",
        )


def write_default_config(path: Path | None = None, *, force: bool = False) -> Path:
    config_path = path or default_config_path()
    if config_path.exists() and not force:
        raise ConfigurationError(
            f"Configuration already exists: {config_path}; use --force to replace it"
        )
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        """# fixm4b configuration
cleanup_filenames = false
bookpeek = false
goodscraps_timeout = 30.0
open_library_timeout = 15.0
# goodscraps_user_agent = "MyApp/1.0 (me@example.com)"
# open_library_user_agent = "MyApp/1.0 (me@example.com)"
# inbox_folder = "/path/to/inbox"
# converted_folder = "/path/to/converted"
# archive_folder = "/path/to/archive"
# minimalist = true
""",
        encoding="utf-8",
    )
    return config_path


def default_config_path() -> Path:
    root = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return root / "fixm4b" / "config.toml"
