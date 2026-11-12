#!/usr/bin/env python3
"""Генератор схемы подключения ESP32 к мультипечи (SVG).

Запуск:  python3 tools/wiring.py docs/wiring.svg
Результат: чистый, самодостаточный SVG (без внешних ассетов).
"""
import sys

W, H = 1600, 1300

# --- палитра ---------------------------------------------------------------
BG = "#ffffff"
INK = "#0f172a"
MUTED = "#64748b"
CARD = "#ffffff"
CARD_ST = "#cbd5e1"
MAINS = "#dc2626"          # 230 В
MAINS_SOFT = "#fef2f2"
MAINS_BORDER = "#fecdd3"
SIG = "#2563eb"            # 3.3 В логика
GND = "#334155"            # земля
BOARD = "#0f172a"
BOARD_PAD = "#38bdf8"
WARN_BG = "#fffbeb"
WARN_BORDER = "#fcd34d"
WARN_INK = "#92400e"

out = []


def add(s):
    out.append(s)


def rect(x, y, w, h, fill=CARD, stroke=CARD_ST, rx=14, sw=2, dash=None, extra=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{sw}"{d} {extra}/>')


def text(x, y, s, size=13, fill=INK, weight="normal", anchor="start", family="sans", ls=None):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    esc = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if family == "mono":
        ff = "DejaVu Sans Mono, Consolas, monospace"
    else:
        ff = "DejaVu Sans, Segoe UI, Arial, sans-serif"
    add(f'<text x="{x}" y="{y}" font-family="{ff}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}"{a}{l}>{esc}</text>')


def line(x1, y1, x2, y2, color=SIG, w=2.4, dash=None, cap="round"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
        f'stroke-width="{w}" stroke-linecap="{cap}"{d}/>')


def path(d, color=SIG, w=2.4, dash=None, fill="none"):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{w}" '
        f'stroke-linecap="round" stroke-linejoin="round"{ds}/>')


def dot(x, y, color=SIG, r=4.5):
    add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')


def pad(x, y, label, color=SIG, anchor="middle", dx=0, dy=-10, size=12, bold=True):
    """Клемма на краю карточки/платы."""
    add(f'<circle cx="{x}" cy="{y}" r="5.5" fill="#ffffff" stroke="{color}" stroke-width="2.5"/>')
    if label:
        text(x + dx, y + dy, label, size, color, "bold" if bold else "normal", anchor)


def gnd_symbol(x, y, color=GND):
    line(x, y, x, y + 6, color, 2.4)
    line(x - 13, y + 6, x + 13, y + 6, color, 3)
    line(x - 8, y + 12, x + 8, y + 12, color, 3)
    line(x - 3.5, y + 18, x + 3.5, y + 18, color, 3)


def resistor_h(x, y, w=58, h=20, label="", color=SIG):
    rect(x, y - h / 2, w, h, fill="#ffffff", stroke=color, rx=4, sw=2.2)
    if label:
        text(x + w / 2, y - h / 2 - 7, label, 11.5, color, "bold", "middle")


def resistor_v(x, y, w=22, h=52, label="", color=SIG):
    rect(x - w / 2, y, w, h, fill="#ffffff", stroke=color, rx=4, sw=2.2)
    if label:
        text(x + w / 2 + 8, y + h / 2 + 4, label, 11.5, color, "bold")


def zigzag_h(x, y, w=70, amp=9, segs=6, color=MAINS):
    step = w / segs
    pts = [(x, y)]
    for i in range(segs):
        yy = y - amp if i % 2 == 0 else y + amp
        pts.append((x + step * (i + 0.5), yy))
        pts.append((x + step * (i + 1), y))
    d = "M " + " L ".join(f"{px:.1f} {py:.1f}" for px, py in pts)
    path(d, color, 2.4)


