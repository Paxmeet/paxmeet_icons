import re, math
from PIL import Image, ImageDraw, ImageFont

dart = open("lib/paxmeet_icons.dart").read()
# name -> codepoint
items = re.findall(r'static const IconData (\w+) = IconData\(0x([0-9a-fA-F]+)', dart)
items = [(n, int(h,16)) for n,h in items]
items.sort(key=lambda x: x[0])

cell, glyph_px, pad = 120, 64, 8
cols = 6
rows = math.ceil(len(items)/cols)
W, H = cols*cell, rows*cell
img = Image.new("RGB", (W,H), "white")
d = ImageDraw.Draw(img)
font = ImageFont.truetype("fonts/PaxmeetIcons.ttf", glyph_px)
try:
    label = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 11)
except: label = ImageFont.load_default()

for i,(name,cp) in enumerate(items):
    cx = (i%cols)*cell; cy=(i//cols)*cell
    ch = chr(cp)
    # center glyph
    bbox = d.textbbox((0,0), ch, font=font)
    gw, gh = bbox[2]-bbox[0], bbox[3]-bbox[1]
    gx = cx + (cell-gw)/2 - bbox[0]
    gy = cy + (cell-glyph_px)/2 - bbox[1] - 6
    d.text((gx,gy), ch, font=font, fill=(80,40,160))
    # label
    lb = d.textbbox((0,0), name, font=label)
    lw = lb[2]-lb[0]
    d.text((cx+(cell-lw)/2, cy+cell-20), name, font=label, fill=(60,60,60))
    d.rectangle([cx,cy,cx+cell-1,cy+cell-1], outline=(220,220,220))

out="preview.png"
img.save(out)
print("saved", out, f"({len(items)} glyphs)")
