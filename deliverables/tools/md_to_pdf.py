#!/usr/bin/env python3
"""Render ServiceNow-Impact-Australia-Client-Brief.md to a print-ready A4 PDF.

reportlab Platypus is used (rather than an HTML->PDF engine) so line spacing,
pagination and table splitting are exact.

Supports the Markdown subset used in the brief: h1-h4, paragraphs, bold/italic/
code spans, bullet lists (one nesting level), numbered lists, pipe tables,
blockquote call-outs, thematic breaks, and the single ```mermaid fence (replaced
with a styled layered diagram).

Run:  /home/user/pdfenv/bin/python tools/md_to_pdf.py
"""
import os
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, Flowable, HRFlowable,
                                ListFlowable, ListItem, NextPageTemplate,
                                PageBreak, PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "ServiceNow-Impact-Australia-Client-Brief.md")
OUT = os.path.join(ROOT, "artifacts", "ServiceNow-Impact-Australia-Client-Brief.pdf")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
NAVY = colors.HexColor("#03213f")
BLUE = colors.HexColor("#1f4e79")
GREEN = colors.HexColor("#03754d")
LIGHT_GREEN = colors.HexColor("#e6f4ee")
GREY = colors.HexColor("#f2f4f7")
MID = colors.HexColor("#5c6b7a")
RULE = colors.HexColor("#d9e2ec")
DOC_TITLE = "ServiceNow Impact — Client Briefing (Australia release)"

pdfmetrics.registerFont(TTFont("DejaVu", FONT_DIR + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", FONT_DIR + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Mono", FONT_DIR + "DejaVuSansMono.ttf"))
pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold",
                              italic="DejaVu", boldItalic="DejaVu-Bold")

S = {
    "h1": ParagraphStyle("h1", fontName="DejaVu-Bold", fontSize=25, leading=30,
                         textColor=NAVY, spaceAfter=6),
    "cover_sub": ParagraphStyle("cover_sub", fontName="DejaVu-Bold", fontSize=12.5,
                                leading=17, textColor=GREEN, spaceAfter=10),
    "h2": ParagraphStyle("h2", fontName="DejaVu-Bold", fontSize=14.5, leading=18,
                         textColor=colors.white, backColor=NAVY,
                         borderPadding=(6, 8, 7, 8), spaceBefore=16, spaceAfter=10),
    "h3": ParagraphStyle("h3", fontName="DejaVu-Bold", fontSize=11.8, leading=15,
                         textColor=BLUE, spaceBefore=11, spaceAfter=4),
    "tochead": ParagraphStyle("tochead", fontName="DejaVu-Bold", fontSize=11.8,
                              leading=15, textColor=BLUE, spaceAfter=6),
    "h4": ParagraphStyle("h4", fontName="DejaVu-Bold", fontSize=10.2, leading=13.5,
                         textColor=GREEN, spaceBefore=8, spaceAfter=3),
    "body": ParagraphStyle("body", fontName="DejaVu", fontSize=9.3, leading=13.2,
                           textColor=NAVY, spaceAfter=6, alignment=TA_LEFT),
    "bullet": ParagraphStyle("bullet", fontName="DejaVu", fontSize=9.3, leading=12.8,
                             textColor=NAVY, spaceAfter=3.5, splitLongWords=1),
    "bullet2": ParagraphStyle("bullet2", fontName="DejaVu", fontSize=8.8, leading=12.2,
                              textColor=NAVY, leftIndent=12, spaceAfter=3),
    "num": ParagraphStyle("num", fontName="DejaVu", fontSize=9.3, leading=12.8,
                          textColor=NAVY, spaceAfter=3.5),
    "th": ParagraphStyle("th", fontName="DejaVu-Bold", fontSize=8, leading=10.2,
                         textColor=colors.white),
    "td": ParagraphStyle("td", fontName="DejaVu", fontSize=8, leading=10.4, textColor=NAVY),
}
MARGIN_X, TOP, BOTTOM = 40, 52, 46
FRAME_W = A4[0] - 2 * MARGIN_X


