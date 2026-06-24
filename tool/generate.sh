#!/usr/bin/env bash
# Regenerate the PaxmeetIcons font + Dart class from tool/svgs/*.svg
# Usage:  bash tool/generate.sh   (run from the package root)
set -euo pipefail

# Normalize every SVG in tool/svgs/ with picosvg (strokes->fills, shapes->paths,
# clip-paths resolved) so glyphs render correctly. Idempotent — safe to re-run.
PICO="$(cd "$(dirname "$0")/.." && pwd)/tool/.venv/bin/picosvg"
if [ -x "$PICO" ]; then
  for svg in tool/svgs/*.svg; do
    [ -f "$svg" ] || continue
    if out="$("$PICO" "$svg" 2>/dev/null)"; then printf '%s' "$out" > "$svg"; fi
  done
  echo "✓ Normalized SVGs with picosvg"
fi

# Install the generator once (no-op if already activated):
dart pub global activate icon_font_generator >/dev/null 2>&1 || true

GEN="$(dart pub global list >/dev/null 2>&1; echo "$HOME/.pub-cache/bin/generator")"

"$GEN" tool/svgs fonts/PaxmeetIcons.ttf \
  --output-class-file=lib/paxmeet_icons.dart \
  --class-name=PaxmeetIcons \
  --font-name=PaxmeetIcons \
  --package=paxmeet_icons \
  --recursive

echo "✓ Regenerated fonts/PaxmeetIcons.ttf and lib/paxmeet_icons.dart"
echo "  Icon name = svg filename. Add/rename SVGs in tool/svgs/ then re-run this."
