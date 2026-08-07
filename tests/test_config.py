from __future__ import annotations

from pathlib import Path

from fixm4b.config import Fixm4bConfig, default_config_path, write_default_config
from fixm4b.errors import ConfigurationError
from fixm4b.settings import Fixm4bSettings, get_settings, set_settings


def test_default_config_path_uses_xdg(monkeypatch, tmp_path: Path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    assert default_config_path() == tmp_path / "fixm4b" / "config.toml"


def test_write_and_load_config(tmp_path: Path, monkeypatch):
    monkeypatch.delenv("CLEANUP_FILENAMES", raising=False)
    monkeypatch.delenv("BOOKPEEK", raising=False)
    monkeypatch.delenv("GOODSCRAPS_USER_AGENT", raising=False)
    monkeypatch.delenv("OPEN_LIBRARY_USER_AGENT", raising=False)
    path = tmp_path / "config.toml"
    write_default_config(path)
    cfg = Fixm4bConfig.load(path)
    assert cfg.cleanup_filenames is False
    assert cfg.goodscraps_timeout == 30.0
    settings = cfg.to_settings()
    assert isinstance(settings, Fixm4bSettings)


def test_write_default_config_refuses_overwrite(tmp_path: Path):
    path = tmp_path / "config.toml"
    write_default_config(path)
    try:
        write_default_config(path)
        assert False, "expected ConfigurationError"
    except ConfigurationError:
        pass
    write_default_config(path, force=True)


def test_set_settings_injection():
    set_settings(Fixm4bSettings(cleanup_filenames=True, bookpeek=True))
    try:
        s = get_settings()
        assert s.cleanup_filenames is True
        assert s.bookpeek is True
    finally:
        set_settings(None)
