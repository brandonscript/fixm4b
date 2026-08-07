from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from tinta import Tinta  # type: ignore[import-untyped]

from fixm4b import __version__
from fixm4b.config import Fixm4bConfig, default_config_path, write_default_config
from fixm4b.errors import ConfigurationError, Fixm4bError
from fixm4b.settings import set_settings

COLORS_FILE = Path(__file__).with_name("colors.ini")
if COLORS_FILE.exists():
    Tinta.load_colors(str(COLORS_FILE))


def _config_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fixm4b config", description="Manage fixm4b configuration")
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("show", help="Show the effective configuration")
    new = sub.add_parser("new", help="Write a default config.toml")
    new.add_argument("--force", action="store_true", help="Overwrite an existing config file")
    return parser


def _run_config(argv: list[str]) -> int:
    args = _config_parser().parse_args(argv)
    if args.action == "show":
        cfg = Fixm4bConfig.load()
        print(json.dumps(cfg.model_dump(mode="json"), indent=2))
        print(f"# path: {default_config_path()}", file=sys.stderr)
        return 0
    if args.action == "new":
        path = write_default_config(force=args.force)
        print(f"Wrote {path}")
        return 0
    return 2


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] in {"-V", "--version"}:
        print(f"fixm4b {__version__}")
        return 0
    if argv and argv[0] == "config":
        try:
            return _run_config(argv[1:])
        except ConfigurationError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1

    # Load XDG / env settings for the planner before CLI runs.
    set_settings(Fixm4bConfig.load().to_settings())
    if "--debug" in argv or "-d" in argv:
        os.environ.setdefault("FIXM4B_DEBUG", "1")

    from fixm4b.cli import main as cli_main

    try:
        return cli_main(argv)
    except ConfigurationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except Fixm4bError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print()
        print(Tinta().light_pink("Meow.").to_str())
        raise SystemExit(130)
