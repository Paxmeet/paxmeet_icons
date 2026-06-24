# Adding / updating / removing icons

The package turns a folder of SVGs into one icon font. The **single source of
truth** is the [`alliconsvg/`](../alliconsvg/) folder — a flat folder where the
**filename is the icon name**. You edit that folder, run the build, and the font,
the Dart class, and the reference webpage all regenerate.

```
alliconsvg/home.svg   ─┐
alliconsvg/heart.svg   ├─ build ─▶  fonts/PaxmeetIcons.ttf
alliconsvg/search.svg ─┘            lib/paxmeet_icons.dart  →  PaxmeetIcons.home …
                                    index.html (reference page)
```

---

## One-time setup (first time on a machine)

The build uses **picosvg** (converts strokes→fills) and **icon_font_generator**.

```bash
cd paxmeet_icons

# 1. picosvg (Python) — for stroke/shape normalization
python3 -m venv tool/.venv
tool/.venv/bin/pip install picosvg

# 2. icon_font_generator (Dart) — builds the font
dart pub global activate icon_font_generator
```

---

## Add a new icon

1. **Prepare the SVG.** It must be:
   - **Single color** (monochrome). The color is applied later in Flutter via
     `Icon(color:)`. Multi-color/brand icons cannot be a font glyph.
   - Either fill-based **or** stroke-based — both are fine, picosvg converts
     strokes to filled outlines automatically.
   - Recommended canvas: `24×24` viewBox, no embedded raster images.

2. **Name it well** and drop it in `alliconsvg/`:
   - Use **snake_case**; the filename becomes a **camelCase** Dart identifier.
     - `add_circle.svg`   → `PaxmeetIcons.addCircle`
     - `event_ticket.svg` → `PaxmeetIcons.eventTicket`
   - Name by **what the icon depicts** or its **UI meaning**, not the design-tool
     export name: `wallet` not `empty_wallet`, `message` not `message_text`,
     `microphone` not `microphone_2`.

3. **Build:**
   ```bash
   bash tool/import.sh        # normalize alliconsvg/ -> tool/svgs/ (picosvg)
   bash tool/generate.sh      # build the .ttf + lib/paxmeet_icons.dart
   tool/.venv/bin/python tool/build_web.py   # refresh index.html reference page
   ```

4. **Use it:** `Icon(PaxmeetIcons.eventTicket)`. In an app already depending on
   the package, run `flutter pub get` + full restart to pick up the new font.

> Tip: there's no need to remember the three commands separately — they always
> run together. See **One-command build** below.

---

## Rename an icon

1. Rename the file in `alliconsvg/` (e.g. `empty_wallet.svg` → `wallet.svg`).
2. Re-run the build (`import.sh` clears stale files, so the old name disappears).
3. Update any usages in apps from `PaxmeetIcons.emptyWallet` → `PaxmeetIcons.wallet`.

## Remove an icon

1. Delete the file from `alliconsvg/`.
2. Re-run the build. The glyph and its constant are gone.

---

## One-command build (optional convenience)

Run all three steps at once:

```bash
bash tool/import.sh && bash tool/generate.sh && tool/.venv/bin/python tool/build_web.py
```

---

## How it works (reference)

| Folder / file | Role |
|---|---|
| `alliconsvg/` | **Source of truth** — flat, clean-named SVGs you edit. |
| `tool/import.sh` | Normalizes each SVG with picosvg into `tool/svgs/` (clears old files first). |
| `tool/svgs/` | Generated, normalized SVGs — the actual font input. Don't hand-edit. |
| `tool/generate.sh` | Runs `icon_font_generator`: `tool/svgs/` → `.ttf` + Dart class. |
| `tool/build_web.py` | Builds the self-contained `index.html` reference page. |
| `fonts/PaxmeetIcons.ttf` | The generated font (committed). |
| `lib/paxmeet_icons.dart` | The generated `PaxmeetIcons` class (committed). |

---

## Gotchas

- **Empty or wrong-looking glyph?** The SVG was probably multi-color or had an
  embedded image. Make it a single-color vector and rebuild.
- **`import.sh` says "PICOSVG FAILED"** for a file → that SVG has something
  picosvg can't resolve (e.g. multi-color, raster). Simplify/flatten it in the
  design tool and re-export.
- **Name collisions:** two files can't share a name. Filenames are unique by
  definition, so just pick distinct, descriptive names.
- Always commit the regenerated `fonts/PaxmeetIcons.ttf` and
  `lib/paxmeet_icons.dart` together with the SVG change.
