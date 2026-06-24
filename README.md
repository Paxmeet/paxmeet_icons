# paxmeet_icons

Paxmeet's custom icon set, shipped as a single icon font — the same approach as
[`font_awesome_flutter`](https://pub.dev/packages/font_awesome_flutter).

![icon preview](preview.png)

33 icons, ~12.6 KB font (tree-shaken further per app). Regenerate `preview.png`
with `tool/.venv/bin/python tool/preview.py` after adding icons.

## 📖 Guides

- **[docs/INSTALL.md](docs/INSTALL.md)** — add this library to a Flutter project and use icons.
- **[docs/ADDING_ICONS.md](docs/ADDING_ICONS.md)** — add, rename, or remove icons.

- **One `.ttf`** holds every icon (not hundreds of asset files).
- Icons are `const IconData`, so Flutter **tree-shakes unused glyphs** in release
  builds — your app ships only the icons it actually references (a few KB).
- The same `.ttf` also works on a **website** (`@font-face` + CSS).

## Add / update icons

1. Put single-color SVGs in `tool/svgs/` (filename = icon name, snake_case →
   camelCase identifier, e.g. `add_circle.svg` → `PaxmeetIcons.addCircle`).
   Stroke-based ("linear"/"outline") icons are fine — `generate.sh` runs
   **picosvg** to convert strokes to filled outlines automatically.
   Multi-color icons can't be a single font glyph — keep those as SVGs.
2. Regenerate:
   ```bash
   bash tool/generate.sh
   ```
   This normalizes the SVGs, then rewrites `fonts/PaxmeetIcons.ttf` and
   `lib/paxmeet_icons.dart`.

> First-time setup of the normalizer (one-time):
> ```bash
> python3 -m venv tool/.venv && tool/.venv/bin/pip install picosvg
> ```

### Source SVGs

`alliconsvg/` holds the raw source set as a **flat folder** of clean
snake_case-named SVGs (filename = icon name). Drop a new single-color SVG in,
then run:

```bash
bash tool/import.sh    # picosvg-normalize alliconsvg/ -> tool/svgs/
bash tool/generate.sh  # build font + Dart class
```

## Use it in a Flutter app

In the app's `pubspec.yaml`, depend on this package (see distribution options below), then:

```dart
import 'package:paxmeet_icons/paxmeet_icons.dart';

Icon(PaxmeetIcons.home, size: 24, color: Colors.purple);
```

No font declaration needed in the **app** — the font ships with this package
(`fontPackage: 'paxmeet_icons'` is baked into each `IconData`).

> Build release with tree-shaking (default): `flutter build apk` →
> "Font asset PaxmeetIcons.ttf was tree-shaken ...".
> Don't construct `IconData` from a variable codepoint, or tree-shaking is disabled.

## Icon reference webpage

`index.html` is a **self-contained** gallery of every icon with its name and
Flutter code (font embedded as base64 — no assets, no server needed):

- **View locally:** open `index.html` in any browser.
- **Search** by name; **click** an icon to copy its `PaxmeetIcons.xxx` code.
- **Publish (GitHub Pages):** push this repo → Settings → Pages → deploy from
  the repo root; the page is then public at `https://<you>.github.io/paxmeet_icons/`.
- **Regenerate** after adding icons:
  ```bash
  tool/.venv/bin/python tool/build_web.py
  ```

## Distribution options (how the app gets this package)

1. **Local path** (simplest while iterating in this monorepo):
   ```yaml
   dependencies:
     paxmeet_icons:
       path: ../paxmeet_icons
   ```
2. **Git dependency** (private, no pub.dev account needed):
   ```yaml
   dependencies:
     paxmeet_icons:
       git:
         url: https://github.com/paxmeet/paxmeet_icons.git
         ref: main   # or a tag like v0.0.1
   ```
3. **pub.dev** (public package): set a real `version`, remove `publish_to: none`
   from `pubspec.yaml`, then `dart pub publish`.
