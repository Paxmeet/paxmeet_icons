# paxmeet_icons

Paxmeet's custom icon set, shipped as a single icon font and used the same way on
Flutter and the web. One source of icons, identical names everywhere.

![icon preview](preview.png)

**542 icons** in one font (~170 KB). Browse and copy code from the live reference:

> **Reference page:** https://letssuhail.github.io/paxmeet_icons/

Search any icon, click it to copy the exact Flutter / React / HTML code.

## Why a font (not asset files)

- One small file holds every icon, instead of hundreds of SVG/PNG assets.
- Scalable and colorable like text (`color`, `size`).
- Flutter tree-shakes the glyphs you don't use out of release builds.
- The same font works on Flutter and on any website.

## Usage

| Platform | Code |
|---|---|
| Flutter | `Icon(PaxmeetIcons.addCircle)` |
| Web (React / Next.js) | `<PaxmeetIcon name="addCircle" />` |
| Web (CSS class) | `<i class="pmi pmi-addCircle"></i>` |

The icon color is whatever you set (`color:` in Flutter, `color` in CSS). The font
itself is monochrome - it has no built-in color.

Full setup for both platforms: **[docs/USAGE.md](docs/USAGE.md)**.

### Flutter (quick start)
```yaml
# pubspec.yaml
dependencies:
  paxmeet_icons:
    git:
      url: https://github.com/letssuhail/paxmeet_icons.git
      ref: main
```
```dart
import 'package:paxmeet_icons/paxmeet_icons.dart';
Icon(PaxmeetIcons.home, size: 24, color: Color(0xFF7332D6));
```

### Web (quick start)
```bash
npm install github:letssuhail/paxmeet_icons
```
```js
// next.config.mjs -> transpilePackages: ['paxmeet_icons']
// app/layout.js
import "paxmeet_icons/css";
```
```jsx
import { PaxmeetIcon } from "paxmeet_icons";
<PaxmeetIcon name="home" size={24} color="#7332D6" />
```

## Adding or changing icons

Drop a single-color SVG into [`iconsvgs/`](iconsvgs/) (filename = icon name), then:

```bash
bash tool/build.sh
```

This rebuilds the font, the Flutter class, the web assets, and the reference page
in one step. Details: **[docs/ADDING_ICONS.md](docs/ADDING_ICONS.md)**.

## Repo structure

```
iconsvgs/                source SVGs (one per icon, the single source of truth)
fonts/PaxmeetIcons.ttf   generated font (used by app and web)
lib/paxmeet_icons.dart   generated Flutter class
web/                     generated web assets (CSS + React component)
index.html               self-contained reference page
docs/                    USAGE and ADDING_ICONS guides
tool/                    build scripts
```

## Documentation

- [docs/USAGE.md](docs/USAGE.md) - use the icons in Flutter and on the web
- [docs/ADDING_ICONS.md](docs/ADDING_ICONS.md) - add, rename, or remove icons
- [web/README.md](web/README.md) - web quick reference

## Credits

Icon artwork is based on the open-source [Iconsax / vuesax](https://iconsax.io)
set (MIT). This repository packages them as a font for Paxmeet's app and website.
