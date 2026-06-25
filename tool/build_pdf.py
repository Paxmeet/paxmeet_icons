#!/usr/bin/env python3
import pathlib, markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

PARTS = [
    ("Using paxmeet_icons (Flutter app + Web)", DOCS / "USAGE.md"),
    ("Adding / updating / removing icons", DOCS / "ADDING_ICONS.md"),
]

md = markdown.Markdown(extensions=["tables", "fenced_code", "toc"])

sections = []
for i, (_, path) in enumerate(PARTS):
    text = path.read_text()
    # drop the first H1 (we render our own title) - keep it simple
    html = md.convert(text)
    md.reset()
    page_break = ' style="page-break-before: always;"' if i > 0 else ""
    sections.append(f'<section{page_break}>{html}</section>')

body = "\n".join(sections)

doc = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>paxmeet_icons - Documentation</title>
<style>
  @page {{ size: A4; margin: 18mm 16mm; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
          color: #1c1d22; font-size: 12px; line-height: 1.55; margin: 0; }}
  .cover {{ text-align: center; padding: 40px 0 28px; border-bottom: 3px solid #7332D6; margin-bottom: 24px; }}
  .cover h1 {{ font-size: 30px; margin: 0; }}
  .cover h1 span {{ color: #7332D6; }}
  .cover p {{ color: #6b7280; margin: 6px 0 0; }}
  h1 {{ font-size: 20px; color: #2a1a55; border-bottom: 1px solid #e5e7eb; padding-bottom: 6px; margin-top: 4px; }}
  h2 {{ font-size: 15px; color: #4c2fa6; margin-top: 22px; }}
  h3 {{ font-size: 13px; color: #333; margin-top: 16px; }}
  p, li {{ font-size: 12px; }}
  code {{ font-family: "SF Mono", Menlo, Consolas, monospace; font-size: 11px;
          background: #f3f0ff; color: #5b21b6; padding: 1px 5px; border-radius: 4px; }}
  pre {{ background: #1a1b22; color: #e7e7ee; padding: 12px 14px; border-radius: 8px; overflow-x: auto; }}
  pre code {{ background: none; color: inherit; padding: 0; font-size: 11px; }}
  table {{ border-collapse: collapse; width: 100%; margin: 12px 0; }}
  th, td {{ border: 1px solid #e5e7eb; padding: 6px 9px; text-align: left; font-size: 11px; vertical-align: top; }}
  th {{ background: #f5f3ff; color: #4c2fa6; }}
  blockquote {{ border-left: 3px solid #c4b5fd; margin: 12px 0; padding: 2px 14px; color: #555; background: #faf9ff; }}
  a {{ color: #6d28d9; text-decoration: none; }}
  section {{ margin-bottom: 8px; }}
  hr {{ border: none; border-top: 1px solid #e5e7eb; margin: 20px 0; }}
</style></head>
<body>
  <div class="cover">
    <h1>paxmeet<span>_icons</span></h1>
    <p>Custom icon-font package - Documentation</p>
    <p style="font-size:11px;">Install &amp; usage · Adding / renaming / removing icons</p>
  </div>
  {body}
</body></html>'''

out = DOCS / "paxmeet_icons_docs.html"
out.write_text(doc)
print("wrote", out)
