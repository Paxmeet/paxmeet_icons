# Using paxmeet_icons (Flutter app + Web)

One icon set, defined once, used the same way everywhere. The names are
**identical** across platforms, so designers and developers refer to the same
list (open `index.html` to browse & search every icon).

| Platform | How you use an icon |
|---|---|
| **Flutter** | `Icon(PaxmeetIcons.home)` |
| **Web (React/Next.js)** | `<PaxmeetIcon name="home" />` or `<i className="pmi pmi-home" />` |

Both render from the **same font file** (`fonts/PaxmeetIcons.ttf`), so an icon can
never look different between the app and the website.

---

## A) Flutter app

### 1. Add the dependency
In your app's `pubspec.yaml` under `dependencies:` — pick one:

```yaml
# Git (recommended — works in any project)
paxmeet_icons:
  git:
    url: https://github.com/letssuhail/paxmeet_icons.git
    ref: main          # or a tag like v0.0.1 to pin a version

# …or local path (same repo / monorepo)
# paxmeet_icons:
#   path: ../paxmeet_icons
```

### 2. Install
```bash
flutter pub get        # this repo uses fvm:  fvm flutter pub get
```

### 3. Use
```dart
import 'package:paxmeet_icons/paxmeet_icons.dart';

Icon(PaxmeetIcons.home);
Icon(PaxmeetIcons.heart, size: 28, color: Theme.of(context).primaryColor);

IconButton(
  icon: const Icon(PaxmeetIcons.search),
  onPressed: () {},
);
```

That's it — no font setup in your app's `pubspec.yaml`; the font ships inside the
package. The color comes from Flutter (`color:`), the font is monochrome.

> **App size:** all icons are ~12 KB and Flutter **tree-shakes** the ones you don't
> use out of release builds automatically. Just always use the constants directly
> (`PaxmeetIcons.home`) — never build `IconData` from a variable codepoint, or
> tree-shaking turns off.

---

## B) Web (Next.js / React)

Install straight from GitHub — just like the Flutter dependency, no manual file
copying. The consumer needs **read-access to the (private) repo** (their git/npm
must be authenticated to GitHub).

### 1. Install from GitHub
```bash
npm install github:letssuhail/paxmeet_icons
```

### 2. Let Next.js transpile the package — in `next.config.mjs`
```js
const nextConfig = {
  transpilePackages: ['paxmeet_icons'],
};
```

### 3. Load the CSS once (App Router → `src/app/layout.js`)
```js
import "./globals.css";
import "paxmeet_icons/css";
```

### 4. Use it
```jsx
import { PaxmeetIcon } from "paxmeet_icons";

<PaxmeetIcon name="search" size={20} color="#7332D6" />
```
Or with plain CSS classes (no component):
```jsx
<i className="pmi pmi-search" style={{ fontSize: 20, color: "#7332D6" }} />
```

`paxmeet_icons/names` exports `paxmeetIconNames` — the full list, handy for dropdowns.

**Updating later:** `npm update paxmeet_icons` (or reinstall) pulls the latest from `main`.

> **TypeScript site?** Props are `{ name: string; size?: number; color?: string; className?: string }`.

> **No GitHub access / prefer not to install?** You can instead copy the package's
> `web/` folder into your project (`cp -r paxmeet_icons/web/* src/components/paxmeet-icons/`)
> and import from that local path. The git-install above is the cleaner option.

---

## Finding icon names

- Open **`index.html`** (repo root) in a browser — search any icon, click to copy
  its name / Flutter code. Host it on GitHub Pages to share a public reference.
- Names are camelCase and the same on both platforms: `addCircle`, `wallet`,
  `volume`, `profileCircle`, `chevronLeft`, …

See **[ADDING_ICONS.md](ADDING_ICONS.md)** to add or change icons.