# ===========================================================================
add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
add(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

# --- заголовок -------------------------------------------------------------
text(72, 52, "Мультипечь на ESP32 — схема подключения", 30, INK, "bold")
text(72, 82, "Замена сгоревшей платы управления · ESPHome · SSR + реле + NTC + дверной интерлок",
     15, MUTED)
text(1528, 52, "github.com/kushnirdanik97/esp32-multioven", 13, SIG, "bold", "end")
text(1528, 74, "GPIO26 — ТЭН · GPIO27 — вентилятор · GPIO34 — NTC", 12, MUTED, anchor="end")

# --- зона 230 В -------------------------------------------------------------
rect(72, 100, 1456, 350, MAINS_SOFT, MAINS_BORDER, 18, 2)
text(96, 128, "СИЛОВАЯ ЧАСТЬ · ~230 В AC", 12.5, MAINS, "bold", ls="1.2")

# --- карточка: питание ------------------------------------------------------
rect(90, 140, 330, 290)
text(112, 170, "Питание 230 В → 5 В", 15, INK, "bold")
text(112, 192, "HLK-PM01 (или зарядка 5 В / 1 А)", 11.5, MUTED)

rect(112, 208, 176, 56, "#f8fafc", CARD_ST, 10, 2)
text(200, 232, "Ввод 230 В", 12.5, INK, "bold", "middle")
text(200, 250, "клеммник L · N · PE", 11, MUTED, anchor="middle")

rect(150, 296, 230, 70, "#f8fafc", CARD_ST, 10, 2)
text(265, 320, "HLK-PM01", 13, INK, "bold", "middle")
text(265, 338, "AC 230 В → DC 5 В, 1 А", 11, MUTED, anchor="middle")
text(265, 354, "гальваническая развязка", 10.5, MUTED, anchor="middle")

# ввод -> БП
line(200, 264, 200, 296, MAINS, 2.6)
line(250, 264, 250, 296, GND, 2.6)
text(192, 285, "L", 11, MAINS, "bold", "end")
text(258, 285, "N", 11, GND, "bold")
# PE на корпус
line(288, 264, 288, 380, "#16a34a", 2.6)
text(296, 372, "PE → корпус прибора и радиатор SSR", 10.5, "#15803d")
# выходы БП
line(200, 366, 200, 430, MAINS, 2.6)
line(250, 366, 250, 430, GND, 2.6)
pad(200, 430, "+5 В", MAINS, dy=-8, dx=-16)
pad(250, 430, "GND", GND, dy=-8, dx=18)

# --- карточка: ТЭН + SSR ----------------------------------------------------
rect(520, 140, 480, 290)
text(542, 170, "ТЭН + твердотельное реле (SSR)", 15, INK, "bold")
text(542, 192, "SSR-25DA / SSR-40DA (по току ТЭНа с запасом ×2)", 11.5, MUTED)

# клеммы карточки (левая грань) — 230 В
pad(520, 200, "L", MAINS, anchor="end", dx=-10, dy=4)
pad(520, 300, "+", SIG, anchor="end", dx=-10, dy=4)
pad(520, 340, "−", SIG, anchor="end", dx=-10, dy=4)

# SSR
rect(560, 250, 120, 80, "#f8fafc", MAINS, 10, 2.4)
text(620, 285, "SSR", 14, MAINS, "bold", "middle")
text(620, 305, "40 A / 3–32 В", 10.5, MUTED, anchor="middle")
pad(620, 250, "", MAINS)
pad(620, 330, "", MAINS)
pad(560, 275, "", SIG)
pad(560, 315, "", SIG)
text(626, 246, "1", 10, MAINS, "bold")
text(626, 344, "2", 10, MAINS, "bold")

# L -> SSR 1
path("M 520 200 L 620 200 L 620 250", MAINS, 2.6)
# управление +/- внутрь карточки
path("M 520 300 L 536 300 L 536 275 L 560 275", SIG, 2.2)
path("M 520 340 L 544 340 L 544 315 L 560 315", SIG, 2.2)
text(550, 268, "+", 10, SIG, "bold")
text(550, 331, "−", 10, SIG, "bold")

# SSR 2 -> ТЭН
path("M 620 330 L 620 372 L 800 372", MAINS, 2.6)
# ТЭН
rect(800, 345, 140, 54, "#f8fafc", MAINS, 10, 2.4)
zigzag_h(812, 372, 74, 8, 6, MAINS)
text(890, 364, "ТЭН", 12.5, MAINS, "bold")
text(890, 382, "2 кВт", 10.5, MUTED)
# ТЭН -> N
path("M 940 372 L 960 372 L 960 372", MAINS, 2.6)
path("M 870 399 L 870 404 L 520 404", GND, 2.6)
dot(870, 399, GND)
pad(520, 404, "N", GND, anchor="end", dx=-10, dy=4)

text(548, 424, "радиатор обязателен", 10.5, MAINS, "bold")
text(686, 424, "·  NC двери — в разрыв цепи «+»", 10.5, SIG)

# --- карточка: вентилятор + реле -------------------------------------------
rect(1040, 140, 488, 290)
text(1062, 170, "Вентилятор конвекции + реле", 15, INK, "bold")
text(1062, 192, "модуль реле 5 В (опто) или SRD-05VDC", 11.5, MUTED)

pad(1040, 215, "L", MAINS, anchor="end", dx=-10, dy=4)
pad(1040, 400, "N", GND, anchor="end", dx=-10, dy=4)
pad(1180, 430, "IN", SIG)

# контакт K1.1 в цепи L
path("M 1040 215 L 1120 215", MAINS, 2.6)
add('<circle cx="1132" cy="215" r="5" fill="none" stroke="#dc2626" stroke-width="2.4"/>')
add('<circle cx="1180" cy="215" r="5" fill="none" stroke="#dc2626" stroke-width="2.4"/>')
line(1136, 211, 1174, 197, MAINS, 2.6)
text(1156, 240, "K1.1", 10.5, MAINS, "bold", "middle")
path("M 1180 215 L 1345 215 L 1345 258", MAINS, 2.6)

# вентилятор
add('<circle cx="1345" cy="300" r="42" fill="#f8fafc" stroke="#dc2626" stroke-width="2.4"/>')
text(1345, 306, "M", 18, MAINS, "bold", "middle")
path("M 1345 258 L 1345 342 M 1303 300 L 1387 300", MAINS, 1.4, "6 6")
text(1396, 296, "вентилятор", 10.5, MUTED)
text(1396, 312, "230 В", 10.5, MUTED)
path("M 1345 342 L 1345 400 L 1040 400", GND, 2.6)

# катушка реле
rect(1085, 300, 205, 70, "#f8fafc", SIG, 10, 2.2)
text(1187, 326, "катушка реле 5 В", 12.5, SIG, "bold", "middle")
text(1187, 346, "+5 В и GND — от БП", 10, MUTED, anchor="middle")
path("M 1187 300 L 1187 228", SIG, 1.6, "4 5")
path("M 1180 370 L 1180 430", SIG, 2.2)

# ===========================================================================
# --- зона низковольтная -----------------------------------------------------
rect(72, 470, 1456, 620, "#f8fafc", "#e2e8f0", 18, 2)
text(96, 498, "НИЗКОВОЛЬТНАЯ ЧАСТЬ · 3.3 / 5 В", 12.5, SIG, "bold", ls="1.2")

# --- плата ESP32 ------------------------------------------------------------
rect(90, 560, 380, 450, BOARD, "#1e293b", 18, 2)
text(112, 600, "ESP32 DevKit V1", 20, "#f8fafc", "bold")
text(112, 624, "ESP32-WROOM-32 · логика 3.3 В", 11.5, "#94a3b8")
rect(112, 646, 336, 1, "#1e293b", "#1e293b", 0, 1)
text(112, 676, "USB — питание/прошивка", 11, "#94a3b8")
text(112, 700, "BOOT + EN — вход в загрузчик", 11, "#94a3b8")
text(112, 972, "5 В подавать на VIN / 5V,", 11, "#fbbf24")
text(112, 990, "НЕ на пин 3V3", 11, "#fbbf24")

# верхние пины
for x, lbl in [(200, "5V"), (250, "GND"), (330, "26"), (390, "27")]:
    add(f'<rect x="{x-11}" y="548" width="22" height="14" rx="3" fill="{BOARD_PAD}"/>')
    text(x, 586, lbl, 12.5, "#e2e8f0", "bold", "middle")
# правые пины
for y, lbl in [(620, "3V3"), (660, "34"), (825, "32"), (950, "33")]:
    add(f'<rect x="458" y="{y-11}" width="14" height="22" rx="3" fill="{BOARD_PAD}"/>')
    text(446, y + 5, lbl, 12.5, "#e2e8f0", "bold", "end")

# --- коридоры от ESP32 к силовой части -------------------------------------
# 5V и GND от блока питания (прямые вертикали)
path("M 200 430 L 200 548", MAINS, 2.6)
path("M 250 430 L 250 548", GND, 2.6)

# GPIO26 -> NC двери -> 1к -> SSR «+»
path("M 330 548 L 330 447 L 470 447 L 470 300 L 520 300", SIG, 2.4)
# NC контакт двери на линии 447
line(378, 447, 388, 447, SIG, 2.4)
add('<circle cx="388" cy="447" r="4" fill="none" stroke="#2563eb" stroke-width="2.2"/>')
add('<circle cx="418" cy="447" r="4" fill="none" stroke="#2563eb" stroke-width="2.2"/>')
line(391, 444, 415, 432, SIG, 2.4)
text(403, 474, "SQ1 дверь, NC — разрыв цепи «+»", 10.5, SIG, "bold", "middle")
# 1 кОм на вертикали x=470 (между 380 и 410)
resistor_v(470, 372, 22, 40)
text(452, 396, "1 кОм", 10.5, SIG, "bold", "end")

# GND -> SSR «−»
path("M 250 548 L 250 485 L 480 485 L 480 340 L 520 340", GND, 2.4)
dot(480, 485, GND)

# GPIO27 -> IN реле
path("M 390 548 L 390 528 L 1180 528 L 1180 430", SIG, 2.4)

# правые пины -> карточки
path("M 470 620 L 560 620", SIG, 2.4)
path("M 470 660 L 560 660", SIG, 2.4)
path("M 470 825 L 500 825 L 500 895 L 560 895", SIG, 2.4)
path("M 470 950 L 520 950 L 520 1025 L 560 1025", SIG, 2.4)

# --- карточка: делитель NTC -------------------------------------------------
rect(560, 600, 440, 200)
text(582, 630, "Делитель NTC — датчик духовки", 15, INK, "bold")
text(582, 650, "ADC1_CH6 (GPIO34) · 12 дБ · медиана ×5", 11, MUTED)
pad(560, 620, "", SIG)
pad(560, 660, "", SIG)
text(572, 616, "3V3", 10, SIG, "bold")
text(572, 682, "34", 10, SIG, "bold")

path("M 560 620 L 700 620 L 700 640", SIG, 2.2)
resistor_v(700, 640, 24, 44, "R1 120 кОм")
line(700, 684, 700, 700, SIG, 2.2)
dot(700, 700, SIG)
path("M 700 700 L 632 700 L 632 660 L 560 660", SIG, 2.2)
path("M 700 700 L 700 712", GND, 2.2)
resistor_v(700, 712, 24, 44, "NTC 130 кОм / 20 °C", SIG)
line(700, 756, 700, 768, GND, 2.2)
gnd_symbol(700, 768, GND)
text(582, 790, "B = 3950 · номиналы R1 и NTC — под свой датчик (multioven.yaml)", 10.5, MUTED)

# --- карточка: дверь (сигнал) ----------------------------------------------
rect(560, 830, 440, 110)
text(582, 860, "Датчик двери (сигнал)", 15, INK, "bold")
text(582, 880, "GPIO32 · внутренний pull-up", 11, MUTED)
pad(560, 895, "", SIG)
path("M 560 895 L 620 895", SIG, 2.2)
add('<circle cx="624" cy="895" r="4.5" fill="none" stroke="#2563eb" stroke-width="2.2"/>')
add('<circle cx="672" cy="895" r="4.5" fill="none" stroke="#2563eb" stroke-width="2.2"/>')
line(628, 891, 668, 877, SIG, 2.4)
text(648, 920, "дверь закрыта = замкнут на GND", 10.5, MUTED, anchor="middle")
path("M 672 895 L 730 895 L 730 906", GND, 2.2)
gnd_symbol(730, 906, GND)

# --- карточка: бузер --------------------------------------------------------
rect(560, 960, 440, 110)
text(582, 990, "Пассивный бузер", 15, INK, "bold")
text(582, 1010, "GPIO33 · LEDC/RTTTL (сигналы готовности)", 11, MUTED)
pad(560, 1025, "", SIG)
path("M 560 1025 L 612 1025", SIG, 2.2)
resistor_h(612, 1025, 44, 18, "100 Ω")
path("M 656 1025 L 700 1025", SIG, 2.2)
add('<path d="M 700 1006 L 700 1044 L 726 1032 L 726 1018 Z" fill="#f8fafc" stroke="#2563eb" stroke-width="2.2"/>')
path("M 734 1014 Q 750 1025 734 1036", SIG, 2.2)
text(756, 1030, "бузер", 10.5, MUTED)
path("M 700 1044 L 700 1050", GND, 2.2)
path("M 726 1050 L 700 1050", GND, 2.2)
gnd_symbol(726, 1050, GND)

# --- карточка: распиновка ---------------------------------------------------
rect(1040, 600, 488, 470)
text(1062, 632, "Распиновка и назначение", 15, INK, "bold")
line(1062, 646, 1506, 646, "#e2e8f0", 1.6)

rows = [
    ("5V / VIN", "питание от HLK-PM01 (5 В, ≥0.7 А)", MAINS),
    ("GND", "общая земля: БП, SSR «−», реле", GND),
    ("3V3", "питание делителя NTC", SIG),
    ("GPIO26", "SSR «+» — ШИМ нагрева (через NC двери)", SIG),
    ("GPIO27", "IN реле вентилятора", SIG),
    ("GPIO34", "ADC1 — делитель NTC (только вход)", SIG),
    ("GPIO32", "геркон/концевик двери (pull-up)", SIG),
    ("GPIO33", "пассивный бузер (LEDC)", SIG),
]
y = 674
for name, desc, col in rows:
    add(f'<rect x="1062" y="{y-12}" width="86" height="22" rx="6" fill="#eef2ff"/>')
    text(1105, y + 3, name, 11.5, col, "bold", "middle")
    text(1160, y + 3, desc, 12, INK)
    y += 32

text(1062, 948, "Не использовать GPIO0/2/5/12/15 (strapping) —", 11, MUTED)
text(1062, 966, "при старте дают ложный уровень на выходе.", 11, MUTED)

# легенда
y = 1002
for col, dash, lbl in [(MAINS, None, "~230 В"), (SIG, None, "сигнал 3.3 В"),
                       (GND, None, "GND"), (SIG, "4 5", "мех. связь")]:
    line(1062, y, 1102, y, col, 3, dash)
    text(1112, y + 4, lbl, 11.5, MUTED)
    y += 22

# ===========================================================================
# --- предупреждения ---------------------------------------------------------
rect(72, 1112, 1456, 156, WARN_BG, WARN_BORDER, 18, 2)
text(96, 1144, "⚠  БЕЗОПАСНОСТЬ", 14, WARN_INK, "bold", ls="1.2")
text(96, 1172, "230 В опасно для жизни. Все работы — только обесточив прибор; силовую часть монтирует тот, кто умеет.",
     12.5, INK)
text(96, 1196, "NC-контакт двери ставится ФИЗИЧЕСКИ в разрыв цепи управления SSR: программный интерлок — вторая линия защиты, не замена.",
     12.5, INK)
text(96, 1220, "ТЭН коммутируется только через SSR с радиатором и запасом по току ×2; корпус прибора и радиатор — на PE.",
     12.5, INK)
text(96, 1244, "Сверяйте распиновку своей платы: у клонов DevKit порядок пинов отличается; 5 В — на VIN, не на 3V3.",
     12.5, INK)

add("</svg>")

sys.stdout.write("")  # noqa
target = sys.argv[1] if len(sys.argv) > 1 else "wiring.svg"
with open(target, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"OK {target} ({len(chr(10).join(out))} bytes)")
