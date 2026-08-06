# -*- coding: utf-8 -*-
"""Generate 癡LS Group 東北雙馬拉松 2027 itinerary PDF (A4, bright vibrant brand design)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth

# ---------- Brand palette ----------
CORAL  = HexColor("#ff5a5f")
YELLOW = HexColor("#ffc23c")
SKY    = HexColor("#39b7e8")
GREEN  = HexColor("#7cc954")
INK    = HexColor("#2b2b43")
SOFT   = HexColor("#55556e")
PALE_C = HexColor("#ffecec")
PALE_Y = HexColor("#fff6df")
PALE_S = HexColor("#e8f6fd")
PALE_G = HexColor("#f0fae9")
WHITEC = HexColor("#ffffff")

W, H = A4  # 595 x 842 pt
M = 38  # margin

pdfmetrics.registerFont(TTFont("WQY", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", subfontIndex=0))

OUT = "/home/ubuntu/202705jpmarathon/docs/itinerary.pdf"
c = canvas.Canvas(OUT, pagesize=A4)

PAGE = 0

def newpage():
    global PAGE
    c.showPage()
    PAGE += 1

def titlebar(c, x, y, w, h, fill, txt, fs=13, tc=WHITEC):
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, 6, stroke=0, fill=1)
    c.setFillColor(tc)
    c.setFont("WQY", fs)
    c.drawString(x + 12, y + h/2 - fs*0.36, txt)

def wrap_lines(text, fs, maxw):
    """Wrap text into lines by character width (CJK-aware via stringWidth)."""
    lines = []
    for para in text.split("\n"):
        cur = ""
        for ch in para:
            if stringWidth(cur + ch, "WQY", fs) > maxw:
                lines.append(cur)
                cur = ch
            else:
                cur += ch
        if cur:
            lines.append(cur)
    return lines

def bullet_block(y, text, color, fs=10.5, leading=15, x=M, indent=24, maxw=None):
    maxw = maxw or (W - 2*M - indent - 8)
    lines = wrap_lines(text, fs, maxw)
    for ln in lines:
        c.setFillColor(color); c.circle(x+10, y+3, 2.2, stroke=0, fill=1)
        c.setFillColor(INK); c.setFont("WQY", fs)
        c.drawString(x+indent, y, ln)
        y -= leading
    return y

def footer(pagenum=None):
    c.setFillColor(CORAL)
    c.rect(0, 0, W, 10, stroke=0, fill=1)
    c.setFillColor(WHITEC)
    c.setFont("WQY", 8)
    c.drawString(M, 3.5, "癡LS Group・東北雙馬拉松挑戰之旅 2027")
    c.drawRightString(W - M, 3.5, "頁 %d" % (pagenum or PAGE))

# =========================================================
# COVER PAGE
# =========================================================
# big color bands
c.setFillColor(CORAL); c.rect(0, H-180, W, 180, stroke=0, fill=1)
c.setFillColor(YELLOW); c.rect(0, H-190, W, 10, stroke=0, fill=1)
# decorative circles
c.setStrokeColor(WHITEC); c.setLineWidth(2)
c.setFillColor(HexColor("#ff8574")); c.circle(W-70, H-70, 34, stroke=0, fill=1)
c.setFillColor(YELLOW); c.circle(70, H-150, 20, stroke=0, fill=1)

# brand
c.setFillColor(WHITEC); c.setFont("WQY", 22)
c.drawString(M, H-64, "癡LS Group")

c.setFillColor(YELLOW); c.setFont("WQY", 11)
c.drawString(M, H-88, "跑馬旅行團 · 2027")

# main title
c.setFillColor(WHITEC); c.setFont("WQY", 34)
c.drawString(M, H-160, "東北雙馬拉松")
c.drawString(M, H-205, "挑戰之旅 2027")

# subtitle block on pale panel
c.setFillColor(PALE_C); c.roundRect(M, H-330, W-2*M, 92, 10, stroke=0, fill=1)
c.setFillColor(CORAL); c.setFont("WQY", 17)
c.drawString(M+18, H-270, "仙台半馬 × 岩手奥州きらめき全馬")
c.setFillColor(INK); c.setFont("WQY", 11)
c.drawString(M+18, H-296, "五月中旬 ・ 佛誕夾中間 ・ 請4放9 ・ 東北 JR Pass 10日任搭")

# key date chips
chip_r = M; chip_w = (W-2*M - 12)/2
# row 1
c.setFillColor(SKY); c.roundRect(M, H-378, chip_w, 40, 8, stroke=0, fill=1)
c.setFillColor(WHITEC); c.setFont("WQY", 17)
c.drawCentredString(M+chip_w/2, H-366, "5/8 – 5/16")
c.setFillColor(INK); c.setFont("WQY", 10)
c.drawCentredString(M+chip_w/2, H-384, "主要行程 9 日（推薦 +1 日=10 日）")

c.setFillColor(GREEN); c.roundRect(M+chip_w+12, H-378, chip_w, 40, 8, stroke=0, fill=1)
c.setFillColor(WHITEC); c.setFont("WQY", 17)
c.drawCentredString(M+chip_w+12+chip_w/2, H-366, "5/9 ・ 5/16")
c.setFillColor(INK); c.setFont("WQY", 10)
c.drawCentredString(M+chip_w+12+chip_w/2, H-384, "仙台半馬 ／ 奥州全馬（兩個星期日）")

# row 2
c.setFillColor(YELLOW); c.roundRect(M, H-428, chip_w, 40, 8, stroke=0, fill=1)
c.setFillColor(WHITEC); c.setFont("WQY", 17)
c.drawCentredString(M+chip_w/2, H-416, "5/13 佛誕")
c.setFillColor(INK); c.setFont("WQY", 10)
c.drawCentredString(M+chip_w/2, H-434, "紅日放假・全日休腳恢復")

c.setFillColor(CORAL); c.roundRect(M+chip_w+12, H-428, chip_w, 40, 8, stroke=0, fill=1)
c.setFillColor(WHITEC); c.setFont("WQY", 17)
c.drawCentredString(M+chip_w+12+chip_w/2, H-416, "請4放9 / 放10")
c.setFillColor(INK); c.setFont("WQY", 10)
c.drawCentredString(M+chip_w+12+chip_w/2, H-434, "請 5/10-12・14 ／ +5/17")

# bottom accent
c.setFillColor(HexColor("#2b2b43"))
c.roundRect(M, H-500, W-2*M, 42, 8, stroke=0, fill=1)
c.setFillColor(WHITEC); c.setFont("WQY", 12)
c.drawCentredString(W/2, H-483, "一個假期 ・ 兩場馬拉松 ・ 一次上晒兩面獎牌")

footer(1)
newpage()

# =========================================================
# ITINERARY PAGES  (Day 1 .. Day 10)
# =========================================================
days = [
    ("DAY 1", "5/8（六）", "香港 → 仙台・報到", CORAL,
     ["UO891 HKG 08:15 → SDJ 13:30（香港快運直航，約 5 小時 15 分）",
      "仙台機場 → 仙台駅（機場快線約 25 分鐘），酒店 check-in",
      "下午：仙台半馬 報到 / 領取號碼布（會場：弘進パーク仙台，賽前一日必須領取）",
      "夜晚：仙台名物「炭燒牛舌」＋毛豆麻糬（ずんだ），早啲瞓儲體力",
      "宿：仙台駅周邊（東横INN 仙台東口 / 西口中央）—— 賽前週六要提早訂房"]),
    ("DAY 2", "5/9（日）", "仙台國際半馬 21.0975km", SKY,
     ["10:05 第 1 波浪（精英／一般I）｜10:15 第 2 波浪（一般II）起跑，限時 2:30",
      "賽道：弘進パーク仙台 → 定禅寺通（「杜之都」林蔭大道）→ 卸町 → 折返",
      "完賽：仙台城跡 / 瑞鳳殿打卡，大啖牛舌慶功",
      "跑法策略：呢場當「B 賽事」控制配速（當高質素 long run），主力留返下星期日全馬",
      "宿：仙台"]),
    ("DAY 3", "5/10（一）", "松島・恢復遊", GREEN,
     ["松島（日本三景）：遊船 + 瑞巌寺 + 五大堂",
      "輕鬆恢復行，唔好劇烈運動",
      "宿：仙台 或 轉住松島溫泉"]),
    ("DAY 4", "5/11（二）", "平泉世界遺產", YELLOW,
     ["平泉 中尊寺・金色堂（UNESCO）、毛越寺、嚴美溪",
      "仙台 → 平泉 新幹線 / 在來線（JR Pass 全包）",
      "宿：一ノ関 或 盛岡"]),
    ("DAY 5", "5/12（三）", "盛岡・花卷溫泉", CORAL,
     ["盛岡：盛岡城跡公園、盛岡冷麵、前澤牛",
      "下午：花卷溫泉 泡湯，為全馬前深度恢復",
      "宿：花卷溫泉 或 盛岡"]),
    ("DAY 6", "5/13（四）", "佛誕・全日恢復", SKY,
     ["紅日放假 —— 全日休腳：溫泉、按摩、輕食補碳",
      "大谷翔平出身地周邊走走（奥州 / 一関）",
      "宿：一ノ関 或 水沢江刺 附近"]),
    ("DAY 7", "5/14（五）", "轉戰奥州・補碳", GREEN,
     ["移動到 奥州市（一ノ関 / 水沢江刺），酒店 check-in",
      "最後補碳日：多食飯 / 麵，儲 glycogen",
      "宿：奥州 / 一関"]),
    ("DAY 8", "5/15（六）", "奥州全馬報到", YELLOW,
     ["奥州きらめき全馬 報到 / 領號碼布（會場：奥州市江刺総合支所）",
      "賽前 briefing、早瞓",
      "宿：奥州 / 一関（步行 / 短途到會場最佳）"]),
    ("DAY 9", "5/16（日）", "奥州きらめき全馬 42.195km", CORAL,
     ["8:30 起跑，限時 6:00（6 個關門點）",
      "賽道：奥州市江刺総合支所出發，高低差僅 20m —— 全平緩賽道，破 PB 絕佳",
      "完賽：慶功、前澤牛慶祝、花卷溫泉恢復",
      "宿：奥州 / 仙台"]),
    ("DAY 10", "5/17（一）", "仙台 → 香港・返港", SKY,
     ["朝早：秋保温泉 / 仙台市內慢逛",
      "SDJ → HKG 返港 —— 跑完全馬休息足一日先飛"]),
]

day_header_h = 52
row_gap = 8

for (label, date, title, color, lines) in days:
    # header banner
    c.setFillColor(color); c.roundRect(M, H-day_header_h-M+8, W-2*M, day_header_h, 8, stroke=0, fill=1)
    c.setFillColor(WHITEC); c.setFont("WQY", 20)
    c.drawString(M+16, H-day_header_h-M+22, label)
    c.setFillColor(WHITEC); c.setFont("WQY", 18)
    c.drawString(M+130, H-day_header_h-M+22, date)
    c.setFillColor(WHITEC); c.setFont("WQY", 22)
    c.drawString(M+232, H-day_header_h-M+22, title)
    # decorative
    c.setFillColor(WHITEC); c.circle(M+W-2*M-22, H-44, 9, stroke=0, fill=1)

    y = H - day_header_h - M - 34
    c.setFillColor(color); c.setFont("WQY", 12)
    c.drawString(M+4, y, "▪")
    c.setFillColor(SOFT); c.setFont("WQY", 11)
    c.drawString(M+16, y, "行程重點")
    y -= 20

    for line in lines:
        # bullet (wrapped)
        y = bullet_block(y, line, color, fs=11, leading=20) - 3

    # bottom tip banner
    tip = {"DAY 1": "編號布一定要 5/8 當日攞，過日無得攞！",
           "DAY 2": "半馬當「B 賽事」，唔好搏，maintain 住節奏就得。",
           "DAY 6": "佛誕紅日，全日唔好郁 —— 為全馬儲滿 glycogen。",
           "DAY 7": "今日係煤滿 glycogen 最後機會，食多啲睇怕唔會錯。",
           "DAY 9": "全平緩賽道，破 PB 最佳時機！下午慶功唔好客氣。"}.get(label)
    if tip:
        c.setFillColor(PALE_G if color==GREEN else PALE_Y if color==YELLOW else PALE_S if color==SKY else PALE_C)
        c.roundRect(M, y-6, W-2*M, 30, 6, stroke=0, fill=1)
        c.setFillColor(color); c.circle(M+14, y+9, 3, stroke=0, fill=1)
        c.setFillColor(INK); c.setFont("WQY", 10)
        c.drawString(M+26, y+7, "提示：")
        c.setFillColor(SOFT); c.setFont("WQY", 10)
        c.drawString(M+66, y+7, tip)
    footer()
    newpage()

# =========================================================
# 注意事項 PAGE
# =========================================================
def section(y, title, color, bullets):
    titlebar(c, M, y, W-2*M, 30, color, "  " + title, fs=13)
    y -= 26
    for b in bullets:
        y = bullet_block(y, b, color)
        y -= 6
    return y - 6

# 注意事項 page 1
titlebar(c, M, H-M-30, W-2*M, 34, CORAL, "  馬拉松相關注意事項", fs=15)
y = H-M-80

y = section(y, "① 半馬＋全馬相隔 7 日（最重要！）", CORAL,
    ["5/9 半馬 + 5/16 全馬 = 背靠背 double challenge",
     "建議：仙台半馬用控制配速跑（當高質素 long run / tempo，唔好搏 PB），主力放晒喺奥州全馬",
     "中間一星期：減量（taper）+ 恢復，只做輕鬆跑 / 完全休息，唔好加量"])

y = section(y, "② 賽事報名（有經驗人仕幫手）", YELLOW,
    ["仙台半馬：經 runnet 報名，報名期約 2026 年 12 月；需提交達標紀錄（一般I：半馬<2:00 或全馬<4:30；一般II：能 2:30 內完成半馬）；參賽費 ¥8,000",
     "奥州きらめき全馬：經 RUNNET / 郵便，報名期約 2026 年 11 月底 – 2027 年 2 月中；全馬 ¥10,000；定員 3,000 人",
     "唔保證名額、唔代辦 —— 但有有經驗人仕陪你報名、跟進流程"])

y = section(y, "③ 號碼布領取（一定係賽前一日）", SKY,
    ["仙台半馬：5/8（六）會場領取",
     "奥州全馬：5/15（六）會場領取（無郵寄）",
     "所以要預留 Day 1 / Day 8 下午去報到"])

y = section(y, "④ 住宿要早訂", GREEN,
    ["賽前週六（5/9、5/16 前一晚）大城市 / 賽事區酒店緊張（東横INN 等都會爆滿）",
     "一確認報名成功就訂，尤其仙台駅周邊同奥州 / 一関"])
footer()
newpage()

# 注意事項 page 2
titlebar(c, M, H-M-30, W-2*M, 34, SKY, "  馬拉松相關注意事項（續）", fs=15)
y = H-M-80

y = section(y, "⑤ 交通（JR Pass 全包）", SKY,
    ["仙台 → 一ノ関：新幹線約 45 分鐘",
     "奥州會場：最近站 水沢江刺（JR 東北本線）；賽日有免費穿梭巴士",
     "東北 JR Pass 10日 ¥50,000：5/8–5/17 連續使用，東北新幹線 + 在來線任搭，夾埋三陸鐵道，回本無難度"])

y = section(y, "⑥ 天氣 ＆ 裝備", YELLOW,
    ["5 月東北：日間約 15–22°C，全馬可能偏暖 —— 帶防曬、帽子、補給，注意補水",
     "半馬全馬都係官方補給，但可自備能量膠",
     "跑鞋：兩場共用一對比賽鞋就得（相隔 7 日夠回復）"])

y = section(y, "⑦ 全馬後恢復", GREEN,
    ["唔好即日飛 —— 跑完 42km 之後搭長途機好辛苦，休息一晚（Day 10）先走",
     "花卷溫泉 / 秋保溫泉 泡湯、按摩、食牛"])

y = section(y, "⑧ 額外彩蛋：東京馬拉松 2027 抽籤", CORAL,
    ["仙台半馬係 RUN as ONE – Tokyo Marathon 2027 提攜大會 —— 完賽者可申請抽 3 個東京馬拉松 2027 出走名額",
     "參加 package 等於多一個「衝六大」嘅機會"])

# bottom note band
c.setFillColor(HexColor("#ffcf33"))
c.roundRect(M, 60, W-2*M, 30, 6, stroke=0, fill=1)
c.setFillColor(HexColor("#5a4300")); c.setFont("WQY", 10.5)
c.drawCentredString(W/2, 72, "價格會隨季節／訂房時機浮動，一切以實際報價為準。")
footer()
newpage()

# =========================================================
# 費用估算 TABLE PAGE
# =========================================================
titlebar(c, M, H-M-30, W-2*M, 34, CORAL, "  費用估算（每人・參考）", fs=15)
c.setFillColor(SOFT); c.setFont("WQY", 10.5)
c.drawString(M, H-M-58, "以下為建議開支參考，最終以實際詢價／匯率為準。")

rows = [
    ("機票 HKG ⇄ SDJ（HK Express 直航）", "~2,500 – 3,500"),
    ("東北 JR Pass 10日", "~2,630"),
    ("住宿 8–9 晚（經濟酒店 / 溫泉旅館）", "~4,500 – 6,000"),
    ("仙台半馬參賽費（¥8,000）", "~420"),
    ("奥州全馬參賽費（¥10,000）", "~530"),
    ("膳食 / 雜費", "~2,500 – 3,500"),
]

y = H-M-96
rowh = 34
for i, (item, cost) in enumerate(rows):
    fillcol = [PALE_C, PALE_Y, PALE_S, PALE_G][i % 4]
    c.setFillColor(fillcol)
    c.roundRect(M, y-rowh, W-2*M, rowh, 6, stroke=0, fill=1)
    # left edge accent
    c.setFillColor([CORAL, YELLOW, SKY, GREEN][i % 4])
    c.rect(M, y-rowh, 5, rowh, stroke=0, fill=1)
    c.setFillColor(INK); c.setFont("WQY", 11)
    c.drawString(M+18, y-rowh+11, item)
    c.setFillColor([CORAL, YELLOW, SKY, GREEN][i % 4]); c.setFont("WQY", 12)
    c.drawRightString(W-M-18, y-rowh+11, "HKD " + cost)
    y -= rowh + 6

# total
c.setFillColor(INK)
c.roundRect(M, y-52, W-2*M, 52, 8, stroke=0, fill=1)
c.setFillColor(WHITEC); c.setFont("WQY", 14)
c.drawString(M+18, y-30, "合計（每人・參考）")
c.setFillColor(YELLOW); c.setFont("WQY", 20)
c.drawRightString(W-M-18, y-30, "HKD ~13,000 – 16,500")

c.setFillColor(SOFT); c.setFont("WQY", 9.5)
c.drawString(M, y-70, "※ 跑手視乎季節／訂房時機價格浮動；價錢以實際報價為準。")

footer()
newpage()

c.save()
print("PDF written to", OUT)

import os
print("SIZE:", os.path.getsize(OUT))
