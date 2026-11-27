#!/usr/bin/env python3
"""Build the hospitality IoT Security Kit overview PDF.

Rebuild from the project root:

    .venv-pdf/bin/python scripts/build_overview_pdf.py

Figures are written to figures/. The PDF is written next to the source note.
Commercial charts use only the price ranges stated in the overview.
The incident plot is a labeled schematic of Figure 1, not a captured trace.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fontTools.ttLib import TTCollection
from matplotlib import font_manager
from PIL import Image
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
FONT_DIR = FIG / "fonts"
OUT = ROOT / "IoT-Security-Kit-Against-Sleeper-AI-Agents.pdf"

W, H = A4
LEFT = 36
RIGHT = W - 36
WIDTH = RIGHT - LEFT
BOTTOM = 46

NAVY = HexColor("#102433")
NAVY_2 = HexColor("#17344A")
INK = HexColor("#1C1917")
MUTED = HexColor("#5C564F")
RULE = HexColor("#DDD6CC")
PAGE = HexColor("#F3F0EA")
CARD = white
CREAM = HexColor("#F6F1E8")
TEAL = HexColor("#145E52")
TEAL_LINE = HexColor("#1F7A6B")
TEAL_SOFT = HexColor("#E5F2EE")
AMBER = HexColor("#7A4E1D")
AMBER_LINE = HexColor("#B08448")
AMBER_SOFT = HexColor("#F8F1E6")
CRIMSON = HexColor("#8C2F28")
CRIMSON_LINE = HexColor("#C4473C")
CRIMSON_SOFT = HexColor("#F8EBE8")
GREEN_LINE = HexColor("#2F8F62")

S = {}


def extract_fonts() -> None:
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    faces = {
        "/System/Library/Fonts/Avenir Next.ttc": {
            7: "Avenir.ttf",
            5: "Avenir-Medium.ttf",
            2: "Avenir-Demi.ttf",
            0: "Avenir-Bold.ttf",
            8: "Avenir-Heavy.ttf",
        },
        "/System/Library/Fonts/Supplemental/Charter.ttc": {
            0: "Charter.ttf",
            1: "Charter-Italic.ttf",
            3: "Charter-Bold.ttf",
        },
    }
    for src, mapping in faces.items():
        collection = TTCollection(src)
        for index, name in mapping.items():
            dest = FONT_DIR / name
            if not dest.exists():
                collection.fonts[index].save(str(dest))

    pdfmetrics.registerFont(TTFont("Avenir", str(FONT_DIR / "Avenir.ttf")))
    pdfmetrics.registerFont(TTFont("Avenir-Medium", str(FONT_DIR / "Avenir-Medium.ttf")))
    pdfmetrics.registerFont(TTFont("Avenir-Demi", str(FONT_DIR / "Avenir-Demi.ttf")))
    pdfmetrics.registerFont(TTFont("Avenir-Bold", str(FONT_DIR / "Avenir-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Avenir-Heavy", str(FONT_DIR / "Avenir-Heavy.ttf")))
    pdfmetrics.registerFont(TTFont("Charter", str(FONT_DIR / "Charter.ttf")))
    pdfmetrics.registerFont(TTFont("Charter-Italic", str(FONT_DIR / "Charter-Italic.ttf")))
    pdfmetrics.registerFont(TTFont("Charter-Bold", str(FONT_DIR / "Charter-Bold.ttf")))
    pdfmetrics.registerFontFamily(
        "Charter",
        normal="Charter",
        bold="Charter-Bold",
        italic="Charter-Italic",
        boldItalic="Charter-Bold",
    )
    pdfmetrics.registerFontFamily(
        "Avenir",
        normal="Avenir",
        bold="Avenir-Demi",
        italic="Avenir",
        boldItalic="Avenir-Demi",
    )


def styles() -> None:
    def add(name, **kw):
        S[name] = ParagraphStyle(name, **kw)

    add(
        "body",
        fontName="Charter",
        fontSize=10.5,
        leading=14.4,
        textColor=INK,
        alignment=TA_JUSTIFY,
    )
    add(
        "body_left",
        fontName="Charter",
        fontSize=10.5,
        leading=14.4,
        textColor=INK,
        alignment=TA_LEFT,
    )
    add(
        "lead",
        fontName="Charter",
        fontSize=11.5,
        leading=15.6,
        textColor=INK,
        alignment=TA_LEFT,
    )
    add(
        "small",
        fontName="Avenir",
        fontSize=8.5,
        leading=11.4,
        textColor=MUTED,
        alignment=TA_LEFT,
    )
    add(
        "caption",
        fontName="Avenir",
        fontSize=8.2,
        leading=11.0,
        textColor=MUTED,
        alignment=TA_LEFT,
    )
    add(
        "card_kicker",
        fontName="Avenir-Demi",
        fontSize=7.6,
        leading=9.4,
        textColor=TEAL,
        alignment=TA_LEFT,
    )
    add(
        "card_title",
        fontName="Avenir-Demi",
        fontSize=10.5,
        leading=13.2,
        textColor=INK,
        alignment=TA_LEFT,
    )
    add(
        "card_body",
        fontName="Charter",
        fontSize=9,
        leading=12.2,
        textColor=INK,
        alignment=TA_LEFT,
    )
    add(
        "th",
        fontName="Avenir-Demi",
        fontSize=8,
        leading=10.4,
        textColor=CREAM,
        alignment=TA_LEFT,
    )
    add(
        "td",
        fontName="Charter",
        fontSize=8.4,
        leading=11.0,
        textColor=INK,
        alignment=TA_LEFT,
    )
    add(
        "td_strong",
        fontName="Avenir-Medium",
        fontSize=8.3,
        leading=11.0,
        textColor=INK,
        alignment=TA_LEFT,
    )
    add(
        "fact_k",
        fontName="Avenir-Demi",
        fontSize=7.4,
        leading=9.2,
        textColor=TEAL,
        alignment=TA_LEFT,
    )
    add(
        "fact_t",
        fontName="Avenir-Demi",
        fontSize=10,
        leading=12.6,
        textColor=NAVY,
        alignment=TA_LEFT,
    )
    add(
        "fact_b",
        fontName="Charter",
        fontSize=8.2,
        leading=10.8,
        textColor=INK,
        alignment=TA_LEFT,
    )
    add(
        "cover_path",
        fontName="Avenir",
        fontSize=10,
        leading=13.2,
        textColor=CREAM,
        alignment=TA_LEFT,
    )
    add(
        "step",
        fontName="Charter",
        fontSize=9,
        leading=12.2,
        textColor=INK,
        alignment=TA_LEFT,
    )


def _font(path: Path, size: float) -> font_manager.FontProperties:
    return font_manager.FontProperties(fname=str(path), size=size)


def build_signal_chart() -> Path:
    regular = FONT_DIR / "Avenir.ttf"
    demi = FONT_DIR / "Avenir-Demi.ttf"
    t = [i / 10 for i in range(0, 401)]

    def pulse(x, start, peak, end, height, base):
        if x < start or x > end:
            return base
        if x < peak:
            u = (x - start) / (peak - start)
            s = u * u * (3 - 2 * u)
            return base + (height - base) * s
        u = (x - peak) / (end - peak)
        s = u * u * (3 - 2 * u)
        return height + (base - height) * s

    net = [pulse(x, 6, 9, 15, 1.0, 0.08) for x in t]
    puck = [0.08 + (0.78 - 0.08) * (0 if x < 11 else min(1, (x - 11) / 5)) for x in t]
    ble = [0.0 if x < 14 else 1.0 for x in t]

    fig, axes = plt.subplots(
        3,
        1,
        figsize=(10.7, 4.85),
        sharex=True,
        gridspec_kw={"hspace": 0.22, "top": 0.90, "bottom": 0.12, "left": 0.11, "right": 0.98},
    )
    fig.patch.set_facecolor("#FFFFFF")
    series = [
        (axes[0], net, "#1F7A6B", "Network metadata  ·  relative volume", [0.08, 1.0], ["low", "high"]),
        (axes[1], puck, "#B08448", "Sensor puck  ·  draw above a quiet baseline", [0.08, 0.78], ["baseline", "elevated"]),
        (axes[2], ble, "#C4473C", "Bluetooth  ·  rogue advertisement", [0.0, 1.0], ["absent", "present"]),
    ]
    for ax, y, color, title, ticks, labels in series:
        ax.set_facecolor("#FFFFFF")
        ax.axvspan(18, 40, color="#C4473C", alpha=0.08, lw=0)
        ax.axvline(18, color="#C4473C", lw=0.9, ls=(0, (3, 2)))
        ax.plot(t, y, color=color, lw=2.0, solid_capstyle="round")
        ax.set_ylim(-0.08, 1.22)
        ax.set_yticks(ticks)
        ax.set_yticklabels(labels, fontproperties=_font(regular, 8), color="#5C564F")
        ax.set_title(title, loc="left", fontproperties=_font(demi, 9.5), color="#1C1917", pad=4)
        ax.tick_params(axis="y", length=0, pad=3)
        ax.tick_params(axis="x", length=0, pad=2)
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)
        ax.spines["left"].set_color("#E4DDD4")
        ax.spines["bottom"].set_color("#E4DDD4")
        ax.grid(axis="y", color="#EFEAE3", lw=0.6)
        ax.set_axisbelow(True)
    axes[0].text(
        18.4,
        1.08,
        "TV quarantined",
        fontproperties=_font(demi, 8),
        color="#8C2F28",
        va="bottom",
    )
    axes[2].set_xlim(0, 40)
    axes[2].set_xticks([0, 6, 11, 14, 18, 30, 40])
    axes[2].set_xticklabels(
        ["0", "6", "11", "14", "18", "30", "40"],
        fontproperties=_font(regular, 8),
        color="#5C564F",
    )
    axes[2].set_xlabel(
        "Minutes from the first unusual flow    ·    shapes are explanatory, not a recording",
        fontproperties=_font(regular, 8),
        color="#5C564F",
        labelpad=6,
    )
    dest = FIG / "incident-signals.png"
    fig.savefig(dest, dpi=180)
    plt.close(fig)
    return dest


def build_pricing_chart() -> Path:
    regular = FONT_DIR / "Avenir.ttf"
    demi = FONT_DIR / "Avenir-Demi.ttf"
    rows = [
        ("Smart locks", 5, 10, "#8AA0AE"),
        ("Noise & occupancy monitors", 10, 15, "#8AA0AE"),
        ("This kit", 14, 19, "#145E52"),
    ]
    fig, ax = plt.subplots(figsize=(10.7, 2.55))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    for i, (label, lo, hi, color) in enumerate(rows):
        ax.barh(i, hi - lo, left=lo, height=0.42, color=color, zorder=3)
        ax.text(
            hi + 0.45,
            i,
            f"€{lo}–{hi}",
            va="center",
            fontproperties=_font(demi, 9),
            color="#1C1917",
        )
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontproperties=_font(regular, 9), color="#1C1917")
    ax.set_xlabel(
        "Euros per property (comparables quoted per door), per month",
        fontproperties=_font(regular, 8),
        color="#5C564F",
    )
    ax.set_xlim(0, 26)
    ax.set_xticks([0, 5, 10, 15, 20, 25])
    for label in ax.get_xticklabels():
        label.set_fontproperties(_font(regular, 8))
        label.set_color("#5C564F")
    ax.tick_params(length=0)
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#E4DDD4")
    ax.grid(axis="x", color="#EFEAE3", lw=0.6)
    ax.set_axisbelow(True)
    fig.subplots_adjust(left=0.28, right=0.97, top=0.88, bottom=0.28)
    dest = FIG / "pricing-ranges.png"
    fig.savefig(dest, dpi=180)
    plt.close(fig)
    return dest


def annual(properties: int, monthly: int) -> int:
    return properties * monthly * 12


def build_portfolio_chart() -> Path:
    regular = FONT_DIR / "Avenir.ttf"
    demi = FONT_DIR / "Avenir-Demi.ttf"
    portfolios = [10, 50, 200]
    low = [annual(n, 14) for n in portfolios]
    high = [annual(n, 19) for n in portfolios]
    fig, ax = plt.subplots(figsize=(10.7, 3.35))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    import numpy as np

    x = np.arange(len(portfolios))
    width = 0.36
    bars_low = ax.bar(x - width / 2, low, width, color="#1F7A6B", label="€14 / month", zorder=3)
    bars_high = ax.bar(x + width / 2, high, width, color="#102433", label="€19 / month", zorder=3)
    for bars in (bars_low, bars_high):
        for bar in bars:
            value = int(bar.get_height())
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                value + 700,
                f"€{value:,.0f}",
                ha="center",
                va="bottom",
                fontproperties=_font(demi, 7.5),
                color="#1C1917",
            )
    ax.set_xticks(x)
    ax.set_xticklabels(
        [f"{n} properties" for n in portfolios],
        fontproperties=_font(regular, 9),
        color="#1C1917",
    )
    ax.set_ylabel(
        "Illustrative annual subscription",
        fontproperties=_font(regular, 8),
        color="#5C564F",
    )
    ax.set_ylim(0, 54000)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _p: f"€{int(v / 1000)}k" if v else "€0"))
    for label in ax.get_yticklabels():
        label.set_fontproperties(_font(regular, 8))
        label.set_color("#5C564F")
    legend = ax.legend(frameon=False, prop=_font(regular, 8), loc="upper left")
    for text in legend.get_texts():
        text.set_color("#1C1917")
    ax.tick_params(length=0)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#E4DDD4")
    ax.spines["bottom"].set_color("#E4DDD4")
    ax.grid(axis="y", color="#EFEAE3", lw=0.6)
    ax.set_axisbelow(True)
    fig.subplots_adjust(left=0.10, right=0.98, top=0.92, bottom=0.16)
    dest = FIG / "portfolio-subscription.png"
    fig.savefig(dest, dpi=180)
    plt.close(fig)
    return dest


def para_height(text: str, style: ParagraphStyle, width: float) -> float:
    if not text:
        return 0
    paragraph = Paragraph(text, style)
    _w, h = paragraph.wrap(width, 4000)
    return h


def draw_para(c: canvas.Canvas, text: str, style: ParagraphStyle, x: float, y_top: float, width: float) -> float:
    paragraph = Paragraph(text, style)
    _w, h = paragraph.wrap(width, 4000)
    paragraph.drawOn(c, x, y_top - h)
    return h


def begin_page(c: canvas.Canvas, section: str, key: str, title: str) -> None:
    c.setFillColor(PAGE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, H - 5, W, 5, fill=1, stroke=0)
    c.setFillColor(MUTED)
    c.setFont("Avenir-Medium", 8)
    c.drawString(LEFT, H - 24, section.upper())
    c.setFillColor(TEAL)
    c.setFont("Avenir-Demi", 8)
    c.drawRightString(RIGHT, H - 24, f"{c.getPageNumber():02d}")
    c.setStrokeColor(RULE)
    c.setLineWidth(0.4)
    c.line(LEFT, H - 32, RIGHT, H - 32)
    c.bookmarkPage(key)
    c.addOutlineEntry(title, key, level=0, closed=False)


def finish_page(c: canvas.Canvas, y: float, name: str) -> None:
    if y < BOTTOM:
        raise SystemExit(f"Layout overflow on {name}: content ended at y={y:.1f}")
    c.setStrokeColor(RULE)
    c.setLineWidth(0.4)
    c.line(LEFT, 30, RIGHT, 30)
    c.setFillColor(MUTED)
    c.setFont("Avenir", 7.5)
    c.drawString(LEFT, 18, "EAE Madrid  ·  Master in Project Management  ·  November 2026")
    c.drawRightString(RIGHT, 18, "Hospitality & short-term rentals")
    c.showPage()


def section_title(c: canvas.Canvas, kicker: str, title: str, y: float) -> float:
    c.setFillColor(TEAL)
    c.setFont("Avenir-Demi", 8)
    c.drawString(LEFT, y - 8, kicker.upper())
    c.setFillColor(NAVY)
    c.setFont("Charter-Bold", 20)
    c.drawString(LEFT, y - 32, title)
    return 42


def draw_swatch_line(c: canvas.Canvas, x: float, y: float, color, dashed: bool = False) -> None:
    c.setStrokeColor(color)
    c.setLineWidth(2.0)
    c.setLineCap(1)
    if dashed:
        c.setDash(3.2, 2.2)
    c.line(x, y, x + 28, y)
    c.setDash()


def row_of_cards(c: canvas.Canvas, cards: list[dict], x: float, y: float, width: float, cols: int, gap: float = 10) -> float:
    col_w = (width - gap * (cols - 1)) / cols
    rows = [cards[i : i + cols] for i in range(0, len(cards), cols)]
    cursor = y
    for row in rows:
        heights = []
        inners = []
        for card in row:
            pad = 11
            inner_w = col_w - pad * 2 - 3
            h = pad
            if card.get("kicker"):
                h += para_height(card["kicker"], S["card_kicker"], inner_w) + 2
            h += para_height(card["title"], S["card_title"], inner_w) + 3
            h += para_height(card["body"], S["card_body"], inner_w)
            h += pad
            heights.append(h)
            inners.append(inner_w)
        row_h = max(heights)
        for i, card in enumerate(row):
            cx = x + i * (col_w + gap)
            c.setFillColor(CARD)
            c.setStrokeColor(RULE)
            c.setLineWidth(0.6)
            c.roundRect(cx, cursor - row_h, col_w, row_h, 6, fill=1, stroke=1)
            c.setFillColor(card.get("accent", TEAL))
            c.rect(cx, cursor - row_h, 3.2, row_h, fill=1, stroke=0)
            pad = 11
            inner_w = inners[i]
            tx = cx + pad + 2
            ty = cursor - pad
            if card.get("kicker"):
                kh = draw_para(c, card["kicker"], S["card_kicker"], tx, ty, inner_w)
                ty -= kh + 2
            th = draw_para(c, card["title"], S["card_title"], tx, ty, inner_w)
            ty -= th + 3
            draw_para(c, card["body"], S["card_body"], tx, ty, inner_w)
        cursor -= row_h + gap
    return y - cursor - gap


def draw_figure(c: canvas.Canvas, path: Path, x: float, y_top: float, width: float, max_h: float) -> float:
    with Image.open(path) as image:
        iw, ih = image.size
    height = min(max_h, width * ih / iw)
    used_w = height * iw / ih
    c.setFillColor(CARD)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.roundRect(x - 1, y_top - height - 1, used_w + 2, height + 2, 4, fill=1, stroke=1)
    c.drawImage(str(path), x, y_top - height, width=used_w, height=height, mask="auto")
    return height


def draw_brief_index(c: canvas.Canvas, x: float, y_top: float, width: float) -> None:
    c.setFillColor(HexColor("#8FB0A8"))
    c.setFont("Avenir-Demi", 7.4)
    c.drawString(x, y_top - 2, "IN THIS BRIEF")
    rows = [
        [("02", "Apartment"), ("03", "Incident"), ("04", "Exposure"), ("05", "Architecture"), ("06", "Turnover")],
        [("07", "Comparison"), ("08", "Privacy"), ("09", "Commercial"), ("10", "Thesis"), ("11", "Pilot")],
    ]
    col_w = width / 5
    y = y_top - 20
    for row in rows:
        for i, (num, name) in enumerate(row):
            cx = x + i * col_w
            c.setFillColor(HexColor("#9ED9CE"))
            c.setFont("Avenir-Demi", 8)
            c.drawString(cx, y, num)
            c.setFillColor(CREAM)
            c.setFont("Avenir", 8.5)
            c.drawString(cx + 16, y, name)
        y -= 16


def draw_two_stays(c: canvas.Canvas, x: float, y_top: float, width: float) -> float:
    height = 116
    y = y_top - height
    c.setFillColor(CARD)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.roundRect(x, y, width, height, 6, fill=1, stroke=1)
    stays = [
        (AMBER, "Stay N", "The guest is in the room. Phone and laptop sit on the dashed path. The television is on the management path, where a local payload can arrive and then go quiet."),
        (TEAL, "Turnover", "11:00 to 15:00. Firmware and configuration, pairing caches, and a BLE beacon that outlived the guest. The health score is the output."),
        (NAVY, "Stay N+1", "The next guest arrives against that score. A condition still living on the television is the failure this kit is scoped to catch."),
    ]
    gap = 10
    col_w = (width - 20 - gap * 2) / 3
    for i, (color, title, body) in enumerate(stays):
        cx = x + 10 + i * (col_w + gap)
        c.setFillColor(color)
        c.rect(cx, y + height - 16, 18, 3, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont("Avenir-Demi", 9)
        c.drawString(cx, y + height - 32, title)
        draw_para(c, body, S["caption"], cx, y + height - 40, col_w - 4)
        if i < 2:
            c.setFillColor(MUTED)
            c.setFont("Avenir", 11)
            c.drawCentredString(cx + col_w + gap / 2, y + height - 34, "→")
    return height


def draw_instrument_rows(c: canvas.Canvas, x: float, y_top: float, width: float) -> float:
    rows = [
        ("Endpoint", "The television has no agent. The gateway watches it from the path it already sits on."),
        ("The router", "Local flows and BLE stay visible when the traffic never leaves for the internet."),
        ("The next stay", "The health score is part of turnover, in the same window as the linen."),
        ("Power and radio", "The puck and the BLE scan are the two instruments a modem does not have."),
    ]
    row_h = 28
    gap = 3
    for i, (title, body) in enumerate(rows):
        yy = y_top - i * (row_h + gap)
        c.setFillColor(CARD)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.4)
        c.roundRect(x, yy - row_h, width, row_h, 4, fill=1, stroke=1)
        c.setFillColor(NAVY)
        c.setFont("Avenir-Demi", 8)
        c.drawString(x + 10, yy - 19, title)
        draw_para(c, body, S["caption"], x + 108, yy - 8, width - 120)
    return len(rows) * (row_h + gap) - gap


def draw_sweep(c: canvas.Canvas, x: float, y_top: float, width: float) -> float:
    height = 108
    y = y_top - height
    c.setFillColor(CARD)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.roundRect(x, y, width, height, 6, fill=1, stroke=1)
    c.setFillColor(TEAL)
    c.setFont("Avenir-Demi", 7.5)
    c.drawString(x + 12, y + height - 16, "THE SWEEP, IN ORDER")
    steps = [
        ("1", "Open", "The PMS marks the window from the calendar."),
        ("2", "Compare", "Firmware and configuration against the previous sweep."),
        ("3", "Clear", "Guest pairing caches on the lock and the television."),
        ("4", "Listen", "BLE adverts, for a beacon absent at check-in."),
        ("5", "Sign", "Health score, on the manager’s console before 15:00."),
    ]
    gap = 6
    col_w = (width - 24 - gap * 4) / 5
    for i, (num, title, body) in enumerate(steps):
        cx = x + 12 + i * (col_w + gap)
        c.setFillColor(TEAL)
        c.setFont("Avenir-Demi", 8)
        c.drawString(cx, y + height - 36, num)
        c.setFillColor(NAVY)
        c.setFont("Avenir-Demi", 8)
        c.drawString(cx + 12, y + height - 36, title)
        draw_para(c, body, S["caption"], cx, y + height - 44, col_w)
    return height


def draw_figure_links(c: canvas.Canvas, x: float, y_top: float, width: float) -> float:
    rows = [
        (GREEN_LINE, "Segmentation", "Solid green is the management path. Dashed tan is the guest path. They meet at the gateway."),
        (AMBER_LINE, "Silent compute", "“Puck elevated” is the side-channel, sitting on the television console."),
        (CRIMSON_LINE, "Bluetooth", "“Rogue BLE” and the dashed red path are the radio observation from the gateway."),
        (TEAL, "Turnover", "The drawing is a mid-stay failure. The sweep is how that state is caught before the next arrival."),
        (NAVY, "Fleet", "The gateway in the entry is one node. The console is the same status, repeated across the portfolio."),
        (TEAL, "Privacy", "The laptop and the phone are on the guest path, and that path is read as metadata."),
    ]
    row_h = 34
    gap = 4
    for i, (color, title, body) in enumerate(rows):
        yy = y_top - i * (row_h + gap)
        c.setFillColor(CARD)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.4)
        c.roundRect(x, yy - row_h, width, row_h, 4, fill=1, stroke=1)
        c.setFillColor(color)
        c.rect(x, yy - row_h, 3.2, row_h, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont("Avenir-Demi", 8.5)
        c.drawString(x + 14, yy - 14, title)
        draw_para(c, body, S["caption"], x + 118, yy - 8, width - 132)
    return len(rows) * (row_h + gap) - gap


def draw_data_split(c: canvas.Canvas, x: float, y_top: float, width: float) -> float:
    height = 168
    y = y_top - height
    gap = 10
    col_w = (width - gap) / 2
    columns = [
        (TEAL, "On the gateway", [
            "Flow volumes, headers, ports, and DNS",
            "The BLE advertisement log",
            "Puck samples, once phase 2 is installed",
            "The correlation that turns three signals into one status",
            "Logs for this stay, deleted at checkout",
        ]),
        (NAVY, "To the cloud", [
            "A status: green, amber, or red",
            "The turnover health score",
            "Which property device changed state",
            "The time of the sweep",
            "Nothing that reconstructs a guest’s traffic",
        ]),
    ]
    for i, (color, title, lines) in enumerate(columns):
        cx = x + i * (col_w + gap)
        c.setFillColor(CARD)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.6)
        c.roundRect(cx, y, col_w, height, 6, fill=1, stroke=1)
        c.setFillColor(color)
        c.rect(cx, y, 3.2, height, fill=1, stroke=0)
        c.setFillColor(color)
        c.setFont("Avenir-Demi", 10)
        c.drawString(cx + 14, y + height - 20, title)
        ly = y + height - 38
        for line in lines:
            c.setFillColor(color)
            c.circle(cx + 18, ly + 3, 2, fill=1, stroke=0)
            draw_para(c, line, S["small"], cx + 28, ly + 10, col_w - 42)
            ly -= 24
    return height


def draw_money_tiles(c: canvas.Canvas, x: float, y_top: float, width: float) -> float:
    height = 62
    tiles = [
        ("€99–€149", "Hardware, once per gateway"),
        ("€14–€19", "Subscription, per property / month"),
        ("> 80%", "SaaS gross-margin target"),
    ]
    gap = 8
    col_w = (width - gap * 2) / 3
    for i, (value, label) in enumerate(tiles):
        cx = x + i * (col_w + gap)
        c.setFillColor(NAVY)
        c.roundRect(cx, y_top - height, col_w, height, 5, fill=1, stroke=0)
        c.setFillColor(CREAM)
        c.setFont("Avenir-Demi", 14)
        c.drawString(cx + 12, y_top - 26, value)
        c.setFillColor(HexColor("#D5E6E1"))
        c.setFont("Avenir", 7.5)
        c.drawString(cx + 12, y_top - 42, label)
    return height


def draw_phases(c: canvas.Canvas, x: float, y_top: float, width: float) -> float:
    height = 96
    y = y_top - height
    c.setFillColor(CARD)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.roundRect(x, y, width, height, 6, fill=1, stroke=1)
    phases = [
        ("Phase 1  ·  MVP", "Managed LAN enforcement, device and flow monitoring, PMS turnover and fleet dashboard."),
        ("Phase 2", "Power and thermal pucks on the high-value appliances."),
        ("Pilot", "Twenty apartments with Madrid short-term managers, after the charter and the architecture spec."),
    ]
    col_w = (width - 28) / 3
    for i, (title, body) in enumerate(phases):
        cx = x + 12 + i * col_w
        c.setFillColor(TEAL if i < 2 else NAVY)
        c.circle(cx + 4, y + height - 20, 3.5, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont("Avenir-Demi", 8.5)
        c.drawString(cx + 14, y + height - 24, title)
        draw_para(c, body, S["caption"], cx, y + height - 36, col_w - 16)
    return height


def page_cover(c: canvas.Canvas) -> None:
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(TEAL_LINE)
    c.rect(0, H - 6, W, 6, fill=1, stroke=0)

    c.setFillColor(HexColor("#D5E6E1"))
    c.setFont("Avenir-Medium", 8.5)
    c.drawString(LEFT, H - 48, "EAE MADRID   ·   MASTER IN PROJECT MANAGEMENT   ·   PMBOK   ·   NOVEMBER 2026")

    c.setFillColor(CREAM)
    c.setFont("Charter-Bold", 34)
    c.drawString(LEFT, H - 108, "IoT Security Kit")
    c.drawString(LEFT, H - 148, "Against Sleeper AI Agents")

    c.setStrokeColor(TEAL_LINE)
    c.setLineWidth(1.4)
    c.line(LEFT, H - 168, LEFT + 86, H - 168)

    deck = (
        "A local edge appliance and a fleet console for boutique hotels, "
        "short-term rentals, and serviced apartments. The gateway watches "
        "network metadata, Bluetooth, and power, and it reports a status the "
        "property manager can act on between guests."
    )
    draw_para(c, deck, S["cover_path"], LEFT, H - 196, 500)

    c.setFillColor(HexColor("#C9D5DE"))
    c.setFont("Avenir", 9)
    c.drawString(LEFT, H - 292, "Reference scene  ·  a one-bedroom short-term rental. The drawing is on the next page.")
    draw_brief_index(c, LEFT, H - 314, WIDTH)

    card_y = 214
    card_h = 248
    c.setFillColor(NAVY_2)
    c.roundRect(LEFT, card_y, WIDTH, card_h, 8, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.setFont("Avenir-Demi", 8)
    c.drawString(LEFT + 16, card_y + card_h - 22, "THREE PATHS IN THE APARTMENT")

    paths = [
        (GREEN_LINE, False, "Management path", "Smart lock, thermostat, television, and the gateway in the entry. One controlled segment."),
        (AMBER_LINE, True, "Guest path", "Laptop and phone stay on their own segment, off the lock and the television."),
        (CRIMSON_LINE, True, "Rogue path", "A foreign BLE transmitter by the television. The set is quarantined. The puck reads elevated."),
    ]
    row_top = card_y + card_h - 48
    for i, (color, dashed, title, body) in enumerate(paths):
        yy = row_top - i * 64
        draw_swatch_line(c, LEFT + 18, yy - 8, color, dashed)
        c.setFillColor(CREAM)
        c.setFont("Avenir-Demi", 11)
        c.drawString(LEFT + 58, yy - 4, title)
        draw_para(c, body, S["cover_path"], LEFT + 58, yy - 12, WIDTH - 86)

    c.setFillColor(PAGE)
    c.rect(0, 0, W, 196, fill=1, stroke=0)
    facts = [
        ("01  /  Placement", "Inline at the entry", "Between the fiber modem and the apartment Wi-Fi, beside the smart lock."),
        ("02  /  Sensors", "Three channels", "Flow metadata, BLE advertising, and an optional power and thermal puck."),
        ("03  /  Operations", "Turnover audit", "A health score in the window from 11:00 check-out to 15:00 check-in."),
        ("04  /  Price", "€14–19 / month", "Per property. Hardware €99–€149, or €0 upfront on an annual term."),
    ]
    col_w = WIDTH / 4
    for i, (kicker, title, body) in enumerate(facts):
        fx = LEFT + i * col_w
        if i:
            c.setStrokeColor(RULE)
            c.setLineWidth(0.5)
            c.line(fx - 8, 36, fx - 8, 168)
        draw_para(c, kicker, S["fact_k"], fx, 172, col_w - 16)
        draw_para(c, title, S["fact_t"], fx, 150, col_w - 16)
        draw_para(c, body, S["fact_b"], fx, 124, col_w - 16)

    c.bookmarkPage("cover")
    c.addOutlineEntry("Cover", "cover", level=0, closed=False)
    c.showPage()


def page_setup(c: canvas.Canvas, floorplan: Path) -> None:
    begin_page(c, "The setup", "setup", "The reference apartment")
    y = H - 50
    y -= section_title(c, "Figure 1", "One apartment, three paths", y)
    y -= 8
    lead = (
        "Living holds the television, the sensor puck, the rogue transmitter, and both guest devices. "
        "The guest path returns along the kitchen. The bedroom has no monitored device in this drawing. "
        "The entry holds the gateway and the smart lock."
    )
    y -= draw_para(c, lead, S["lead"], LEFT, y, WIDTH)
    y -= 12
    image_h = draw_figure(c, floorplan, LEFT, y, WIDTH, 430)
    y -= image_h + 8
    y -= draw_para(
        c,
        "Figure 1. Supplied setup drawing of the reference apartment. Schematic, not a measured floor plan. "
        "Line colors below match the drawing.",
        S["caption"],
        LEFT,
        y,
        WIDTH,
    )
    y -= 14
    legend = [
        (GREEN_LINE, False, "Management path", "Solid green. Lock, thermostat, television, and the fixed device on the left wall of the living room. All of them end at the gateway."),
        (AMBER_LINE, True, "Guest path", "Dashed tan. Laptop and phone. The path reaches the gateway and stays off the lock, the thermostat, and the television."),
        (CRIMSON_LINE, True, "Rogue BLE", "Dashed red. A foreign transmitter beside the television, observed from the gateway’s radio."),
        (CRIMSON_LINE, False, "Quarantine", "Red box and crosses. The television is isolated. The crossed links are blocked."),
    ]
    # Puck is a label, not a line. Draw four line rows, then a fifth text row.
    for color, dashed, title, body in legend:
        c.setFillColor(CARD)
        c.roundRect(LEFT, y - 32, WIDTH, 32, 4, fill=1, stroke=0)
        if dashed:
            draw_swatch_line(c, LEFT + 10, y - 16, color, True)
        elif title == "Quarantine":
            c.setStrokeColor(color)
            c.setLineWidth(1.3)
            c.roundRect(LEFT + 10, y - 22, 22, 12, 2, fill=0, stroke=1)
            c.setFont("Avenir-Demi", 7)
            c.setFillColor(color)
            c.drawString(LEFT + 16, y - 19, "×")
        else:
            draw_swatch_line(c, LEFT + 10, y - 16, color, False)
        c.setFillColor(NAVY)
        c.setFont("Avenir-Demi", 8.5)
        c.drawString(LEFT + 46, y - 13, title)
        c.setFillColor(MUTED)
        c.setFont("Avenir", 8)
        # body may be long; use a paragraph in the remaining width
        draw_para(c, body, S["caption"], LEFT + 148, y - 6, WIDTH - 160)
        y -= 36
    # The paragraph height may exceed 32 and overflow the row. Guard after.
    finish_page(c, y, "setup")


def page_incident(c: canvas.Canvas, signals: Path) -> None:
    begin_page(c, "The setup", "incident", "Reading the incident")
    y = H - 50
    y -= section_title(c, "Figure 2", "Four observations, then quarantine", y)
    y -= 8
    lead = (
        "The drawing on the previous page is the end state. Read it as a short sequence. "
        "A large flow appears on the television’s management path, the puck leaves its baseline and stays there, "
        "and a BLE advertisement shows up beside the set. The correlation engine treats those three as one condition "
        "and the policy engine quarantines the television."
    )
    y -= draw_para(c, lead, S["body"], LEFT, y, WIDTH)
    y -= 12
    y -= draw_fusion(c, LEFT, y, WIDTH)
    y -= 12
    image_h = draw_figure(c, signals, LEFT, y, WIDTH, 320)
    y -= image_h + 6
    y -= draw_para(
        c,
        "Figure 2. Illustrative traces for the incident in Figure 1. The vertical axis is relative on purpose: "
        "these are shapes that explain the drawing, not a recording from a property.",
        S["caption"],
        LEFT,
        y,
        WIDTH,
    )
    y -= 12
    beats = [
        ("6 min", "Volume", "A tall, short-lived flow on the management path, the shape of a large download, then quiet again."),
        ("11 min", "Puck", "Power or thermal draw steps off the quiet baseline and holds. The label in the drawing is “Puck elevated.”"),
        ("14 min", "Rogue BLE", "Advertisements appear beside the television. The dashed red path is that observation."),
        ("18 min", "Quarantine", "The fused condition isolates the television. Crosses mark the blocked links."),
    ]
    y -= row_of_cards(
        c,
        [
            {"kicker": t, "title": title, "body": body, "accent": color}
            for (t, title, body), color in zip(
                beats, [TEAL, AMBER, CRIMSON, CRIMSON]
            )
        ],
        LEFT,
        y,
        WIDTH,
        4,
        gap=8,
    )
    y -= 4
    note_h = 52
    c.setFillColor(NAVY)
    c.roundRect(LEFT, y - note_h, WIDTH, note_h, 5, fill=1, stroke=0)
    c.setFillColor(HexColor("#D5E6E1"))
    c.setFont("Avenir-Demi", 7.5)
    c.drawString(LEFT + 12, y - 16, "WHAT THIS INCIDENT SENDS UPSTAIRS")
    draw_para(
        c,
        "The cloud receives a status, the device, and the time. The download itself, the BLE payload, and the puck samples stay on the gateway. That split is the privacy rule on page 8, applied to Figure 1.",
        ParagraphStyle(
            "note",
            fontName="Charter",
            fontSize=9,
            leading=12.2,
            textColor=CREAM,
        ),
        LEFT + 12,
        y - 24,
        WIDTH - 24,
    )
    y -= note_h
    finish_page(c, y, "incident")


def draw_fusion(c: canvas.Canvas, x: float, y_top: float, width: float) -> float:
    height = 78
    y = y_top - height
    c.setFillColor(CARD)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.roundRect(x, y, width, height, 6, fill=1, stroke=1)
    inputs = [
        (TEAL_SOFT, TEAL, "Network metadata"),
        (AMBER_SOFT, AMBER, "Puck elevated"),
        (CRIMSON_SOFT, CRIMSON, "Rogue BLE"),
    ]
    box_w, box_h = 118, 16
    top = y + height - 16 - box_h
    for i, (fill, stroke, label) in enumerate(inputs):
        by = top - i * 20
        c.setFillColor(fill)
        c.setStrokeColor(stroke)
        c.setLineWidth(0.8)
        c.roundRect(x + 12, by, box_w, box_h, 3, fill=1, stroke=1)
        c.setFillColor(stroke)
        c.setFont("Avenir-Demi", 7.5)
        c.drawCentredString(x + 12 + box_w / 2, by + 4.5, label)
        c.setStrokeColor(stroke)
        c.setLineWidth(1.0)
        c.line(x + 12 + box_w, by + box_h / 2, x + 168, y + height / 2)
    # merge node
    c.setFillColor(NAVY)
    c.circle(x + 172, y + height / 2, 4, fill=1, stroke=0)
    stages = [
        (x + 190, "Correlation", "On the gateway"),
        (x + 310, "Policy", "VLAN & quarantine"),
        (x + 420, "Result", "TV quarantined"),
    ]
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.1)
    c.line(x + 176, y + height / 2, x + 500, y + height / 2)
    for sx, title, sub in stages:
        c.setFillColor(NAVY if title != "Result" else CRIMSON)
        c.roundRect(sx, y + height / 2 - 14, 96, 28, 4, fill=1, stroke=0)
        c.setFillColor(CREAM)
        c.setFont("Avenir-Demi", 8)
        c.drawCentredString(sx + 48, y + height / 2 + 1, title)
        c.setFont("Avenir", 6.5)
        c.drawCentredString(sx + 48, y + height / 2 - 9, sub)
    return height


def page_problem(c: canvas.Canvas) -> None:
    begin_page(c, "Threat model", "problem", "The exposure")
    y = H - 50
    y -= section_title(c, "Problem", "A quiet model on a loud appliance", y)
    y -= 8
    lead = (
        "Televisions, locks, thermostats, voice assistants, and set-top boxes in a rental now have the memory "
        "and the compute to run a small language model on the device. Quantized models in the 0.5B–3B range "
        "fit on Android TV, Tizen, webOS, and embedded Linux. Once that payload is local, it can wait."
    )
    y -= draw_para(c, lead, S["body"], LEFT, y, WIDTH)
    y -= 12
    threats = [
        {
            "kicker": "Condition",
            "title": "Dormant until a local cue",
            "body": "Little or no outbound traffic while it waits. A date, the presence of a particular guest, a spoken phrase, or a request already on the LAN is enough to wake it.",
            "accent": CRIMSON,
        },
        {
            "kicker": "Channel",
            "title": "Commands off the IP path",
            "body": "A second local channel carries instructions: Bluetooth or BLE, a firmware image introduced beside the normal update path, or an ad-hoc radio. The modem’s internet log stays quiet.",
            "accent": CRIMSON,
        },
        {
            "kicker": "Position",
            "title": "Already inside the room",
            "body": "The device can collect credentials, use an onboard microphone or camera, and look across the rest of the apartment network from a trusted socket.",
            "accent": AMBER,
        },
        {
            "kicker": "Duration",
            "title": "It outlives the guest",
            "body": "Checkout does not clear it. The next guest inherits the condition. The property manager inherits the liability and the brand damage.",
            "accent": AMBER,
        },
    ]
    y -= row_of_cards(c, threats, LEFT, y, WIDTH, 2, gap=8)
    y -= 6
    c.setFillColor(NAVY)
    c.setFont("Avenir-Demi", 9)
    c.drawString(LEFT, y - 10, "What a standard modem cannot see")
    y -= 20
    gaps = [
        ("Endpoint", "Televisions, locks, and domestic appliances have no antivirus and no endpoint agent. There is nothing on the device to ask."),
        ("The router", "An ISP modem or a mesh node watches outbound internet packets. Local compute, peer scanning, and a BLE beacon are outside that view."),
        ("The next stay", "A backdoor left in stay N is still there for stay N+1. Turnover today checks linen and locks. It does not check the television."),
        ("Power and radio", "Nobody is routinely watching outlet draw, surface heat, or unauthorized transmitters in the room."),
    ]
    y -= row_of_cards(
        c,
        [{"kicker": "Blind spot", "title": t, "body": b, "accent": NAVY} for t, b in gaps],
        LEFT,
        y,
        WIDTH,
        4,
        gap=8,
    )
    y -= 4
    c.setFillColor(NAVY)
    c.setFont("Avenir-Demi", 9)
    c.drawString(LEFT, y - 2, "Across two stays")
    y -= 14
    y -= draw_two_stays(c, LEFT, y, WIDTH)
    y -= 6
    y -= draw_para(
        c,
        "Figure 3. The product is scoped to the gap between guests. The floor plan is what a missed gap looks like during a stay.",
        S["caption"],
        LEFT,
        y,
        WIDTH,
    )
    y -= 6
    y -= draw_instrument_rows(c, LEFT, y, WIDTH)
    finish_page(c, y, "problem")


def page_architecture(c: canvas.Canvas) -> None:
    begin_page(c, "Solution", "architecture", "System architecture")
    y = H - 50
    y -= section_title(c, "The kit", "A gateway, then a console", y)
    y -= 8
    lead = (
        "The pilot gateway routes between protected LAN segments or controls a managed router, switch and access point. The kit also includes an optional puck and a cloud console "
        "for whoever runs five properties or five hundred. Phase 1 is the gateway, the network and BLE engines, "
        "the turnover link to the property system, and the fleet dashboard. Phase 2 adds the puck."
    )
    y -= draw_para(c, lead, S["body"], LEFT, y, WIDTH)
    y -= 10
    arch_h = 292
    draw_architecture(c, LEFT, y, WIDTH, arch_h)
    y -= arch_h + 8
    y -= draw_para(
        c,
        "Figure 4. Concept schematic. The pilot separates media from critical property devices and routes between them through an enforcement point (page 11). "
        "The puck is out of band: it feeds correlation, and it does not sit on either VLAN. "
        "Quarantine is a policy action on a management device — the television in Figure 1.",
        S["caption"],
        LEFT,
        y,
        WIDTH,
    )
    y -= 14
    layers = [
        ("Network metadata", "LAN / WLAN", "Bulk downloads on the order of several gigabytes, internal port scans, odd DNS, command-and-control beacons.", "Measures transfer patterns without inspecting guest payloads."),
        ("Bluetooth and RF", "BLE and classic", "Rogue proximity beacons, covert transmitters, pairing attempts beside the lock.", "Finds hardware a guest, or a previous guest, left in the room."),
        ("Side channel", "Puck, phase 2", "Thermal and electrical deviations from the device baseline.", "Provides context for investigating unusual device activity."),
        ("Correlation", "On the gateway", "Correlates available signals and policy events.", "Adds context to alerts and operator review."),
    ]
    # compact layer rows
    row_h = 52
    for name, where, detects, benefit in layers:
        if y - row_h < BOTTOM:
            break
        c.setFillColor(CARD)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.5)
        c.roundRect(LEFT, y - row_h, WIDTH, row_h, 5, fill=1, stroke=1)
        c.setFillColor(TEAL)
        c.setFont("Avenir-Demi", 9)
        c.drawString(LEFT + 10, y - 16, name)
        c.setFillColor(MUTED)
        c.setFont("Avenir", 7.5)
        c.drawString(LEFT + 10, y - 28, where)
        draw_para(c, detects, S["caption"], LEFT + 150, y - 8, 190)
        draw_para(c, benefit, S["small"], LEFT + 348, y - 8, WIDTH - 360)
        y -= row_h + 5
    y -= 6
    c.setFillColor(TEAL_SOFT)
    c.roundRect(LEFT, y - 36, WIDTH, 36, 4, fill=1, stroke=0)
    draw_para(
        c,
        "Phase 1 ships the gateway, the two network engines, PMS turnover, and the dashboard. The puck, and the side-channel row above, are phase 2.",
        S["small"],
        LEFT + 10,
        y - 8,
        WIDTH - 20,
    )
    y -= 36
    finish_page(c, y, "architecture")


def draw_architecture(c: canvas.Canvas, x: float, y_top: float, width: float, height: float) -> None:
    y = y_top - height
    c.setFillColor(CARD)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.roundRect(x, y, width, height, 6, fill=1, stroke=1)

    devices = [
        ("Smart TV", TEAL_SOFT, TEAL, "Management"),
        ("Door lock", TEAL_SOFT, TEAL, "Management"),
        ("Thermostat", TEAL_SOFT, TEAL, "Management"),
        ("Guest devices", AMBER_SOFT, AMBER, "Guest VLAN"),
    ]
    gap = 8
    pill_w = (width - 24 - gap * 3) / 4
    pill_h = 32
    pill_top = y_top - 12 - pill_h
    centers = []
    for i, (label, fill, stroke, sub) in enumerate(devices):
        px = x + 12 + i * (pill_w + gap)
        c.setFillColor(fill)
        c.setStrokeColor(stroke)
        c.setLineWidth(0.9)
        c.roundRect(px, pill_top, pill_w, pill_h, 4, fill=1, stroke=1)
        c.setFillColor(stroke)
        c.setFont("Avenir-Demi", 8)
        c.drawCentredString(px + pill_w / 2, pill_top + 16, label)
        c.setFont("Avenir", 6.5)
        c.drawCentredString(px + pill_w / 2, pill_top + 6, sub)
        centers.append(px + pill_w / 2)

    gw_x = x + 12
    gw_w = width - 24
    gw_h = 108
    gw_top = pill_top - 36
    gw_y = gw_top - gw_h
    # arrows
    for i, cx in enumerate(centers):
        c.setStrokeColor(TEAL_LINE if i < 3 else AMBER_LINE)
        c.setLineWidth(1.1)
        if i == 3:
            c.setDash(2.5, 2)
        c.line(cx, pill_top, cx, gw_top)
        c.setDash()

    c.setFillColor(NAVY)
    c.roundRect(gw_x, gw_y, gw_w, gw_h, 5, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.setFont("Avenir-Demi", 7.5)
    c.drawString(gw_x + 10, gw_y + gw_h - 14, "EDGE SECURITY GATEWAY")
    c.setFont("Avenir", 7)
    c.setFillColor(HexColor("#D5E6E1"))
    c.drawRightString(gw_x + gw_w - 10, gw_y + gw_h - 14, "Raspberry Pi 5 class  ·  inline")
    cells = [
        ("Network metadata", "DNS, flows, volume"),
        ("Bluetooth / RF", "BLE advertising"),
        ("Correlation", "Local engine"),
        ("Policy", "VLAN & quarantine"),
    ]
    cell_gap = 6
    cell_w = (gw_w - 20 - cell_gap * 3) / 4
    cell_h = 62
    cell_y = gw_y + 14
    for i, (title, sub) in enumerate(cells):
        cx = gw_x + 10 + i * (cell_w + cell_gap)
        c.setFillColor(NAVY_2)
        c.roundRect(cx, cell_y, cell_w, cell_h, 4, fill=1, stroke=0)
        c.setFillColor(CREAM)
        c.setFont("Avenir-Demi", 7.6)
        c.drawString(cx + 6, cell_y + 36, title)
        c.setFillColor(HexColor("#D5E6E1"))
        c.setFont("Avenir", 7)
        c.drawString(cx + 6, cell_y + 22, sub)
        if i < 3:
            c.setStrokeColor(HexColor("#7FB5A8"))
            c.setLineWidth(1.3)
            mid = cell_y + cell_h / 2
            c.line(cx + cell_w, mid, cx + cell_w + cell_gap, mid)

    # cloud
    cloud_y = y + 12
    cloud_h = 48
    c.setStrokeColor(NAVY)
    c.setFillColor(NAVY)
    c.setLineWidth(1)
    mid = x + width / 2
    c.line(mid, gw_y, mid, cloud_y + cloud_h)
    c.setFillColor(TEAL_SOFT)
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.8)
    c.roundRect(gw_x, cloud_y, gw_w, cloud_h, 5, fill=1, stroke=1)
    cloud_cells = [
        ("Fleet dashboard", "Status for every property"),
        ("PMS sync", "Guesty, Smoobu, Beds24, iCal"),
        ("Turnover audit", "Health score before check-in"),
        ("Manager", "Green / amber / red"),
    ]
    for i, (title, sub) in enumerate(cloud_cells):
        cx = gw_x + 8 + i * (cell_w + cell_gap)
        if i == 3:
            c.setFillColor(NAVY)
            c.roundRect(cx - 2, cloud_y + 7, cell_w + 4, cloud_h - 14, 4, fill=1, stroke=0)
            c.setFillColor(CREAM)
            c.setFont("Avenir-Demi", 7.4)
            c.drawString(cx + 4, cloud_y + 28, title)
            c.setFillColor(HexColor("#D5E6E1"))
            c.setFont("Avenir", 6.6)
            c.drawString(cx + 4, cloud_y + 16, sub)
        else:
            c.setFillColor(TEAL)
            c.setFont("Avenir-Demi", 7.4)
            c.drawString(cx, cloud_y + 28, title)
            c.setFillColor(MUTED)
            c.setFont("Avenir", 6.6)
            c.drawString(cx, cloud_y + 14, sub)


def page_features(c: canvas.Canvas) -> None:
    begin_page(c, "Hospitality", "features", "Hospitality features")
    y = H - 50
    y -= section_title(c, "Operations", "The question is the 15:00 arrival", y)
    y -= 8
    lead = (
        "A property manager is not asking whether the network is secure in the abstract. "
        "The question is whether this apartment is fit for the guest who arrives at 15:00. "
        "The gateway takes the turnover window from the property-management calendar and spends it on a sweep."
    )
    y -= draw_para(c, lead, S["body"], LEFT, y, WIDTH)
    y -= 12
    y -= draw_turnover(c, LEFT, y, WIDTH)
    y -= 8
    y -= draw_para(
        c,
        "Figure 5. The audit itself is a quality target of under five minutes, inside an 11:00–15:00 turnover. "
        "The rest of the window is physical cleaning. The health score is due before the next guest.",
        S["caption"],
        LEFT,
        y,
        WIDTH,
    )
    y -= 12
    features = [
        {
            "kicker": "01",
            "title": "Turnover sanitization",
            "body": "Sync with Guesty, Smoobu, Beds24, or an iCal feed. During the cleaning window the gateway checks IoT firmware and configuration drift, clears guest pairing caches, and looks for a BLE beacon that survived checkout. The output is a turnover health score.",
            "accent": TEAL,
        },
        {
            "kicker": "02",
            "title": "Two VLANs, by default",
            "body": "Phones and laptops land on a guest VLAN. Locks, keypads, thermostats, and internal sensors stay on a management VLAN the guest segment cannot scan. That is the dashed path and the solid path in Figure 1.",
            "accent": AMBER,
        },
        {
            "kicker": "03",
            "title": "Implants left behind",
            "body": "Foreign hardware on a socket or an Ethernet jack: a hidden radio, a sniffer, a high-draw device. The radio scan covers the first. The puck, in phase 2, covers the draw.",
            "accent": CRIMSON,
        },
        {
            "kicker": "04",
            "title": "Cyber-clean stay",
            "body": "A signed PDF and a listing badge that the room was swept before check-in. Aimed at corporate and executive guests, where a higher average daily rate is the commercial point of the certificate.",
            "accent": NAVY,
        },
    ]
    y -= row_of_cards(c, features, LEFT, y, WIDTH, 2, gap=8)
    y -= 2
    kpis = [
        ("< 0.5%", "False-alarm target"),
        ("< 5 min", "Audit-time target"),
        ("Unchanged", "Guest bandwidth target"),
    ]
    box_w = (WIDTH - 16) / 3
    for i, (value, label) in enumerate(kpis):
        bx = LEFT + i * (box_w + 8)
        c.setFillColor(NAVY)
        c.roundRect(bx, y - 48, box_w, 48, 5, fill=1, stroke=0)
        c.setFillColor(CREAM)
        c.setFont("Avenir-Demi", 13)
        c.drawString(bx + 10, y - 22, value)
        c.setFont("Avenir", 7.5)
        c.setFillColor(HexColor("#D5E6E1"))
        c.drawString(bx + 10, y - 36, label)
    y -= 58
    y -= draw_para(
        c,
        "Quality targets for the pilot. They are design goals from the project overview, not measured results.",
        S["caption"],
        LEFT,
        y,
        WIDTH,
    )
    y -= 12
    y -= draw_sweep(c, LEFT, y, WIDTH)
    finish_page(c, y, "features")


def draw_turnover(c: canvas.Canvas, x: float, y_top: float, width: float) -> float:
    height = 92
    y = y_top - height
    c.setFillColor(CARD)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.roundRect(x, y, width, height, 6, fill=1, stroke=1)
    c.setFillColor(TEAL)
    c.setFont("Avenir-Demi", 7.5)
    c.drawString(x + 12, y + height - 16, "TURNOVER WINDOW")
    c.setFillColor(MUTED)
    c.setFont("Avenir", 7.5)
    c.drawRightString(x + width - 12, y + height - 16, "Triggered by the PMS calendar")

    axis_y = y + 40
    x0 = x + 28
    x1 = x + width - 28
    c.setStrokeColor(RULE)
    c.setLineWidth(2)
    c.line(x0, axis_y, x1, axis_y)

    def at(frac):
        return x0 + frac * (x1 - x0)

    # window 11:00 to 15:00 mapped across the axis, with a little pad
    c.setFillColor(TEAL_SOFT)
    c.rect(at(0.08), axis_y - 7, at(0.92) - at(0.08), 14, fill=1, stroke=0)
    c.setFillColor(TEAL_LINE)
    c.roundRect(at(0.08), axis_y - 7, at(0.22) - at(0.08), 14, 2, fill=1, stroke=0)

    marks = [
        (0.08, "11:00", "Check-out"),
        (0.18, "Audit", "< 5 min target"),
        (0.55, "Cleaning", "Score due in this window"),
        (0.92, "15:00", "Check-in"),
    ]
    for frac, title, sub in marks:
        mx = at(frac)
        c.setFillColor(NAVY if title != "Audit" else TEAL)
        c.circle(mx, axis_y, 3.2, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont("Avenir-Demi", 7.5)
        c.drawCentredString(mx, axis_y + 16, title)
        c.setFillColor(MUTED)
        c.setFont("Avenir", 6.6)
        c.drawCentredString(mx, axis_y - 22, sub)
    return height


def page_comparison(c: canvas.Canvas) -> None:
    begin_page(c, "Comparison", "comparison", "Modem and kit")
    y = H - 50
    y -= section_title(c, "Capability", "Where a mesh router stops", y)
    y -= 8
    lead = (
        "Consumer mesh gear can pass packets and, with care, separate an SSID. "
        "The hospitality job adds a radio, a side channel, a calendar, a fleet view, and a privacy rule. "
        "The table uses the words of the project overview."
    )
    y -= draw_para(c, lead, S["body"], LEFT, y, WIDTH)
    y -= 14
    header = [
        Paragraph("Capability", S["th"]),
        Paragraph("Standard ISP modem or consumer mesh", S["th"]),
        Paragraph("Hospitality security kit", S["th"]),
    ]
    rows_src = [
        ("Guest and IoT segmentation", "Manual, and easy to misconfigure", "Automatic, and on by default"),
        ("Silent local compute", "No side-channel measurement", "Power and thermal profiling from the puck"),
        ("Bluetooth and RF implants", "No radio visibility", "Dedicated multi-band scan"),
        ("Turnover and PMS", "No property-calendar link", "Guesty, Smoobu, Beds24, and iCal"),
        ("Fleet of 50 or more", "A separate app per router", "One multi-tenant console"),
        ("Guest privacy, GDPR / LOPD", "No privacy design for this use", "Metadata only, privacy by design"),
    ]
    data = [header]
    for cap, modem, kit in rows_src:
        data.append(
            [
                Paragraph(cap, S["td_strong"]),
                Paragraph(modem, S["td"]),
                Paragraph(kit, S["td"]),
            ]
        )
    col_w = [150, 180, 193]
    table = Table(data, colWidths=col_w, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("BACKGROUND", (2, 1), (2, -1), TEAL_SOFT),
                ("BACKGROUND", (0, 1), (1, -1), white),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LINEBELOW", (0, 0), (-1, -2), 0.3, RULE),
                ("LINEBEFORE", (2, 1), (2, -1), 0.4, TEAL_LINE),
            ]
        )
    )
    _tw, th = table.wrap(WIDTH, 700)
    table.drawOn(c, LEFT, y - th)
    y -= th + 14
    y -= draw_para(
        c,
        "Figure 6. Qualitative comparison from the project overview. Segmentation on a consumer router exists; "
        "it is not the default, and it is not tied to a checkout clock. Privacy on a consumer router is uncontrolled "
        "for this use, which is a different claim from “the router reads guest mail.”",
        S["caption"],
        LEFT,
        y,
        WIDTH,
    )
    y -= 16
    # three closing points
    points = [
        ("Metadata is the inspection", "The kit’s network engine reads volumes, headers, ports, and DNS. Opening guest payloads is outside the product."),
        ("The fleet is the buyer", "A manager with one flat can live in a router app. A manager with fifty flats cannot. The console is the thing they pay the monthly fee for."),
        ("Quarantine stays human-gated", "Automated isolation of a guest device is available. Taking a television or a lock offline in the middle of a stay waits for a person, so a false alarm does not cancel a checkout."),
    ]
    y -= row_of_cards(
        c,
        [{"kicker": "Implication", "title": t, "body": b, "accent": TEAL} for t, b in points],
        LEFT,
        y,
        WIDTH,
        3,
        gap=8,
    )
    y -= 6
    c.setFillColor(NAVY)
    c.setFont("Avenir-Demi", 9)
    c.drawString(LEFT, y - 4, "The same six rows, in Figure 1")
    y -= 16
    y -= draw_figure_links(c, LEFT, y, WIDTH)
    finish_page(c, y, "comparison")


def page_privacy(c: canvas.Canvas) -> None:
    begin_page(c, "Privacy", "privacy", "Privacy and the certificate")
    y = H - 50
    y -= section_title(c, "Governance", "The constraint that makes the badge possible", y)
    y -= 8
    lead = (
        "Airbnb’s 2024 ban on indoor cameras reset what a guest will tolerate in a rental. "
        "Any product that watches a room with a lens is unsellable in this market. "
        "The kit is specified so the certificate on the listing and the rule in the gateway are the same rule."
    )
    y -= draw_para(c, lead, S["body"], LEFT, y, WIDTH)
    y -= 12
    principles = [
        {
            "kicker": "Inspection",
            "title": "Metadata only",
            "body": "Flow volumes, packet headers, port destinations, and DNS lookups. The contents of guest traffic are not reconstructed and are not stored.",
            "accent": TEAL,
        },
        {
            "kicker": "Regulation",
            "title": "GDPR Article 25, and LOPD",
            "body": "Privacy by design and by default. No audio, no video, and no browsing history. The regulatory review still has to confirm the EU Cyber Resilience Act and Spanish LOPDGDD. That review is a next step, not a completed opinion.",
            "accent": TEAL,
        },
        {
            "kicker": "Processing",
            "title": "Correlation stays in the room",
            "body": "The engine that fuses network, radio, and puck runs on the gateway. The cloud receives a status: green, amber, or red. It does not receive a packet capture of the stay.",
            "accent": NAVY,
        },
        {
            "kicker": "Retention",
            "title": "Purge at checkout",
            "body": "Network logs end with the stay. The next guest does not inherit a dossier, and the manager does not accumulate one. Tenant isolation is a retention rule, not only a VLAN.",
            "accent": NAVY,
        },
    ]
    y -= row_of_cards(c, principles, LEFT, y, WIDTH, 2, gap=8)
    y -= 4
    # certificate panel
    panel_h = 168
    c.setFillColor(NAVY)
    c.roundRect(LEFT, y - panel_h, WIDTH, panel_h, 8, fill=1, stroke=0)
    c.setFillColor(HexColor("#D5E6E1"))
    c.setFont("Avenir-Demi", 8)
    c.drawString(LEFT + 16, y - 20, "VERIFIED CYBER-CLEAN STAY")
    c.setFillColor(CREAM)
    c.setFont("Charter-Bold", 14)
    c.drawString(LEFT + 16, y - 42, "A certificate the host can show")
    body = (
        "After the turnover sweep the gateway produces a digitally signed PDF and a badge for the listing. "
        "The badge is aimed at corporate travelers and executive guests, where the manager’s case for a higher "
        "average daily rate needs a document, not a slogan. The signature covers the health score for that "
        "turnover: devices checked, pairing caches cleared, no surviving rogue beacon. It does not describe the guest."
    )
    draw_para(
        c,
        body,
        ParagraphStyle(
            "cert",
            fontName="Charter",
            fontSize=9.5,
            leading=13.0,
            textColor=CREAM,
            alignment=TA_LEFT,
        ),
        LEFT + 16,
        y - 54,
        WIDTH - 200,
    )
    # mini certificate card
    cx = LEFT + WIDTH - 168
    cy = y - panel_h + 22
    c.setFillColor(CREAM)
    c.roundRect(cx, cy, 140, panel_h - 44, 4, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(cx, cy + panel_h - 44 - 8, 140, 8, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Avenir-Demi", 7)
    c.drawString(cx + 10, cy + panel_h - 68, "TURNOVER HEALTH")
    c.setFont("Charter-Bold", 12)
    c.drawString(cx + 10, cy + panel_h - 88, "Clear to arrive")
    c.setFont("Avenir", 7)
    c.setFillColor(MUTED)
    lines = ["Apartment  ·  4B", "Window  ·  11:00–15:00", "IoT drift  ·  none", "Rogue BLE  ·  none", "Signed at the gateway"]
    for i, line in enumerate(lines):
        c.drawString(cx + 10, cy + panel_h - 108 - i * 11, line)
    y -= panel_h + 12
    y -= draw_para(
        c,
        "Figure 7. Illustrative certificate. The fields are the ones the turnover engine is specified to know. "
        "They are not a sample from a pilot.",
        S["caption"],
        LEFT,
        y,
        WIDTH,
    )
    y -= 12
    c.setFillColor(NAVY)
    c.setFont("Avenir-Demi", 9)
    c.drawString(LEFT, y - 4, "Where a record lives")
    y -= 16
    y -= draw_data_split(c, LEFT, y, WIDTH)
    finish_page(c, y, "privacy")


def page_commercial(c: canvas.Canvas, pricing: Path, portfolio: Path) -> None:
    begin_page(c, "Commercial", "commercial", "Go to market")
    y = H - 50
    y -= section_title(c, "Model", "Who already pays for a box in the flat", y)
    y -= 6
    segments = [
        ("STR managers", "Professional hosts with 5 to 100 or more apartments in Madrid, Barcelona, London, Paris."),
        ("Boutique hotels", "Independent houses of 10 to 60 rooms, without an in-house security team."),
        ("Serviced apartments", "Corporate housing, where the guest is handling commercial data."),
    ]
    col_w = (WIDTH - 16) / 3
    for i, (title, body) in enumerate(segments):
        sx = LEFT + i * (col_w + 8)
        c.setFillColor(CARD)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.5)
        c.roundRect(sx, y - 62, col_w, 62, 5, fill=1, stroke=1)
        c.setFillColor(TEAL)
        c.rect(sx, y - 62, 3, 62, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont("Avenir-Demi", 8.5)
        c.drawString(sx + 10, y - 16, title)
        draw_para(c, body, S["caption"], sx + 10, y - 22, col_w - 20)
    y -= 74
    intro = (
        "Managers already rent hardware for the same doorway. Noise and occupancy monitors (Minut, NoiseAware) "
        "run €10–€15 per door per month. Smart locks (RemoteLock, Nuki, Yale) run €5–€10. "
        "The kit is priced in that band, and it sells a liability story those products do not: the previous guest’s compromise."
    )
    y -= draw_para(c, intro, S["body"], LEFT, y, WIDTH)
    y -= 8
    ih = draw_figure(c, pricing, LEFT, y, WIDTH, 150)
    y -= ih + 4
    y -= draw_para(
        c,
        "Figure 8. Monthly ranges as stated in the project overview. Comparables are published list bands for those categories, quoted here exactly as the overview quotes them.",
        S["caption"],
        LEFT,
        y,
        WIDTH,
    )
    y -= 10
    ih = draw_figure(c, portfolio, LEFT, y, WIDTH, 200)
    y -= ih + 4
    fifty_lo = annual(50, 14)
    fifty_hi = annual(50, 19)
    hw_lo, hw_hi = 50 * 99, 50 * 149
    y -= draw_para(
        c,
        f"Figure 9. Annual subscription is properties × monthly price × 12, at the two ends of €14–€19. "
        f"Hardware is separate: €99–€149 per gateway, so a 50-apartment portfolio is €{hw_lo:,.0f}–€{hw_hi:,.0f} once, "
        f"against €{fifty_lo:,.0f}–€{fifty_hi:,.0f} of subscription per year. "
        f"An annual commitment can waive the upfront hardware fee. "
        f"Gross margin on SaaS is a target above 80%. Churn is a target under 5%, on the argument that the audit sits inside daily turnover. Neither figure is a measured result.",
        S["caption"],
        LEFT,
        y,
        WIDTH,
    )
    y -= 8
    y -= draw_para(
        c,
        "Acquisition in the overview runs through regional manager associations (FEVITUR in Spain), partnerships with the PMS platforms above, and insurers who already price guest-damage liability.",
        S["small"],
        LEFT,
        y,
        WIDTH,
    )
    y -= 10
    y -= draw_money_tiles(c, LEFT, y, WIDTH)
    finish_page(c, y, "commercial")


def page_thesis(c: canvas.Canvas) -> None:
    begin_page(c, "Thesis", "thesis", "PMBOK and next steps")
    y = H - 50
    y -= section_title(c, "EAE Madrid", "What the thesis has to manage", y)
    y -= 8
    lead = (
        "Scoping the kit to hospitality gives each PMBOK knowledge area a real stakeholder and a real clock. "
        "The clock is the turnover. The buyer is a manager. The user who must be protected from the product is the guest."
    )
    y -= draw_para(c, lead, S["body"], LEFT, y, WIDTH)
    y -= 10
    areas = [
        ("Stakeholders", "Property managers buy it. Guests are the privacy constraint. Cleaning staff run the turnover. OTAs set the camera rules. European regulators set the rest."),
        ("Scope", "Phase 1 covers managed LAN enforcement, network telemetry, PMS turnover and the fleet dashboard. Evaluate BLE and power telemetry for incremental detection value."),
        ("Schedule and cost", "Prototype, firmware, cloud backend, then a 20-unit pilot on Madrid rentals. Costing is bottom-up from the bill of materials, with a cash-flow and a break-even still to build."),
        ("Quality", "Measure false alerts per property-week, audit time and guest throughput. Page 11 gives the pilot acceptance checks."),
        ("Risk", "A bad policy must not kill a guest’s call. Mitigation: a person authorizes quarantine of a live device. A privacy miss is mitigated by metadata-only design. Supply lead time is mitigated by commercial single-board computers."),
        ("Procurement", "OEM contract manufacturing against white-label assembly. Cloud hosting in EU regions. An external penetration test before the pilot is called a pilot."),
    ]
    row_h_pad = 4
    for title, body in areas:
        bh = para_height(body, S["small"], WIDTH - 130)
        rh = max(28, bh + 10)
        c.setFillColor(CARD)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.4)
        c.roundRect(LEFT, y - rh, WIDTH, rh, 4, fill=1, stroke=1)
        c.setFillColor(TEAL)
        c.setFont("Avenir-Demi", 8)
        c.drawString(LEFT + 8, y - 14, title)
        draw_para(c, body, S["small"], LEFT + 118, y - 6, WIDTH - 130)
        y -= rh + row_h_pad
    y -= 8
    c.setFillColor(NAVY)
    c.setFont("Avenir-Demi", 9)
    c.drawString(LEFT, y - 4, "Next steps, in the order the overview gives them")
    y -= 16
    steps = [
        ("1", "Charter", "Phase 1 boundaries and the WBS dictionary."),
        ("2", "Architecture", "Managed LAN enforcement and pilot specification (page 11)."),
        ("3", "Mockups", "Manager dashboard and the PMS webhook."),
        ("4", "Business case", "Three-year cash flow, CAC / LTV, price tests at 10, 50, and 200 properties."),
        ("5", "PMBOK set", "Project plan, risk register, communication matrix, RACI."),
        ("6", "Regulation", "EU Cyber Resilience Act and Spanish LOPDGDD."),
    ]
    col = 3
    gap = 8
    cw = (WIDTH - gap * (col - 1)) / col
    rh = 58
    for i, (num, title, body) in enumerate(steps):
        r, cix = divmod(i, col)
        sx = LEFT + cix * (cw + gap)
        sy = y - r * (rh + gap)
        c.setFillColor(CARD)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.4)
        c.roundRect(sx, sy - rh, cw, rh, 4, fill=1, stroke=1)
        c.setFillColor(TEAL)
        c.setFont("Avenir-Demi", 11)
        c.drawString(sx + 8, sy - 16, num)
        c.setFillColor(NAVY)
        c.setFont("Avenir-Demi", 8.5)
        c.drawString(sx + 24, sy - 16, title)
        draw_para(c, body, S["caption"], sx + 8, sy - 22, cw - 16)
    y -= 2 * (rh + gap) + 6
    y -= draw_phases(c, LEFT, y, WIDTH)
    y -= 8
    y -= draw_para(
        c,
        "Prepared from iot-security-kit-ai-sleeper-agents-overview.md. "
        "Figures 2 and 3 are schematics of the supplied floor plan. Figure 7 is a specimen certificate. "
        "Figures 8 and 9 plot the price ranges stated in the overview. Figure 1 is the supplied setup drawing.",
        S["caption"],
        LEFT,
        y,
        WIDTH,
    )
    finish_page(c, y, "thesis")


def page_implementation(c: canvas.Canvas) -> None:
    begin_page(c, "Pilot implementation", "implementation", "Recommended pilot implementation")
    y = H - 50
    y -= section_title(c, "November 2026 research update", "Active LAN protection", y)
    y -= 12
    y -= draw_para(
        c,
        "Pilot objective. Contain suspicious behavior from a property-owned streaming device while guest internet "
        "and normal door access keep working. Start with one apartment and a managed network before expanding the pilot.",
        S["body"], LEFT, y, WIDTH,
    )
    sections = [
        ("Enforce policy on the LAN",
         "Separate guests, entertainment devices and critical property devices such as locks and thermostats. "
         "Restrict infrastructure administration to authorized operators. Route traffic between zones through the gateway "
         "or integrate with a managed router, switch and access point. Same-VLAN switching can bypass a routed firewall. "
         "Use switch or access-point isolation where peer traffic must be blocked. Test IPv4 and IPv6 and narrowly scope "
         "any casting or Matter/Thread discovery exceptions."),
        ("Detect and contain with network evidence",
         "Inventory approved property devices and set expected outbound access per device role. Alert on policy violations, "
         "unexpected outbound flows and changes to router, DNS or captive portal settings where management telemetry is available. "
         "Use flow timing, volume and firewall decisions when hostname visibility is unavailable. Block prohibited paths by policy "
         "immediately. Keep wider device quarantine operator-authorized, reversible and logged. BLE and power readings add context "
         "for investigation. Measure their incremental detection value before expanding sensor scope."),
        ("Make turnover checks actionable",
         "Use the property management calendar to trigger checks for inventory changes, configuration drift, active quarantine "
         "and isolation status. Show each check, its result and any action staff should take before check-in. Capture firmware "
         "or pairing status where supported by device integrations. Keep raw telemetry local with limited retention and send "
         "only the necessary status and events to the fleet console."),
        ("Measure performance before rollout",
         "Exercise the policy with benign test traffic representing a prohibited television-to-lock connection and unusual egress. "
         "Verify continued door access, guest internet, streaming, updates and permitted casting. Measure time to alert, "
         "false alerts per property-week, checkout audit duration, guest throughput and quarantine rollback success."),
        ("Plan for EU product obligations",
         "If the kit is placed on the EU market, assess whether its core functionality falls into the Cyber Resilience Act "
         "Class II firewall or intrusion detection and prevention category. Budget for the applicable conformity assessment. "
         "Design for signed updates, a component inventory, vulnerability handling and incident reporting."),
    ]
    for heading, body in sections:
        y -= 15
        c.setFillColor(TEAL)
        c.setFont("Avenir-Demi", 11)
        c.drawString(LEFT, y - 10, heading)
        y -= 17
        y -= draw_para(c, body, S["body"], LEFT, y, WIDTH)
    y -= 16
    y -= draw_para(
        c,
        'Evidence and primary sources are listed in the companion <i>Cybersecurity Evidence Compendium</i>.',
        S["caption"], LEFT, y, WIDTH,
    )
    finish_page(c, y, "implementation")


def main() -> None:
    extract_fonts()
    styles()
    floorplan = FIG / "setup-floorplan.png"
    signals = build_signal_chart()
    pricing = build_pricing_chart()
    portfolio = build_portfolio_chart()
    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle("IoT Security Kit Against Sleeper AI Agents")
    c.setAuthor("EAE Madrid — Master in Project Management")
    c.setSubject("Hospitality and short-term rental edition. Project overview, November 2026.")
    c.setCreator("scripts/build_overview_pdf.py")
    page_cover(c)
    page_setup(c, floorplan)
    page_incident(c, signals)
    page_problem(c)
    page_architecture(c)
    page_features(c)
    page_comparison(c)
    page_privacy(c)
    page_commercial(c, pricing, portfolio)
    page_thesis(c)
    page_implementation(c)
    c.save()
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
