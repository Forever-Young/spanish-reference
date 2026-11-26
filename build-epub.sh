#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT="${1:-$ROOT/reference.md}"
OUTPUT="${2:-$ROOT/Spanish reference.epub}"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Missing pandoc. Install it with: brew install pandoc" >&2
  exit 1
fi

export SPANISH_REFERENCE_BUILT_AT="$(TZ=Europe/Madrid date '+%d.%m.%Y %H:%M:%S %Z')"

mkdir -p "$(dirname "$OUTPUT")"
pandoc "$INPUT" --from=markdown --lua-filter="$ROOT/build-timestamp.lua" --lua-filter="$ROOT/epub-filter.lua" --to=epub3 \
  --metadata title="Справочник по испанскому языку: грамматика и живая речь" --metadata lang=ru \
  --toc --toc-depth=2 --split-level=2 --css="$ROOT/epub.css" --output="$OUTPUT"
echo "Created $OUTPUT"