def inline(text):
    t = str(text)
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # stash code spans first: their contents must never be parsed as emphasis
    # (e.g. `dc-*-install.md`, `sn_impact_common.Impact Admin`)
    codes = []

    def _stash(m):
        codes.append(m.group(1))
        return "\x00%d\x00" % (len(codes) - 1)

    t = re.sub(r"`([^`]+)`", _stash, t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<i>\1</i>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", t)
    t = re.sub(r"\x00(\d+)\x00",
               lambda m: '<font name="DejaVu-Mono" size="8.4">%s</font>' % codes[int(m.group(1))], t)
    return t


def plain(text):
    return re.sub(r"[*`]", "", str(text)).strip()


def is_table_row(line):
    s = line.strip()
    return s.startswith("|") and s.endswith("|")


def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_sep_row(line):
    return is_table_row(line) and all(re.fullmatch(r":?-{2,}:?", c) for c in split_row(line))


def build_table(rows, header=True):
    cols = max(len(r) for r in rows)
    body_font = 8.2 if cols <= 2 else (7.8 if cols == 3 else (7.2 if cols == 4 else 6.8))
    th = ParagraphStyle("th%d" % cols, parent=S["th"], fontSize=body_font,
                        leading=body_font * 1.28)
    td = ParagraphStyle("td%d" % cols, parent=S["td"], fontSize=body_font,
                        leading=body_font * 1.32)
    td_lead = ParagraphStyle("tdl%d" % cols, parent=td, textColor=BLUE,
                             fontName="DejaVu-Bold")
    weights = []
    for c in range(cols):
        longest = max((len(plain(r[c])) if c < len(r) else 0) for r in rows) or 1
        weights.append(min(2.6, max(0.62, (longest ** 0.5) / 8.0)))
    total = sum(weights)
    widths = [max(34.0, FRAME_W * w / total) for w in weights]
    scale = FRAME_W / sum(widths)
    widths = [w * scale for w in widths]

    data = []
    for ri, row in enumerate(rows):
        cells = []
        for ci in range(cols):
            raw = row[ci] if ci < len(row) else ""
            style = td_lead if (not header and ci == 0) else (th if (header and ri == 0) else td)
            cells.append(Paragraph(inline(raw), style))
        data.append(cells)

    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    cmds = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b6c4d2")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 3.5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3.5),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if header:
        cmds.append(("BACKGROUND", (0, 0), (-1, 0), BLUE))
        for ri in range(1, len(data)):
            cmds.append(("BACKGROUND", (0, ri), (-1, ri), colors.white if ri % 2 else GREY))
    else:
        for ri in range(len(data)):
            cmds.append(("BACKGROUND", (0, ri), (-1, ri), colors.white if ri % 2 else GREY))
    t.setStyle(TableStyle(cmds))
    return t


def mermaid_diagram():
    col_defs = [
        ("1. Your estate (consumer instance)", NAVY, [
            "Impact Store Application — Impact Common / Content / Health",
            "Platform Health — Scan Engine, HealthScan, real-time prevention, AI fixes",
            "Value data collection — Performance Analytics packs per product",
            "Users & roles — Platform Owner, Admin, Developer, Team Lead, Executive",
            "Instance Observer — off-instance observability",
        ]),
        ("2. Secure sync layer", GREEN, [
            "Service Bridge — automated registration (preferred) or manual registration (regulated / GCC)",
            "Inbound + outbound payloads; connection status must read Active replication",
        ]),
        ("3. Impact Delivery Instance (ServiceNow-hosted)", BLUE, [
            "Impact Squad — CSM / CSE / Platform Architect / SAM",
            "Activity Center — conversations, tasks, files, calendar",
            "Value management — objectives, outcomes, value reports",
            "Catalogues — Accelerators, Initiatives, PARs, Capability Maps, Training",
        ]),
        ("4. Business outcomes", NAVY, [
            "Adoption · Platform health · Performance & availability · Value realised · Upgrade readiness",
            "Cadence: quarterly reviews moving Foundations → Steady State",
        ]),
    ]
    th = ParagraphStyle("dth", fontName="DejaVu-Bold", fontSize=8.2, leading=10.4,
                        textColor=colors.white)
    tb = ParagraphStyle("dtb", fontName="DejaVu", fontSize=7.4, leading=10.0, textColor=NAVY)
    head = [Paragraph(c[0], th) for c in col_defs]
    body = [Paragraph("<br/>".join("• " + inline(x) for x in c[2]), tb) for c in col_defs]
    widths = [FRAME_W * w for w in (0.30, 0.21, 0.29, 0.20)]
    t = Table([head, body], colWidths=widths, hAlign="LEFT")
    cmds = [("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]
    for i, (_t, col, _b) in enumerate(col_defs):
        cmds.append(("BACKGROUND", (i, 0), (i, 0), col))
        cmds.append(("BACKGROUND", (i, 1), (i, 1), LIGHT_GREEN))
    t.setStyle(TableStyle(cmds))
    return t


def callout(text):
    p = Paragraph(inline(text), ParagraphStyle("call", fontName="DejaVu", fontSize=9.2,
                                               leading=13, textColor=NAVY))
    t = Table([[p]], colWidths=[FRAME_W], hAlign="LEFT")
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), GREY),
                           ("LINEBEFORE", (0, 0), (0, -1), 2.4, GREEN),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 6),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t


