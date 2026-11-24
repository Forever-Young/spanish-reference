#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT="${1:-$ROOT/reference.md}"
OUTPUT="${2:-$ROOT/Spanish reference.pdf}"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Missing pandoc. Install it with: brew install pandoc" >&2
  exit 1
fi
if ! command -v weasyprint >/dev/null 2>&1; then
  echo "Missing WeasyPrint. See README.md for installation instructions." >&2
  exit 1
fi

mkdir -p "$(dirname "$OUTPUT")"
TEMP_HTML="$(mktemp "${TMPDIR:-/tmp}/spanish-reference.XXXXXX.html")"
trap 'rm -f "$TEMP_HTML"' EXIT

export SPANISH_REFERENCE_BUILT_AT="$(TZ=Europe/Madrid date '+%d.%m.%Y %H:%M:%S %Z')"

pandoc "$INPUT" --from=markdown --lua-filter="$ROOT/build-timestamp.lua" --lua-filter="$ROOT/build-toc.lua" --to=html5 --standalone --metadata title="" --css="$ROOT/reference.css" --output="$TEMP_HTML"
weasyprint "$TEMP_HTML" "$OUTPUT"
echo "Created $OUTPUT"
