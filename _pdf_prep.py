# -*- coding: utf-8 -*-
"""Generate 癡LS Group 東北雙馬拉松 2027 itinerary PDF."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------- Brand ----------
CORAL   = HexColor("#ff5a5f")
YELLOW  = HexColor("#ffc23c")
SKY     = HexColor("#39b7e8")
GREEN   = HexColor("#7cc954")
INK     = HexColor("#2b2b43")     # dark slate for text
SOFT    = HexColor("#5a5a75")
PALE_C  = HexColor("#ffecec")
PALE_Y  = HexColor("#fff6df")
PALE_S  = HexColor("#e8f6fd")
PALE_G  = HexColor("#f0fae9")
WHITE   = white

W, H = A4  # 595 x 842 pt

pdfmetrics.registerFont(TTFont("WQY", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", subfontIndex=0))

OUT = "/home/ubuntu/202705jpmarathon/docs/itinerary.pdf"

# ---------- Helpers ----------
def titlebar(c, x, y, w, h, fill, txt, fs=13, tc=WHITE, align="left"):
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, 4, stroke=0, fill=1)
    c.setFillColor(tc)
    c.setFont("WQY", fs)
    if align == "left":
        c.drawString(x + 10, y + h/2 - fs*0.36, txt)
    else:
        c.drawCentredString(x + w/2, y + h/2 - fs*0.36, txt)

def chip(c, x, y, w, fill, txt, fs=9, tc=WHITE):
    c.setFillColor(fill)
    c.roundRect(x, y, w, 14, 7, stroke=0, fill=1)
    c.setFillColor(tc)
    c.setFont("WQY", fs)
    c.drawCentredString(x + w/2, y + 4, txt)

def wrap(c, x, w, text, fs=9, leading=13, fill=SOFT, maxw=None):
    """Draw text wrapped by character count approximation (CJK)."""
    c.setFont("WQY", fs)
    maxw = maxw or w
    # estimate width using stringWidth
    from reportlab.pdfbase.pdfmetrics import stringWidth
    out_lines = []
    cur = ""
    for ch in text:
        if ch == "\n":
            out_lines.append(cur); cur = ""; continue
        if stringWidth(cur + ch, "WQY", fs) > maxw:
            out_lines.append(cur); cur = ch
        else:
            cur += ch
    if cur:
        out_lines.append(cur)
    y = y
    for ln in out_lines:
        c.setFillColor(fill)
        c.drawString(x, y, ln)
        y -= leading
    return y  # bottom after text

print("font registered")
c = canvas.Canvas(OUT, pagesize=A4)
c.save()
print("canvas svae ok")
