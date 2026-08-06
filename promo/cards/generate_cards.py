#!/usr/bin/env python3
"""Generate 5 bright vibrant social media cards for 癡LS Group 東北雙馬拉松 2027."""
import os, math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ---------- Constants ----------
W, H = 1080, 1350
IZ = "/home/ubuntu/202705jpmarathon/assets/icons/"
AZ = "/home/ubuntu/202705jpmarathon/assets/"
OUT = "/home/ubuntu/202705jpmarathon/promo/cards/"
os.makedirs(OUT, exist_ok=True)

# Brand palette
CORAL   = (255, 90, 95)     # #ff5a5f
SUN     = (255, 194, 60)    # #ffc23c
SKY     = (57, 183, 232)    # #39b7e8
GRASS   = (124, 201, 84)    # #7cc954
INK     = (35, 48, 58)      # #23303a
CREAM   = (255, 250, 240)   # #fffaf0
WHITE   = (255, 255, 255)

YOZAI = "/usr/share/fonts/truetype/custom/Yozai-Regular.ttf"
APTOS = "/usr/share/fonts/truetype/custom/Aptos.ttf"
APTOSB = "/usr/share/fonts/truetype/custom/Aptos-Bold.ttf"

def F(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)

def pick_cjk(size, bold=False):
    return F(YOZAI, size)
def pick_lat(size, bold=False):
    return F(APTOSB if bold else APTOS, size)

# ---------- Helper: mixed CJK+Latin text ----------
def draw_mixed(draw, xy, parts, size, fill, lat_font=None, bold=True, anchor_left=True, center_x=None):
    """parts = list of (text, is_chinese). Renders CJK with Yozai, latin with Aptos(Bold).
    Returns total width. If center_x given, centers the whole run at that x."""
    cjk = pick_cjk(size)
    lat = lat_font or (pick_lat(int(size*0.96), bold=bold))
    widths, fonts = [], []
    for text, is_cjk in parts:
        f = cjk if is_cjk else lat
        bb = draw.textbbox((0, 0), text, font=f)
        widths.append(bb[2] - bb[0])
        fonts.append(f)
    total = sum(widths)
    x = xy[0]
    if center_x is not None:
        x = center_x - total // 2
    baseline_bottom = xy[1]  # y is the bottom (baseline of the run)
    for (text, is_cjk), w, f in zip(parts, widths, fonts):
        bb = draw.textbbox((0, 0), text, font=f)
        y = baseline_bottom - (bb[3] - bb[1]) + bb[1]
        draw.text((x, y), text, font=f, fill=fill)
        x += w
    return total

def text_w(draw, text, size, is_cjk=True, lat_font=None, bold=True):
    cjk = pick_cjk(size)
    lat = lat_font or pick_lat(int(size*0.96), bold=bold)
    f = cjk if is_cjk else lat
    bb = draw.textbbox((0, 0), text, font=f)
    return bb[2] - bb[0]

def text_h(draw, text, size, is_cjk=True):
    bb = draw.textbbox((0, 0), text, font=pick_cjk(size))
    return bb[3] - bb[1]

