#!/usr/bin/env bash
# Import: normalize every SVG in alliconsvg/ (the flat, clean-named source set)
# into tool/svgs/ with picosvg (strokes -> fills, shapes -> paths, clip-paths
# resolved) so the font glyphs render correctly. Filename = icon name.
#
# Workflow: drop a clean single-color SVG into alliconsvg/ (snake_case name),
#           then:  bash tool/import.sh && bash tool/generate.sh
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/alliconsvg"
DST="$ROOT/tool/svgs"
PICO="$ROOT/tool/.venv/bin/picosvg"

[ -x "$PICO" ] || { echo "picosvg venv missing. Run: python3 -m venv tool/.venv && tool/.venv/bin/pip install picosvg"; exit 1; }

mkdir -p "$DST"
rm -f "$DST"/*.svg   # alliconsvg/ is the single source of truth — clear stale/renamed files
ok=0; fail=0
for src in "$SRC"/*.svg; do
  [ -f "$src" ] || continue
  name="$(basename "$src")"
  if "$PICO" "$src" > "$DST/$name" 2>/dev/null; then
    ok=$((ok+1))
  else
    echo "  PICOSVG FAILED: $name (kept raw copy — check it's single-color)"; cp "$src" "$DST/$name"; fail=$((fail+1))
  fi
done
echo "Imported: $ok ok, $fail need attention. -> $DST"
