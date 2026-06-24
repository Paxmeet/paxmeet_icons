#!/usr/bin/env python3
"""Generate a self-contained icon-reference webpage (index.html) from the
generated font + Dart class. Font is embedded as base64 so the page works
anywhere (open the file directly, or host it on GitHub Pages).
Run:  tool/.venv/bin/python tool/build_web.py
"""
import re, base64, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
dart = (ROOT / "lib/paxmeet_icons.dart").read_text()
ttf = (ROOT / "fonts/PaxmeetIcons.ttf").read_bytes()
b64 = base64.b64encode(ttf).decode()

# name -> codepoint (sorted by name)
items = re.findall(r'static const IconData (\w+) = IconData\(0x([0-9a-fA-F]+)', dart)
items = sorted(((n, int(h, 16)) for n, h in items), key=lambda x: x[0])

cells = "\n".join(
    f'''      <button class="cell" data-name="{n}" data-code="PaxmeetIcons.{n}">
        <span class="ico">&#x{cp:x};</span>
        <span class="name">{n}</span>
      </button>'''
    for n, cp in items
)

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>paxmeet_icons — {len(items)} icons</title>
<style>
  @font-face {{
    font-family: "PaxmeetIcons";
    src: url("data:font/ttf;base64,{b64}") format("truetype");
    font-display: block;
  }}
  :root {{ --bg:#0f1014; --card:#1a1b22; --line:#2a2c36; --txt:#e7e7ee; --sub:#9aa0b4; --accent:#7c4dff; }}
  * {{ box-sizing:border-box; }}
  [hidden] {{ display:none !important; }}
  body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
         background:var(--bg); color:var(--txt); }}
  header {{ position:sticky; top:0; background:rgba(15,16,20,.9); backdrop-filter:blur(8px);
            padding:20px 24px 14px; border-bottom:1px solid var(--line); z-index:5; }}
  h1 {{ margin:0 0 4px; font-size:20px; }}
  h1 span {{ color:var(--accent); }}
  .sub {{ color:var(--sub); font-size:13px; margin-bottom:12px; }}
  #q {{ width:100%; max-width:420px; padding:10px 14px; border-radius:10px; border:1px solid var(--line);
        background:var(--card); color:var(--txt); font-size:14px; outline:none; }}
  #q:focus {{ border-color:var(--accent); }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(120px,1fr)); gap:12px; padding:24px; }}
  .cell {{ display:flex; flex-direction:column; align-items:center; gap:10px; padding:18px 8px;
           background:var(--card); border:1px solid var(--line); border-radius:14px; color:var(--txt);
           cursor:pointer; font:inherit; transition:.12s; }}
  .cell:hover {{ border-color:var(--accent); transform:translateY(-2px); }}
  .ico {{ font-family:"PaxmeetIcons"; font-size:38px; line-height:1; color:var(--accent); }}
  .name {{ font-size:12px; color:var(--sub); text-align:center; word-break:break-word; }}
  .cell.copied .name {{ color:#4ade80; }}
  .toast {{ position:fixed; bottom:24px; left:50%; transform:translateX(-50%) translateY(20px);
            background:var(--accent); color:#fff; padding:10px 18px; border-radius:10px; font-size:13px;
            opacity:0; transition:.2s; pointer-events:none; }}
  .toast.show {{ opacity:1; transform:translateX(-50%) translateY(0); }}
  .empty {{ padding:40px 24px; color:var(--sub); }}
</style>
</head>
<body>
  <header>
    <h1>paxmeet<span>_icons</span></h1>
    <div class="sub">{len(items)} icons · click any to copy its Flutter code · type to filter</div>
    <input id="q" placeholder="Search icons…" autocomplete="off">
  </header>
  <div class="grid" id="grid">
{cells}
  </div>
  <div class="empty" id="empty" hidden>No icons match.</div>
  <div class="toast" id="toast"></div>
<script>
  const q = document.getElementById('q');
  const cells = [...document.querySelectorAll('.cell')];
  const empty = document.getElementById('empty');
  const toast = document.getElementById('toast');
  let tt;
  q.addEventListener('input', () => {{
    const v = q.value.trim().toLowerCase();
    let shown = 0;
    cells.forEach(c => {{ const ok = c.dataset.name.toLowerCase().includes(v); c.hidden = !ok; if (ok) shown++; }});
    empty.hidden = shown > 0;
  }});
  cells.forEach(c => c.addEventListener('click', async () => {{
    const code = c.dataset.code;
    try {{ await navigator.clipboard.writeText(code); }} catch (e) {{}}
    c.classList.add('copied'); setTimeout(() => c.classList.remove('copied'), 800);
    toast.textContent = 'Copied  ' + code;
    toast.classList.add('show'); clearTimeout(tt); tt = setTimeout(() => toast.classList.remove('show'), 1400);
  }}));
</script>
</body>
</html>'''

out = ROOT / "index.html"
out.write_text(html)
print(f"wrote {out}  ({len(items)} icons, {len(html)//1024} KB)")
