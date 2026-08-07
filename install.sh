#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="${HOME}/.local/bin"
COMMAND="${BIN_DIR}/fixm4b"

if ! command -v poetry >/dev/null 2>&1; then
    echo "Error: Poetry is required to install fixm4b." >&2
    exit 1
fi

cd "${SCRIPT_DIR}"
poetry install

mkdir -p "${BIN_DIR}"
ln -sfn "${SCRIPT_DIR}/.venv/bin/fixm4b" "${COMMAND}"

echo "Installed fixm4b at ${COMMAND}"
if [[ ":${PATH}:" != *":${BIN_DIR}:"* ]]; then
    echo "Add ${BIN_DIR} to PATH to run 'fixm4b' directly."
fi