class Doc(BaseDocTemplate):
    def __init__(self, path, **kw):
        BaseDocTemplate.__init__(
            self, path, pagesize=A4, leftMargin=MARGIN_X, rightMargin=MARGIN_X,
            topMargin=TOP, bottomMargin=BOTTOM,
            title="ServiceNow Impact — Client Briefing",
            author="ServiceNow architecture & advisory team",
            subject="ServiceNow Impact on the Australia release", **kw)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="body")
        self.addPageTemplates([PageTemplate(id="Body", frames=[frame], onPage=self.footer)])

    def footer(self, c, doc):
        c.saveState()
        c.setStrokeColor(RULE)
        c.setLineWidth(0.5)
        c.line(MARGIN_X, BOTTOM - 12, A4[0] - MARGIN_X, BOTTOM - 12)
        c.setFont("DejaVu", 7.4)
        c.setFillColor(MID)
        c.drawString(MARGIN_X, BOTTOM - 24, DOC_TITLE)
        c.drawRightString(A4[0] - MARGIN_X, BOTTOM - 24, "Page %d" % self.page)
        c.restoreState()

    def afterFlowable(self, flowable):
        if not isinstance(flowable, Paragraph):
            return
        name = flowable.style.name
        text = plain(flowable.getPlainText())
        if name == "h2":
            key = "h2-%s" % self.seq.nextf("h2")
            self.canv.bookmarkPage(key)
            self.notify("TOCEntry", (0, text, self.page, key))
            self.canv.addOutlineEntry(text, key, level=0, closed=False)
        elif name == "h3":
            key = "h3-%s" % self.seq.nextf("h3")
            self.canv.bookmarkPage(key)
            self.notify("TOCEntry", (1, text, self.page, key))
            self.canv.addOutlineEntry(text, key, level=1, closed=True)


