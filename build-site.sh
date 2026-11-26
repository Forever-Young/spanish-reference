#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTDIR="${1:-$ROOT/site}"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Missing pandoc. Install it with: brew install pandoc" >&2
  exit 1
fi

export SPANISH_REFERENCE_BUILT_AT="$(TZ=Europe/Madrid date '+%d.%m.%Y %H:%M:%S %Z')"

rm -rf "$OUTDIR"
mkdir -p "$OUTDIR"
cp "$ROOT/site.css" "$OUTDIR/site.css"
cp "$ROOT/Spanish reference.pdf" "$ROOT/Spanish reference.epub" "$OUTDIR/" 2>/dev/null || true
pandoc "$ROOT/reference.md" --from=markdown --lua-filter="$ROOT/build-timestamp.lua" --to=html5 --standalone \
  --metadata pagetitle="Справочник грамматики испанского языка" --metadata lang=ru \
  --toc --toc-depth=2 --css=site.css --include-before-body="$ROOT/site-header.html" \
  --output="$OUTDIR/index.html"
echo "Created $OUTDIR/index.html"
