#!/usr/bin/env bash
# Build EVERYTHING from the SVGs in alliconsvg/ — runs the full pipeline so the
# Flutter app, the website assets, and the reference page all stay in sync.
#
# Usage:  bash tool/build.sh   (run from the package root)
set -euo pipefail
cd "$(dirname "$0")/.."

PY="tool/.venv/bin/python"
[ -x "$PY" ] || { echo "Setup needed: python3 -m venv tool/.venv && tool/.venv/bin/pip install picosvg markdown"; exit 1; }

echo "▶ 1/4  Normalizing SVGs (picosvg) …"
bash tool/import.sh

echo "▶ 2/4  Building font + Flutter class …"
bash tool/generate.sh >/dev/null

echo "▶ 3/4  Building web assets (CSS + React component) …"
"$PY" tool/build_web_assets.py

echo "▶ 4/4  Building reference page + preview …"
"$PY" tool/build_web.py
"$PY" tool/preview.py

echo ""
echo "✓ Done. Updated:"
echo "    fonts/PaxmeetIcons.ttf        (the font — used by app AND web)"
echo "    lib/paxmeet_icons.dart        (Flutter:  PaxmeetIcons.xxx)"
echo "    web/paxmeet-icons.css + .jsx  (Web:      <PaxmeetIcon name=\"xxx\"/>)"
echo "    index.html, preview.png       (reference)"
echo ""
echo "Next: commit & push so apps/sites can pull the update:"
echo "    git add -A && git commit -m \"icons: <what changed>\" && git push"
