# -*- coding: utf-8 -*-
"""Generate 癡LS Group 東北雙馬拉松 2027 宣傳文案單張 PDF (A4)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

CORAL  = HexColor("#c05f3c")
FOREST = HexColor("#3e5c4b")
INK    = HexColor("#2b2a26")
MUTED  = HexColor("#6e6a61")
LINE   = HexColor("#e6e1d8")
PAPER  = HexColor("#f7f4ef")

W, H = A4
M = 22 * mm

pdfmetrics.registerFont(TTFont("WQY", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("WQYB", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", subfontIndex=1))

OUT = "/home/ubuntu/202705jpmarathon/downloads/promo-copy.pdf"
c = canvas.Canvas(OUT, pagesize=A4)
c.setFillColor(PAPER)
c.rect(0, 0, W, H, fill=1, stroke=0)

y = H - 24 * mm
c.setFillColor(FOREST)
c.setFont("WQYB", 20)
c.drawString(M, y, "東北雙馬拉松挑戰之旅 2027 — 宣傳文案")
y -= 9 * mm
c.setFillColor(MUTED)
c.setFont("WQY", 11)
c.drawString(M, y, "仙台國際半馬 (5/9) × 岩手奧州閃耀馬拉松 (5/16) ｜ 請4放9 ｜ 東北 JR Pass 10日")
y -= 14 * mm

def section(title, lines, y):
    c.setFillColor(CORAL)
    c.setFont("WQYB", 13)
    c.drawString(M, y, title)
    y -= 7 * mm
    c.setFillColor(INK)
    c.setFont("WQY", 10.5)
    for ln in lines:
        c.drawString(M + 2 * mm, y, ln)
        y -= 5.2 * mm
    return y - 5 * mm

y = section("主口號", ["「一個假期，兩場馬拉松」", "半馬起跑，全馬征服。東北櫻風跑旅，請4放9。"], y)
y = section("支援口號", ["- 請4日假，玩足9日", "- 一張 Pass，玩透東北", "- 全馬破PB好時機（奥州平坦賽道）",
    "- 跑完泡湯食前澤牛，人生無憾", "- 跑入大谷翔平嘅故鄉", "- 佛誕放假，夾喺兩場馬拉松中間"], y)
y = section("賣點（Why Us）", ["- 一程玩兩場：半馬+全馬一次過滿足", "- 有經驗人仕幫手報名，唔使自己盲摸摸",
    "- 佛誕夾中間：請4放9，慳到盡", "- 東北 Pass 10日：松島、平泉、盛岡、花卷溫泉任你去",
    "- 平坦全馬：高低差僅20m，破PB好時機", "- 賽前報到、交通、住宿——我哋搞掂晒"], y)
y = section("報名資料", ["- 仙台半馬：報名期約 2026年12月，經 runnet，參賽費 ¥8,000，需達標紀錄",
    "- 奥州全馬：報名期約 2026年11月底–2027年2月中，經 RUNNET，全馬 ¥10,000，定員3,000人",
    "- 唔保證名額、唔代辦——但有經驗人仕陪你報名、跟進流程"], y)

c.setStrokeColor(LINE)
c.setLineWidth(0.8)
c.line(M, 22 * mm, W - M, 22 * mm)
c.setFillColor(MUTED)
c.setFont("WQY", 9)
c.drawCentredString(W / 2, 16 * mm, "癡LS Group ｜ 你負責跑，其餘我哋搞掂。 ｜ 帶埋朋友一齊跑，送嘅係最美好嘅回憶。")

c.save()
print("OK:", OUT)
