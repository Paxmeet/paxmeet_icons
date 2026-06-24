# Adding / updating / removing icons (updates app + web together)

You edit **one** folder of SVGs and run **one** command. That regenerates the
font, the Flutter class, **and** the web assets — so the app and website always
get the same icons. The single source of truth is
[`alliconsvg/`](../alliconsvg/) — a flat folder where **the filename is the icon
name**.

```
alliconsvg/home.svg        ─┐                    ┌─▶ lib/paxmeet_icons.dart   (Flutter: PaxmeetIcons.home)
alliconsvg/heart.svg        ├─ tool/build.sh ─▶ ├─▶ web/paxmeet-icons.css     (Web: <PaxmeetIcon name="home"/>)
alliconsvg/search.svg      ─┘   (one font)        └─▶ index.html, preview.png  (reference)
```

---

## One-time setup (first time on a machine)

```bash
cd paxmeet_icons

# Python tools: picosvg (stroke→fill normalization) + markdown (for the PDF)
python3 -m venv tool/.venv
tool/.venv/bin/pip install picosvg markdown

# Dart tool: the font generator
dart pub global activate icon_font_generator
```

---

## Add a new icon

1. **Prepare the SVG**
   - **Single color** (monochrome) — the color is applied later (`Icon(color:)`
     in Flutter, `color` in CSS). Multi-color/brand icons can't be a font glyph.
   - Fill-based **or** stroke-based both work — strokes are auto-converted to
     filled outlines by picosvg.
   - Recommended: `24×24` viewBox, no embedded raster images.

2. **Name it well** and drop it into `alliconsvg/`
   - Use **snake_case**; it becomes a **camelCase** name on both platforms:
     - `event_ticket.svg` → Flutter `PaxmeetIcons.eventTicket` / Web `name="eventTicket"`
   - Name by **what the icon depicts** or its UI meaning — `wallet` not
     `empty_wallet`, `message` not `message_text`, `microphone` not `microphone_2`.

3. **Build everything (one command)**
   ```bash
   bash tool/build.sh
   ```
   This updates the font, Flutter class, web CSS/component, and the reference page.

4. **Commit & push** so apps and sites can pull it
   ```bash
   git add -A && git commit -m "icons: add eventTicket" && git push
   ```

5. **Pick it up in each project**
   - **Flutter app:** `flutter pub get` (or `fvm flutter pub get`) + full restart.
   - **Website:** re-copy `web/*` into the site
     (`cp paxmeet_icons/web/* <site>/src/components/paxmeet-icons/`).

---

## Rename an icon
1. Rename the file in `alliconsvg/` (e.g. `empty_wallet.svg` → `wallet.svg`).
2. `bash tool/build.sh` (the build clears stale names automatically).
3. Update usages: Flutter `PaxmeetIcons.emptyWallet` → `PaxmeetIcons.wallet`;
   Web `name="emptyWallet"` → `name="wallet"`.
4. Commit, push, update each project.

## Remove an icon
1. Delete the file from `alliconsvg/`.
2. `bash tool/build.sh`, commit, push.

---

## What each file/script is

| File / folder | Role |
|---|---|
| `alliconsvg/` | **Source of truth** — flat, clean-named SVGs you edit. |
| `tool/build.sh` | **The one command** — runs the whole pipeline below. |
| `tool/import.sh` | Normalizes SVGs with picosvg → `tool/svgs/` (clears old files). |
| `tool/generate.sh` | `icon_font_generator`: `tool/svgs/` → `.ttf` + `lib/paxmeet_icons.dart`. |
| `tool/build_web_assets.py` | Generates `web/` CSS + React component from the font. |
| `tool/build_web.py` | Generates the `index.html` reference page. |
| `tool/preview.py` | Generates `preview.png`. |
| `fonts/PaxmeetIcons.ttf` | The generated font — used by **both** app and web (committed). |
| `lib/paxmeet_icons.dart`, `web/*` | Generated outputs (committed). |

---

## Gotchas

- **Empty / wrong glyph** → the SVG was multi-color or had an embedded image.
  Flatten it to a single-color vector and rebuild.
- **`import.sh` prints "PICOSVG FAILED"** for a file → picosvg can't resolve it
  (multi-color/raster). Simplify and re-export.
- Always commit the regenerated `fonts/`, `lib/paxmeet_icons.dart`, and `web/`
  together with the SVG change, so app and web stay in sync.
- After updating, **restart** the Flutter app fully (not just hot reload) and
  re-copy `web/*` into the website.
