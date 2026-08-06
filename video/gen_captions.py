#!/usr/bin/env python3
"""Generate bottom-right caption overlay PNGs for the 30s CM."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 832, 480
OUT = "/home/ubuntu/202705jpmarathon/video/captions"
os.makedirs(OUT, exist_ok=True)

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
try:
    f = ImageFont.truetype(FONT, 26)
    fsmall = ImageFont.truetype(FONT, 22)
except Exception:
    f = fsmall = ImageFont.load_default()

captions = [
    "仙台・杜之都晨光",
    "仙台國際半馬 5·9",
    "跑手備戰・熱身",
    "平泉・中尊寺金色堂",
    "松島・日本三景",
    "花卷溫泉・恢復",
    "前澤牛・慶功",
    "奥州きらめき全馬 5·16",
    "全馬衝線・破PB",
    "癡LS Group",
]

def caption_png(text, path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad = 20
    # measure
    bbox = d.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = W - pad - tw
    y = H - pad - th
    # shadow / outline
    for dx, dy in [(-1,-1),(-1,1),(1,-1),(1,1),(0,-2),(0,2),(2,0),(-2,0)]:
        d.text((x+dx, y+dy), text, font=f, fill=(0, 0, 0, 200))
    # soft bg chip
    d.rectangle([x-14, y-10, W-pad+6, y+th+12], fill=(20, 20, 18, 110))
    d.text((x, y), text, font=f, fill=(255, 255, 255, 255))
    img.save(path)
    return tw

for i, cap in enumerate(captions, 1):
    caption_png(cap, f"{OUT}/cap{i:02d}.png")
    print(f"cap{i:02d}.png : {cap}")

print("done ->", OUT)
