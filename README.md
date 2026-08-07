# fixm4b

Retag converted audiobooks (ID3 tags, filenames, companion `.txt`) without re-encoding.
Uses Open Library and optional Goodreads (`goodscraps`) / bookpeek.

## Install

```bash
pip install fixm4b
# or
brew install brandonscript/tap/fixm4b
# or from this checkout
./install.sh
```

```bash
fixm4b --help
fixm4b config new
fixm4b config show
```

## Configuration

Default path: `~/.config/fixm4b/config.toml` (or `$XDG_CONFIG_HOME/fixm4b/config.toml`).

Precedence: CLI flags > environment variables > `config.toml` > built-in defaults.

Useful env vars: `OPEN_LIBRARY_USER_AGENT`, `GOODSCRAPS_USER_AGENT`, `BOOKPEEK`,
`CLEANUP_FILENAMES`, `CLI_CONVERTED_FOLDER`, `CLI_ARCHIVE_FOLDER`, `CLI_INBOX_FOLDER`.

## Development

```bash
poetry install
poetry run pytest
poetry run fixm4b --help
```

## License

MIT