def center_text(draw, y, text, size, fill, is_cjk=True, bold=True, cx=None):
    cx = cx if cx is not None else W//2
    w = text_w(draw, text, size, is_cjk, bold=bold)
    bb = draw.textbbox((0, 0), text, font=pick_cjk(size))
    h = bb[3] - bb[1]
    draw.text((cx - w//2, y - h//2 - bb[1]), text, font=pick_cjk(size), fill=fill)
    return h

# ---------- Helper: gradient background ----------
def v_gradient(w, h, top_color, mid_color=None, bottom_color=None):
    img = Image.new("RGB", (w, h))
    px = img.load()
    mid_color = mid_color or top_color
    bottom_color = bottom_color or mid_color
    for y in range(h):
        if y < h*0.55:
            t = y / (h*0.55)
            c = tuple(int(top_color[i] + (mid_color[i]-top_color[i])*t) for i in range(3))
        else:
            t = (y - h*0.55) / (h*0.45)
            c = tuple(int(mid_color[i] + (bottom_color[i]-mid_color[i])*t) for i in range(3))
        for x in range(w):
            px[x, y] = c
    return img

# ---------- Helper: strip white from icon -> transparent on given layer ----------
def load_icon(name, size):
    """Load icon, strip near-white to transparent, resize to `size` (square)."""
    im = Image.open(IZ + name).convert("RGBA")
    im = im.resize((size, size), Image.LANCZOS)
    a = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, alpha = a[x, y]
            if r > 244 and g > 244 and b > 244 and alpha > 200:
                a[x, y] = (r, g, b, 0)
    return im

def rounded_icon_circle(icon_name, dia, bg=WHITE, ring=None, ring_w=0):
    """Place an icon in a white rounded circle, optionally with a colored ring. Returns an RGBA layer (icon_canvas_dia square)."""
    size = int(dia)
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # outer ring
    if ring and ring_w:
        d.ellipse([0, 0, size-1, size-1], fill=ring)
    inner = size - 2*ring_w
    off = ring_w
    d.ellipse([off, off, off+inner-1, off+inner-1], fill=bg)
    pad = int(inner*0.26)
    icon = load_icon(icon_name, inner - 2*pad)
    a = icon.load()
    # Apply circular mask to icon
    mask = Image.new("L", icon.size, 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([0, 0, icon.size[0]-1, icon.size[1]-1], fill=255)
    px = layer.load()
    ix = off + pad
    for yy in range(icon.height):
        for xx in range(icon.width):
            if mask.getpixel((xx, yy)) > 128:
                r, g, b, aa = icon.getpixel((xx, yy))
                px[ix+xx, off+pad+yy] = (r, g, b, aa)
    return layer

def paste_center(base, layer, center_point):
    """Paste `layer` centered on center_point (x,y)."""
    w, h = layer.size
    base.paste(layer, (int(center_point[0]-w//2), int(center_point[1]-h//2)), layer)

# ---------- Branding badges ----------
def brand_circle(font_size, diameter=96, fill=SUN, text_color=INK):
    """Circle with 癡 char."""
    layer = Image.new("RGBA", (diameter, diameter), (0,0,0,0))
    d = ImageDraw.Draw(layer)
    d.ellipse([0, 0, diameter-1, diameter-1], fill=fill)
    f = pick_cjk(font_size)
    bb = d.textbbox((0,0), "癡", font=f)
    w = bb[2]-bb[0]; h = bb[3]-bb[1]
    d.text((diameter//2 - w//2 - bb[0], diameter//2 - h//2 - bb[1]), "癡", font=f, fill=text_color)
    return layer

def draw_brand_header(base, draw, cx_it):
    """Top branding: circle + '癡LS Group' + tagline. Returns bottom y."""
    circle = brand_circle(64, 108, fill=SUN, text_color=INK)
    paste_center(base, circle, (cx_it, 70))
    # name to the right
    y = 62
    # 癡LS Group mixed
    parts = [("癡", True), ("LS ", False), ("Group", False)]
    draw_mixed(draw, (0, y+34), parts, 40, fill=INK, bold=True, center_x=cx_it+150)
    # tagline
    t = "一個假期，兩場馬拉松"
    draw_mixed(draw, (0, y+72), [(t, True)], 26, fill=CORAL, bold=False, center_x=cx_it+150)
    return 120

# ---------- Card 1: Announcement hero ----------
def card_announce():
    # Base: hero-sendai photo as background
    img = Image.new("RGB", (W, H), CREAM)
    hero = Image.open(AZ+"hero-sendai.jpg").convert("RGB")
    # crop to portrait aspect
    tw, th = hero.size
    target = tw / W * H
    if target <= th:
        top = int((th - target)//2); hero = hero.crop((0, top, tw, top+target))
    else:
        # too tall; crop width
        left = int((tw - target)//2); hero = hero.crop((left, 0, left+target, th))
    hero = hero.resize((W, H), Image.LANCZOS)
    # Blend hero with coral->sun gradient for bright vibrant look
    grad = v_gradient(W, H, CORAL, SUN, (255, 170, 95))
    # Use vivid blend: mostly gradient structure but keep photo visible
    blended = Image.blend(hero, grad, 0.60)
    img.paste(blended, (0, 0))
    draw = ImageDraw.Draw(img)

    # Slight dark scrim behind top text zone for legibility
    scrim = Image.new("RGBA", (W, 260), (35, 48, 58, 90))
    img.paste(scrim, (0, 0), scrim)

    # Brand header (white circle variant here)
    circle = brand_circle(64, 108, fill=SUN, text_color=INK)
    paste_center(img, circle, (W//2, 70))
    draw_mixed(draw, (0, 104), [("癡", True), ("LS ", False), ("Group", False)], 40, fill=WHITE, bold=True, center_x=W//2+150)
    draw_mixed(draw, (0, 142), [("一個假期，兩場馬拉松", True)], 26, fill=SUN, bold=False, center_x=W//2+150)

    # Runner icon large in white circle
    run_layer = rounded_icon_circle("icon-runner.png", 330, bg=WHITE, ring=SUN, ring_w=14)
    paste_center(img, run_layer, (W//2, 455))

    # dotted divider
    for i in range(12):
        draw.ellipse([W//2 - 120 + i*22, 655, W//2 - 118 + i*22, 667], fill=SUN)

    # Big headline
    center_text(draw, 730, "一個假期，", 96, fill=WHITE, is_cjk=True, bold=True)
    center_text(draw, 845, "兩場馬拉松", 96, fill=SUN, is_cjk=True, bold=True)

    # subtitle tag
    sub = "仙台半馬 × 岩手奥州全馬"
    sub_w = text_w(draw, sub, 44, is_cjk=True, bold=True)
    draw.rounded_rectangle([(W-sub_w)//2-40, 950, (W+sub_w)//2+40, 1024], radius=37, fill=INK)
    center_text(draw, 987, sub, 44, fill=SUN, is_cjk=True, bold=True)

    # bottom date line
    dt = "仙台 5/9 · 奥州 5/16 · 佛誕 5/13"
    center_text(draw, 1085, dt, 40, fill=WHITE, is_cjk=False, bold=True)

    # footer brand line
    draw_mixed(draw, (0, 1260), [("癡LS Group · 東北雙馬拉松 2027", True)], 30, fill=WHITE, bold=False, center_x=W//2)

    img.save(OUT+"card-announce.png")

# ---------- Card 2: Two races ----------
def card_races():
    img = Image.new("RGB", (W, H), CREAM)
    # sky->grass gradient
    grad = v_gradient(W, H, SKY, (150, 220, 240), GRASS)
    # add soft sky tint; use gradient image directly
    img.paste(grad, (0, 0))
    draw = ImageDraw.Draw(img)

    draw_brand_header(img, draw, W//2)

    # Title
    center_text(draw, 185, "兩場賽事，", 72, fill=INK, is_cjk=True, bold=True)
    center_text(draw, 265, "雙倍精彩", 72, fill=WHITE, is_cjk=True, bold=True)

    # Medal icon center
    medal = rounded_icon_circle("icon-medal.png", 250, bg=WHITE, ring=SUN, ring_w=12)
    paste_center(img, medal, (W//2, 470))

    # Race card 1: Sendai
    y = 640
    card_w = W-120
    cw = card_w
    ch = 265
    x0 = (W-cw)//2
    draw.rounded_rectangle([x0, y, x0+cw, y+ch], radius=36, fill=WHITE, outline=SUN, width=5)
    # accent bar
    draw.rounded_rectangle([x0, y, x0+cw, y+20], radius=10, fill=CORAL)
    # race name
    center_text(draw, y+70, "仙台國際半馬", 46, fill=CORAL, is_cjk=True, bold=True, cx=x0+cw//2)
    # date/time
    draw_mixed(draw, (0, y+138), [("5月9日", True), ("  (10:05 起步)", False)], 40, fill=INK, bold=True, center_x=x0+cw//2)
    sub = "半程馬拉松 · 21.0975km"
    center_text(draw, y+196, sub, 30, fill=(140,140,140), is_cjk=True, bold=False, cx=x0+cw//2)

    # Race card 2
    y2 = y + ch + 40
    draw.rounded_rectangle([x0, y2, x0+cw, y2+ch], radius=36, fill=WHITE, outline=SUN, width=5)
    draw.rounded_rectangle([x0, y2, x0+cw, y2+20], radius=10, fill=GRASS)
    center_text(draw, y2+70, "岩手奧州閃耀馬拉松", 46, fill=GRASS, is_cjk=True, bold=True, cx=x0+cw//2)
    draw_mixed(draw, (0, y2+138), [("5月16日", True), ("  (8:30 起步)", False)], 40, fill=INK, bold=True, center_x=x0+cw//2)
    sub2 = "全程馬拉松 · 42.195km"
    center_text(draw, y2+196, sub2, 30, fill=(140,140,140), is_cjk=True, bold=False, cx=x0+cw//2)

    # footer
    draw_mixed(draw, (0, 1300), [("癡LS Group · 東北雙馬拉松 2027", True)], 26, fill=WHITE, bold=False, center_x=W//2)

    img.save(OUT+"card-races.png")

# ---------- Card 3: 請4放9 holiday math ----------
def card_leave():
    img = Image.new("RGB", (W, H), CREAM)
    grad = v_gradient(W, H, (255, 235, 190), SUN, (255, 220, 150))
    img.paste(grad, (0, 0))
    draw = ImageDraw.Draw(img)

    draw_brand_header(img, draw, W//2)

    # Sakura icon
    sakura = rounded_icon_circle("icon-sakura.png", 250, bg=WHITE, ring=CORAL, ring_w=12)
    paste_center(img, sakura, (W//2, 420))

    # Headline
    center_text(draw, 590, "請4日假，玩足9日", 72, fill=INK, is_cjk=True, bold=True)
    center_text(draw, 675, "一個假期睇晒東北", 40, fill=CORAL, is_cjk=True, bold=False)

    # Holiday strip: 5/8 -> 5/16
    strip_y = 760
    # timeline bar
    bx0, bx1 = 150, W-150
    draw.rounded_rectangle([bx0, strip_y, bx1, strip_y+12], radius=6, fill=WHITE)
    # arrow labels
    lbl = ["5/8", "5/9", "5/13", "5/16"]
    pos = {
        "5/8": 220, "5/9": 400, "5/13": 660, "5/16": 880
    }
    # markers on bar
    def marker(x, color, label, label_color, size=64):
        draw.ellipse([x-size//2, strip_y- (size-12)//2, x+size//2, strip_y + (size-12)//2], fill=color)
        # label above
        center_text(draw, strip_y-40, label, size//2, fill=label_color, is_cjk=False, bold=True, cx=x)
    marker(pos["5/8"], SUN, "5/8", INK)
    marker(pos["5/9"], GRASS, "5/9", INK)
    marker(pos["5/13"], CORAL, "5/13", WHITE)
    marker(pos["5/16"], SKY, "5/16", INK)

    # labels row
    yl = strip_y + 78
    cap_cx = [220, 400, 660, 880]
    caps = [("請假", INK, 30), ("仙台半馬", CORAL, 30), ("佛誕", WHITE, 34), ("奥州全馬", GRASS, 30)]
    for cx, (txt, col, sz) in zip(cap_cx, caps):
        if txt == "佛誕":
            tw = text_w(draw, "佛誕假期", 32, is_cjk=True, bold=True)
            draw.rounded_rectangle([cx-tw//2-26, yl-24, cx+tw//2+26, yl+46], radius=35, fill=CORAL)
            center_text(draw, yl, "佛誕假期", 32, fill=WHITE, is_cjk=True, bold=True, cx=cx)
        elif txt == "請假":
            center_text(draw, yl, "請假", sz, fill=col, is_cjk=True, bold=True, cx=cx)
        else:
            center_text(draw, yl, txt, sz, fill=col, is_cjk=True, bold=True, cx=cx)

    # bottom math
    my = yl + 130
    center_text(draw, my, "4", 96, fill=CORAL, is_cjk=False, bold=True, cx=W//2 - 300)
    draw_mixed(draw, (0, my+32), [("日年假", True)], 46, fill=INK, bold=True, center_x=W//2 - 170)
    center_text(draw, my, "=", 84, fill=INK, is_cjk=False, bold=True, cx=W//2 + 20)
    center_text(draw, my, "9", 96, fill=SUN, is_cjk=False, bold=True, cx=W//2 + 230)
    draw_mixed(draw, (0, my+32), [("日旅程", True)], 46, fill=INK, bold=True, center_x=W//2 + 360)

    draw_mixed(draw, (0, 1230), [("癡LS Group · 東北雙馬拉松 2027", True)], 26, fill=INK, bold=False, center_x=W//2)

    img.save(OUT+"card-leave.png")

# ---------- Card 4: value 4 quadrant ----------
def card_value():
    img = Image.new("RGB", (W, H), CREAM)
    grad = v_gradient(W, H, SUN, (255, 230, 170), (255, 210, 130))
    img.paste(grad, (0, 0))
    draw = ImageDraw.Draw(img)

    draw_brand_header(img, draw, W//2)

    title = "點解要揀我哋？"
    center_text(draw, 175, "點解要揀我哋？", 60, fill=INK, is_cjk=True, bold=True)

    # 2x2 grid
    rows = 2
    cols = 2
    margin = 40
    gap = 28
    top_y = 290
    bottom_gap = 60
    total_gap = (cols-1)*gap
    cw = (W - 2*margin - total_gap)//cols
    total_h = H - top_y - 130
    ch = (total_h - (rows-1)*gap)//rows

    cells = [
        # (icon, title, desc, accent)
        ("icon-guarantee.png", "經驗幫手報名", "有經驗人仕\n陪你報名跟進", CORAL),
        ("icon-train.png", "東北JR Pass", "10日任搭\n玩盡東北", GRASS),
        ("icon-pb.png", "平坦全馬", "破PB 最佳路線", SKY),
        ("icon-gyutan.png", "美食溫泉", "牛舌 · 溫泉\n一路食住玩", SUN),
    ]

    for i, (icon, t, d, accent) in enumerate(cells):
        r, c = divmod(i, cols)
        x = margin + c*(cw+gap)
        y = top_y + r*(ch+gap)
        cx = x + cw//2
        # cell
        draw.rounded_rectangle([x, y, x+cw, y+ch], radius=30, fill=WHITE, outline=accent, width=5)
        # icon centered near top of cell
        ic_dia = int(cw*0.30)
        ic = rounded_icon_circle(icon, ic_dia, bg=WHITE, ring=accent, ring_w=6)
        paste_center(img, ic, (cx, y + int(ch*0.32)))
        # title
        center_text(draw, y + int(ch*0.52), t, 42, fill=INK, is_cjk=True, bold=True, cx=cx)
        # desc
        lines = d.split("\n")
        gray = tuple(int(v*0.55) for v in INK)
        if len(lines) == 1:
            center_text(draw, y + int(ch*0.78), lines[0], 30, fill=gray, is_cjk=True, bold=False, cx=cx)
        else:
            for j, ln in enumerate(lines):
                center_text(draw, y + int(ch*0.70) + j*40, ln, 28, fill=gray, is_cjk=True, bold=False, cx=cx)

    draw_mixed(draw, (0, 1265), [("癡LS Group · 東北雙馬拉松 2027", True)], 26, fill=INK, bold=False, center_x=W//2)
    img.save(OUT+"card-value.png")

# ---------- Card 5: friends ----------
def card_friends():
    img = Image.new("RGB", (W, H), CREAM)
    grad = v_gradient(W, H, (170, 220, 250), SKY, (120, 190, 235))
    img.paste(grad, (0, 0))
    draw = ImageDraw.Draw(img)

    draw_brand_header(img, draw, W//2)

    # Friends icon big
    friends = rounded_icon_circle("icon-friends.png", 360, bg=WHITE, ring=CORAL, ring_w=16)
    paste_center(img, friends, (W//2, 470))

    # Headline
    center_text(draw, 700, "帶埋朋友，", 72, fill=INK, is_cjk=True, bold=True)
    center_text(draw, 790, "送嘅唔係折扣", 56, fill=CORAL, is_cjk=True, bold=True)
    center_text(draw, 890, "係美好回憶", 84, fill=WHITE, is_cjk=True, bold=True)

    # Sub message
    sub = "一齊跑 · 一齊食 · 一齊笑"
    sub_w = text_w(draw, sub, 40, is_cjk=True, bold=True)
    draw.rounded_rectangle([(W-sub_w)//2-40, 960, (W+sub_w)//2+40, 960+70], radius=35, fill=INK)
    center_text(draw, 995, sub, 40, fill=SUN, is_cjk=True, bold=True)

    # Footer tagline
    center_text(draw, 1120, "「一個人跑得快，一班人跑得開心」", 34, fill=INK, is_cjk=True, bold=False)
    draw_mixed(draw, (0, 1230), [("癡LS Group · 東北雙馬拉松 2027", True)], 26, fill=WHITE, bold=False, center_x=W//2)
    img.save(OUT+"card-friends.png")

# ---------- Run all ----------
card_announce()
card_races()
card_leave()
card_value()
card_friends()

# Verify
import json
result = []
for f in sorted(os.listdir(OUT)):
    if f.endswith(".png"):
        path = os.path.join(OUT, f)
        result.append({"path": path, "size": os.path.getsize(path), "px": [W, H]})
print(json.dumps(result))
