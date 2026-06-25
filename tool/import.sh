#!/usr/bin/env bash
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/iconsvgs"
DST="$ROOT/tool/svgs"
PICO="$ROOT/tool/.venv/bin/picosvg"

[ -x "$PICO" ] || { echo "picosvg venv missing. Run: python3 -m venv tool/.venv && tool/.venv/bin/pip install picosvg"; exit 1; }

mkdir -p "$DST"
rm -f "$DST"/*.svg   # iconsvgs/ is the single source of truth - clear stale/renamed files
ok=0; fail=0
for src in "$SRC"/*.svg; do
  [ -f "$src" ] || continue
  name="$(basename "$src")"
  if "$PICO" "$src" > "$DST/$name" 2>/dev/null; then
    ok=$((ok+1))
  else
    echo "  PICOSVG FAILED: $name (kept raw copy - check it's single-color)"; cp "$src" "$DST/$name"; fail=$((fail+1))
  fi
done
echo "Imported: $ok ok, $fail need attention. -> $DST"
