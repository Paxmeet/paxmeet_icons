# Adding `paxmeet_icons` to a Flutter project

This guide shows how to use the Paxmeet icon set in any Flutter app. You add the
package once, then use icons anywhere with `Icon(PaxmeetIcons.xxx)` — no asset
files, no font declaration in your app.

> Browse all icons and copy their code from the reference page: open
> [`index.html`](../index.html) in a browser (or its hosted GitHub Pages URL).

---

## 1. Add the dependency

Pick **one** of the following based on where the package lives, and add it under
`dependencies:` in your app's `pubspec.yaml`.

### Option A — Same repo / monorepo (local path)
```yaml
dependencies:
  paxmeet_icons:
    path: ../paxmeet_icons        # relative path to the package folder
```

### Option B — Private Git repo (recommended for sharing across apps)
```yaml
dependencies:
  paxmeet_icons:
    git:
      url: https://github.com/<your-org>/paxmeet_icons.git
      ref: main                   # or a tag like v0.0.1 to pin a version
```

### Option C — Published on pub.dev (public package)
```yaml
dependencies:
  paxmeet_icons: ^0.0.1
```

## 2. Install
```bash
flutter pub get
# (this project uses fvm, so: fvm flutter pub get)
```

## 3. Use an icon
```dart
import 'package:paxmeet_icons/paxmeet_icons.dart';

// anywhere a widget is allowed:
Icon(PaxmeetIcons.home);

// with size + color (color comes from Flutter, the font is monochrome):
Icon(PaxmeetIcons.heart, size: 28, color: Theme.of(context).primaryColor);

// in a button:
IconButton(
  icon: const Icon(PaxmeetIcons.search),
  onPressed: () {},
);
```

That's it — the font ships **inside** the package (each `IconData` already carries
`fontPackage: 'paxmeet_icons'`), so you do **not** add anything to the `fonts:`
section of your app's `pubspec.yaml`.

---

## App size — nothing to worry about

The font holds all icons in ~12 KB, and Flutter **tree-shakes** the glyphs you
don't use out of release builds automatically. You'll see this during a release
build:

```
Font asset "PaxmeetIcons.ttf" was tree-shaken, reducing it from 33 to 6 glyphs (82% reduction).
```

⚠️ One rule to keep tree-shaking working: always use the constants directly
(`PaxmeetIcons.home`). Don't build `IconData` from a runtime/variable codepoint —
that disables tree-shaking for the whole font.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Icons show as empty boxes (□) | Run `flutter pub get`; do a full restart (not just hot reload) so the new font loads. |
| `Undefined name 'PaxmeetIcons'` | Add the import: `import 'package:paxmeet_icons/paxmeet_icons.dart';` |
| Git dependency won't resolve | Check the `url`/`ref`; ensure you have access to the repo. |
| Wrong icon shows | Names map to glyphs by codepoint; if you regenerated the font, re-run `flutter pub get` and restart. |