def parse_markdown(lines):
    story, i, n = [], 0, len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if stripped.startswith("```"):
            info = stripped[3:].strip().lower()
            block, i = [], i + 1
            while i < n and not lines[i].strip().startswith("```"):
                block.append(lines[i]); i += 1
            i += 1
            is_mermaid = info.startswith("mermaid") or (block and re.match(r"^(flowchart|graph)\b", block[0].strip()))
            story += [Spacer(1, 4), mermaid_diagram() if is_mermaid else callout("\n".join(block)), Spacer(1, 8)]
            continue
        if re.fullmatch(r"-{3,}", stripped):
            story += [Spacer(1, 5), HRFlowable(width="100%", thickness=0.6, color=RULE, spaceAfter=6)]
            i += 1
            continue
        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            if level >= 2:
                style = {2: "h2", 3: "h3", 4: "h4"}.get(level, "h4")
                story.append(Paragraph(inline(stripped[level:].strip()), S[style]))
                i += 1
                continue
        if stripped.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip()); i += 1
            story += [callout(" ".join(buf)), Spacer(1, 6)]
            continue
        if is_table_row(line):
            rows = []
            while i < n and is_table_row(lines[i]):
                if not is_sep_row(lines[i]):
                    rows.append(split_row(lines[i]))
                i += 1
            header = bool(rows) and any(plain(c) for c in rows[0])
            story += [Spacer(1, 2), build_table(rows, header=header), Spacer(1, 9)]
            continue
        if re.match(r"^(\s*)([-*])\s+", line):
            items = []
            while i < n:
                mm = re.match(r"^(\s*)([-*])\s+(.*)$", lines[i])
                if not mm:
                    break
                items.append((len(mm.group(1)), mm.group(3)))
                i += 1
            for indent, txt in items:
                style = "bullet2" if indent >= 2 else "bullet"
                story.append(Paragraph(inline(txt), S[style],
                                       bulletText="•" if indent < 2 else "–"))
            story.append(Spacer(1, 4))
            continue
        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(re.match(r"^\s*(\d+)\.\s+(.*)$", lines[i]).group(2)); i += 1
            story.append(ListFlowable(
                [ListItem(Paragraph(inline(t), S["num"]), leftIndent=16) for t in items],
                bulletType="1", start=1, leftIndent=16,
                bulletFontName="DejaVu-Bold", bulletFontSize=9.0))
            story.append(Spacer(1, 4))
            continue
        buf = [stripped]; i += 1
        while (i < n and lines[i].strip()
               and not lines[i].strip().startswith(("#", "|", ">", "-", "*", "```"))
               and not re.match(r"^\s*\d+\.\s+", lines[i])
               and not re.fullmatch(r"-{3,}", lines[i].strip())):
            buf.append(lines[i].strip()); i += 1
        story.append(Paragraph(inline(" ".join(buf)), S["body"]))
    return story


def build():
    raw = open(SRC, encoding="utf-8").read().splitlines()
    title = plain(raw[0].lstrip("# "))
    subtitle = next((plain(l) for l in raw[1:]
                     if l.strip() and not l.strip().startswith(("#", "|", ">"))), "")
    meta_start = next(k for k, l in enumerate(raw) if is_table_row(l))
    meta_end = meta_start
    while meta_end < len(raw) and is_table_row(raw[meta_end]):
        meta_end += 1
    meta_rows = [split_row(l) for l in raw[meta_start:meta_end] if not is_sep_row(l)]
    quote = next((l for l in raw[meta_end:] if l.strip().startswith(">")), "")

    story = [Spacer(1, 26), Paragraph(inline(title), S["h1"]),
             Paragraph(inline(subtitle), S["cover_sub"]),
             HRFlowable(width="100%", thickness=1.2, color=GREEN, spaceAfter=12),
             build_table(meta_rows, header=False), Spacer(1, 10)]
    if quote:
        story.append(callout(quote.strip()[1:].strip()))
    story += [Spacer(1, 22), Paragraph("Contents", S["tochead"])]
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("toc0", fontName="DejaVu-Bold", fontSize=9.6, leading=15.2,
                       textColor=NAVY, spaceBefore=3),
        ParagraphStyle("toc1", fontName="DejaVu", fontSize=8.6, leading=12.6,
                       textColor=colors.HexColor("#33475b"), leftIndent=14),
    ]
    # find where section 2 starts so the TOC page break lands after section 1's TOC
    body_start = next(k for k, l in enumerate(raw) if re.match(r"^##\s+1\.", l))
    story += [toc, PageBreak()]
    story += parse_markdown(raw[body_start:])
    Doc(OUT).multiBuild(story)


if __name__ == "__main__":
    build()
    from pypdf import PdfReader
    print("pages:", len(PdfReader(OUT).pages))
    print("wrote:", OUT)
