#!/usr/bin/env python3
"""Generate bottom-right caption overlay PNGs for CM v3 (rebalanced scene list)."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 832, 480
OUT = "/home/ubuntu/202705jpmarathon/video/captions"
os.makedirs(OUT, exist_ok=True)
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
f = ImageFont.truetype(FONT, 26) if os.path.exists(FONT) else ImageFont.load_default()

captions = [
    "仙台・杜之都晨光",
    "仙台國際半馬 5·9",
    "平泉・中尊寺金色堂",
    "嚴美溪・溪谷",
    "松島・日本三景",
    "秋保大滝・瀑布",
    "前澤牛・慶功",
    "花卷溫泉・恢復",
    "奥州きらめき全馬 5·16",
    "癡LS Group",
]

for i, text in enumerate(captions, 1):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad = 20
    bbox = d.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]; th = bbox[3] - bbox[1]
    x = W - pad - tw; y = H - pad - th
    for dx, dy in [(-1,-1),(-1,1),(1,-1),(1,1),(0,-2),(0,2),(2,0),(-2,0)]:
        d.text((x+dx, y+dy), text, font=f, fill=(0,0,0,200))
    d.rectangle([x-14, y-10, W-pad+6, y+th+12], fill=(20,20,18,110))
    d.text((x, y), text, font=f, fill=(255,255,255,255))
    img.save(f"{OUT}/cap{i:02d}.png")
    print(f"cap{i:02d}.png : {text}")
print("done")
