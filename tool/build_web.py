#!/usr/bin/env python3
"""Generate a self-contained icon-reference webpage (index.html) from the
generated font + Dart class. Font is embedded as base64 so the page is a single
file that works anywhere - open it directly or host it on GitHub Pages.

Click an icon → modal with Flutter + React + HTML code, each with a copy button.
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

# multiline Flutter dependency snippet (real newlines so copy pastes correctly)
PUBSPEC_DEP = ("paxmeet_icons:\n"
               "    git:\n"
               "      url: https://github.com/letssuhail/paxmeet_icons.git\n"
               "      ref: main")

cells = "\n".join(
    f'''      <button class="cell" data-name="{n}" data-cp="{cp:x}">
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
<title>paxmeet_icons - {len(items)} icons</title>
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
  .htop {{ display:flex; align-items:flex-start; justify-content:space-between; gap:12px; }}
  h1 {{ margin:0 0 4px; font-size:20px; }}
  h1 span {{ color:var(--accent); }}
  .docbtn {{ display:inline-flex; align-items:center; gap:7px; background:var(--accent); color:#fff;
             border:none; border-radius:10px; padding:9px 16px; font-size:13px; font-weight:600;
             cursor:pointer; white-space:nowrap; }}
  .docbtn:hover {{ filter:brightness(1.1); }}
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
  .empty {{ padding:40px 24px; color:var(--sub); }}

  /* modal */
  .backdrop {{ position:fixed; inset:0; background:rgba(0,0,0,.6); backdrop-filter:blur(3px);
               display:flex; align-items:center; justify-content:center; padding:20px; z-index:20;
               opacity:0; transition:.15s; }}
  .backdrop.show {{ opacity:1; }}
  .modal {{ background:var(--card); border:1px solid var(--line); border-radius:18px; width:min(560px,100%);
            padding:24px; box-shadow:0 20px 60px rgba(0,0,0,.5); transform:scale(.96); transition:.15s; }}
  .backdrop.show .modal {{ transform:scale(1); }}
  .mhead {{ display:flex; align-items:center; gap:16px; margin-bottom:20px; }}
  .mhead .mico {{ font-family:"PaxmeetIcons"; font-size:48px; color:var(--accent); line-height:1;
                  width:80px; height:80px; display:flex; align-items:center; justify-content:center;
                  background:var(--bg); border-radius:14px; border:1px solid var(--line); }}
  .mhead .mname {{ font-size:20px; font-weight:600; }}
  .mhead .mclose {{ margin-left:auto; background:none; border:none; color:var(--sub); font-size:26px;
                    cursor:pointer; line-height:1; padding:4px 8px; border-radius:8px; }}
  .mhead .mclose:hover {{ background:var(--bg); color:var(--txt); }}
  .snip {{ margin-bottom:14px; }}
  .snip .lbl {{ font-size:11px; text-transform:uppercase; letter-spacing:.5px; color:var(--sub); margin-bottom:6px; }}
  .snip .row {{ display:flex; align-items:stretch; gap:8px; }}
  .snip code {{ flex:1; font-family:"SF Mono",Menlo,Consolas,monospace; font-size:13px; color:#d6c9ff;
                background:var(--bg); border:1px solid var(--line); border-radius:10px; padding:11px 13px;
                overflow-x:auto; white-space:nowrap; }}
  .snip .cp {{ background:var(--accent); color:#fff; border:none; border-radius:10px; padding:0 14px;
               font-size:12px; font-weight:600; cursor:pointer; white-space:nowrap; }}
  .snip .cp:hover {{ filter:brightness(1.1); }}
  .snip .cp.ok {{ background:#22c55e; }}

  /* install modal */
  .modal.wide {{ width:min(680px,100%); max-height:88vh; overflow-y:auto; }}
  .isec {{ margin-bottom:22px; }}
  .isec h3 {{ font-size:15px; margin:0 0 10px; }}
  .istep {{ display:flex; gap:10px; margin-bottom:10px; }}
  .istep .num {{ flex:0 0 22px; height:22px; border-radius:50%; background:transparent; border:1px solid var(--line);
                 color:var(--sub); font-size:12px; display:flex; align-items:center; justify-content:center; margin-top:2px; }}
  .istep .body {{ flex:1; min-width:0; }}
  .istep .body p {{ margin:2px 0 6px; font-size:13px; color:var(--txt); }}
  .istep .body .muted {{ color:var(--sub); }}
  code.multi {{ white-space:pre !important; line-height:1.5; }}

  .toast {{ position:fixed; bottom:24px; left:50%; transform:translateX(-50%) translateY(20px);
            background:var(--accent); color:#fff; padding:10px 18px; border-radius:10px; font-size:13px;
            opacity:0; transition:.2s; pointer-events:none; z-index:30; }}
  .toast.show {{ opacity:1; transform:translateX(-50%) translateY(0); }}
</style>
</head>
<body>
  <header>
    <div class="htop">
      <div>
        <h1>paxmeet<span>_icons</span></h1>
        <div class="sub">{len(items)} icons · click any to see Flutter &amp; web code · type to filter</div>
      </div>
      <button class="docbtn" id="docbtn">Install</button>
    </div>
    <input id="q" placeholder="Search icons…" autocomplete="off">
  </header>
  <div class="grid" id="grid">
{cells}
  </div>
  <div class="empty" id="empty" hidden>No icons match.</div>

  <div class="backdrop" id="installBackdrop" hidden>
    <div class="modal wide" role="dialog" aria-modal="true">
      <div class="mhead">
        <span class="mname">Install paxmeet_icons</span>
        <button class="mclose" id="iclose" aria-label="Close">&times;</button>
      </div>

      <div class="isec">
        <h3>Flutter app</h3>
        <div class="istep"><div class="num">1</div><div class="body">
          <p class="muted">Add to <b>pubspec.yaml</b> under <code style="padding:1px 5px">dependencies:</code></p>
          <div class="snip"><div class="row">
            <code id="iF1" class="multi">{PUBSPEC_DEP}</code>
            <button class="cp" data-for="iF1">Copy</button></div></div>
        </div></div>
        <div class="istep"><div class="num">2</div><div class="body">
          <p class="muted">Install</p>
          <div class="snip"><div class="row"><code id="iF2">flutter pub get</code><button class="cp" data-for="iF2">Copy</button></div></div>
        </div></div>
        <div class="istep"><div class="num">3</div><div class="body">
          <p class="muted">Use anywhere</p>
          <div class="snip"><div class="row"><code id="iF3">Icon(PaxmeetIcons.home)</code><button class="cp" data-for="iF3">Copy</button></div></div>
        </div></div>
      </div>

      <div class="isec">
        <h3>Website (Next.js / React)</h3>
        <div class="istep"><div class="num">1</div><div class="body">
          <p class="muted">Copy the package's <b>web/</b> files into your site</p>
          <div class="snip"><div class="row">
            <code id="iW1">cp -r paxmeet_icons/web/* src/components/paxmeet-icons/</code>
            <button class="cp" data-for="iW1">Copy</button></div></div>
        </div></div>
        <div class="istep"><div class="num">2</div><div class="body">
          <p class="muted">Import the CSS once in <b>app/layout.js</b></p>
          <div class="snip"><div class="row">
            <code id="iW2">import "@/components/paxmeet-icons/paxmeet-icons.css";</code>
            <button class="cp" data-for="iW2">Copy</button></div></div>
        </div></div>
        <div class="istep"><div class="num">3</div><div class="body">
          <p class="muted">Use anywhere</p>
          <div class="snip"><div class="row">
            <code id="iW3">&lt;PaxmeetIcon name="home" /&gt;</code>
            <button class="cp" data-for="iW3">Copy</button></div></div>
        </div></div>
      </div>

      <p class="sub" style="margin:0">Same icon names on both platforms - click any icon for its exact code.</p>
    </div>
  </div>

  <div class="backdrop" id="backdrop" hidden>
    <div class="modal" role="dialog" aria-modal="true">
      <div class="mhead">
        <span class="mico" id="mico"></span>
        <span class="mname" id="mname"></span>
        <button class="mclose" id="mclose" aria-label="Close">&times;</button>
      </div>
      <div class="snip"><div class="lbl">Flutter</div><div class="row">
        <code id="cFlutter"></code><button class="cp" data-for="cFlutter">Copy</button></div></div>
      <div class="snip"><div class="lbl">React / Next.js</div><div class="row">
        <code id="cReact"></code><button class="cp" data-for="cReact">Copy</button></div></div>
      <div class="snip"><div class="lbl">HTML (CSS class)</div><div class="row">
        <code id="cHtml"></code><button class="cp" data-for="cHtml">Copy</button></div></div>
    </div>
  </div>

  <div class="toast" id="toast"></div>
<script>
  const q = document.getElementById('q');
  const cells = [...document.querySelectorAll('.cell')];
  const empty = document.getElementById('empty');
  const toast = document.getElementById('toast');
  const backdrop = document.getElementById('backdrop');
  const mico = document.getElementById('mico'), mname = document.getElementById('mname');
  const cFlutter = document.getElementById('cFlutter'), cReact = document.getElementById('cReact'), cHtml = document.getElementById('cHtml');
  let tt;

  q.addEventListener('input', () => {{
    const v = q.value.trim().toLowerCase();
    let shown = 0;
    cells.forEach(c => {{ const ok = c.dataset.name.toLowerCase().includes(v); c.hidden = !ok; if (ok) shown++; }});
    empty.hidden = shown > 0;
  }});

  function showToast(msg) {{
    toast.textContent = msg; toast.classList.add('show');
    clearTimeout(tt); tt = setTimeout(() => toast.classList.remove('show'), 1400);
  }}

  function openModal(name, cp) {{
    mico.innerHTML = '&#x' + cp + ';';
    mname.textContent = name;
    cFlutter.textContent = 'Icon(PaxmeetIcons.' + name + ')';
    cReact.textContent = '<PaxmeetIcon name="' + name + '" />';
    cHtml.textContent = '<i class="pmi pmi-' + name + '"></i>';
    backdrop.hidden = false;
    requestAnimationFrame(() => backdrop.classList.add('show'));
  }}
  function closeModal() {{
    backdrop.classList.remove('show');
    setTimeout(() => {{ backdrop.hidden = true; }}, 150);
  }}

  cells.forEach(c => c.addEventListener('click', () => openModal(c.dataset.name, c.dataset.cp)));
  document.getElementById('mclose').addEventListener('click', closeModal);
  backdrop.addEventListener('click', e => {{ if (e.target === backdrop) closeModal(); }});

  // install / docs modal
  const installBackdrop = document.getElementById('installBackdrop');
  function openInstall() {{ installBackdrop.hidden = false; requestAnimationFrame(() => installBackdrop.classList.add('show')); }}
  function closeInstall() {{ installBackdrop.classList.remove('show'); setTimeout(() => {{ installBackdrop.hidden = true; }}, 150); }}
  document.getElementById('docbtn').addEventListener('click', openInstall);
  document.getElementById('iclose').addEventListener('click', closeInstall);
  installBackdrop.addEventListener('click', e => {{ if (e.target === installBackdrop) closeInstall(); }});

  document.addEventListener('keydown', e => {{
    if (e.key !== 'Escape') return;
    if (!backdrop.hidden) closeModal();
    if (!installBackdrop.hidden) closeInstall();
  }});

  document.querySelectorAll('.cp').forEach(btn => btn.addEventListener('click', async () => {{
    const text = document.getElementById(btn.dataset.for).textContent;
    try {{ await navigator.clipboard.writeText(text); }} catch (e) {{}}
    const old = btn.textContent; btn.textContent = '✓'; btn.classList.add('ok');
    setTimeout(() => {{ btn.textContent = old; btn.classList.remove('ok'); }}, 900);
    showToast('Copied  ' + text);
  }}));
</script>
</body>
</html>'''

out = ROOT / "index.html"
out.write_text(html)
print(f"wrote {out}  ({len(items)} icons, {len(html)//1024} KB)")
