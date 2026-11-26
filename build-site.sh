#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTDIR="${1:-$ROOT/site}"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Missing pandoc. Install it with: brew install pandoc" >&2
  exit 1
fi

export SPANISH_REFERENCE_BUILT_AT="$(TZ=Europe/Madrid date '+%d.%m.%Y %H:%M:%S %Z')"

VERSION="$(git -C "$ROOT" describe --tags --always 2>/dev/null || echo dev)"
BUILT_DATE="$(TZ=Europe/Madrid date '+%d.%m.%Y')"
rm -rf "$OUTDIR"
mkdir -p "$OUTDIR"
cp "$ROOT/site.css" "$OUTDIR/site.css"
cp "$ROOT/Spanish reference.pdf" "$ROOT/Spanish reference.epub" "$OUTDIR/" 2>/dev/null || true
cp "$ROOT/favicon.svg" "$ROOT/favicon-48.png" "$ROOT/apple-touch-icon.png" "$OUTDIR/"
ES_DIR="$(mktemp -d)"
trap 'rm -rf "$ES_DIR"' EXIT
python3 "$ROOT/scripts/build-site.py" "$OUTDIR" "$VERSION" "$BUILT_DATE" "$ES_DIR"

# Full-text search index (Pagefind). Optional: without it the search box is hidden.
if command -v npx >/dev/null 2>&1; then
  npx --yes pagefind@1.3.0 --site "$OUTDIR" --force-language ru \
    && npx --yes pagefind@1.3.0 --site "$ES_DIR" --output-path "$OUTDIR/pagefind-es" --force-language es \
    || echo "Pagefind failed; the site works without search." >&2
else
  echo "npx not found; skipping the search index." >&2
fi
