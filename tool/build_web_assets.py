#!/usr/bin/env python3
import re, base64, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
WEB = ROOT / "web"; WEB.mkdir(exist_ok=True)

dart = (ROOT / "lib/paxmeet_icons.dart").read_text()
ttf = (ROOT / "fonts/PaxmeetIcons.ttf").read_bytes()
b64 = base64.b64encode(ttf).decode()

# Use the SAME camelCase names as Flutter, so the team has one convention
# everywhere:  Flutter PaxmeetIcons.addCircle  <=>  web <PaxmeetIcon name="addCircle" />
items = re.findall(r'static const IconData (\w+) = IconData\(0x([0-9a-fA-F]+)', dart)
rows = sorted(((n, n, int(h, 16)) for n, h in items), key=lambda x: x[1])

# ---- CSS ----
classes = "\n".join(f'.pmi-{k}::before {{ content: "\\{cp:x}"; }}' for _, k, cp in rows)
css = f'''/* paxmeet-icons - generated. Do not edit by hand. */
@font-face {{
  font-family: "PaxmeetIcons";
  src: url("data:font/ttf;base64,{b64}") format("truetype");
  font-weight: normal; font-style: normal; font-display: block;
}}
.pmi {{
  font-family: "PaxmeetIcons" !important;
  speak: none; font-style: normal; font-weight: normal; font-variant: normal;
  text-transform: none; line-height: 1; display: inline-block;
  -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;
}}
{classes}
'''
(WEB / "paxmeet-icons.css").write_text(css)

# ---- React component (JSX) ----
jsx = '''// paxmeet-icons React component - generated.
// Usage:  import { PaxmeetIcon } from "@/components/paxmeet-icons/PaxmeetIcon";
//         <PaxmeetIcon name="home" size={24} color="#7332D6" />
import "./paxmeet-icons.css";

export function PaxmeetIcon({ name, size = 24, color, className = "", style, ...rest }) {
  return (
    <i
      className={`pmi pmi-${name} ${className}`}
      style={{ fontSize: size, color, ...style }}
      aria-hidden="true"
      {...rest}
    />
  );
}
'''
(WEB / "PaxmeetIcon.jsx").write_text(jsx)

# ---- names list ----
names_js = "// Generated list of icon names.\nexport const paxmeetIconNames = [\n" + \
    "".join(f'  "{k}",\n' for _, k, _ in rows) + "];\n"
(WEB / "icon-names.js").write_text(names_js)

print(f"wrote web/paxmeet-icons.css, web/PaxmeetIcon.jsx, web/icon-names.js  ({len(rows)} icons)")
