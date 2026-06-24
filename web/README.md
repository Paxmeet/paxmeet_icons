# Using paxmeet_icons on the web (Next.js / React)

The same icon font that powers the Flutter app also works on the web. Icon names
are **identical** to Flutter, so the team uses one convention everywhere:

| Flutter | Web |
|---|---|
| `Icon(PaxmeetIcons.addCircle)` | `<PaxmeetIcon name="addCircle" />` or `<i class="pmi pmi-addCircle" />` |

> Browse/search all icons and copy names from `index.html` (the reference page in
> the repo root) — open it in a browser or its hosted GitHub Pages URL.

## Files in this folder

| File | What it is |
|---|---|
| `paxmeet-icons.css` | Self-contained: `@font-face` (font embedded as base64) + a `.pmi-<name>` class per icon. No font file to host. |
| `PaxmeetIcon.jsx` | React component — `<PaxmeetIcon name="home" size={24} color="#7332D6" />`. |
| `icon-names.js` | Array of all valid icon names (for dropdowns / validation). |

---

## Setup (Next.js App Router, the layout used by Paxmeet_NJS)

1. **Copy** this folder into the site, e.g. `src/components/paxmeet-icons/`.

2. **Import the CSS once.** Either in `src/app/globals.css`:
   ```css
   @import "../components/paxmeet-icons/paxmeet-icons.css";
   ```
   …or in `src/app/layout.js`:
   ```js
   import "@/components/paxmeet-icons/paxmeet-icons.css";
   ```
   (`PaxmeetIcon.jsx` also imports the CSS itself, so importing the component is enough.)

3. **Use it** in any component:
   ```jsx
   import { PaxmeetIcon } from "@/components/paxmeet-icons/PaxmeetIcon";

   export default function Example() {
     return (
       <button>
         <PaxmeetIcon name="search" size={20} color="#7332D6" />
         Search
       </button>
     );
   }
   ```

### Prefer plain CSS classes (no component)?
After importing the CSS, just use:
```html
<i class="pmi pmi-home" style="font-size:24px; color:#7332D6"></i>
```
`color` and `font-size` control the icon — it's a font, so it inherits text color by default.

---

## Notes

- **One source of truth:** all web files are generated from the same font by
  `tool/build_web_assets.py`. When icons are added/renamed in the package,
  re-run it and copy the updated files over (or pull via the steps below).
- **TypeScript site?** Rename `PaxmeetIcon.jsx` → `PaxmeetIcon.tsx` and type the
  props: `{ name: string; size?: number; color?: string; className?: string }`.
- **npm option (later):** this folder can be published as a small npm package so
  the site does `npm i @paxmeet/icons` instead of copying files. Ask if you want
  that set up.

## Pulling updates

The package repo is `https://github.com/letssuhail/paxmeet_icons`. To grab the
latest web assets:
```bash
git clone https://github.com/letssuhail/paxmeet_icons.git
cp -r paxmeet_icons/web/* <your-site>/src/components/paxmeet-icons/
```
