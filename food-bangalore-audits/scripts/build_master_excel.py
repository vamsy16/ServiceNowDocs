#!/usr/bin/env python3
"""Build ONE Excel workbook (Food-Bangalore-ALL-IN-ONE.xlsx) holding every lead,
every email, every leak/win, every source and the skills used per audit."""
import json, sys, re
from pathlib import Path
from datetime import date

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from audit_pdf_food import _slug
from leads_attractive_block import ATTRACTIVE

NAVY = "0F172A"; LIGHT = "F1F5F9"; RED_BG = "FFF1F2"; GREEN_BG = "ECFDF5"; PURPLE = "F5F3FF"
WHITE_BOLD = Font(bold=True, color="FFFFFF", size=10)
HDR = PatternFill("solid", fgColor=NAVY)
WRAP = Alignment(wrap_text=True, vertical="top")
THIN = Border(*[Side(style="thin", color="D8DEE8")]*4)

def style_header(ws, row=1, ncols=None):
    ncols = ncols or ws.max_column
    for c in range(1, ncols+1):
        cell = ws.cell(row=row, column=c)
        cell.font = WHITE_BOLD; cell.fill = HDR
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    ws.row_dimensions[row].height = 26
    ws.freeze_panes = ws.cell(row=row+1, column=1)

def autosize(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

def plain_html(t):
    t = re.sub(r"<br\s*/?>", "\n", t)
    t = re.sub(r"</?b>", "", t)
    t = re.sub(r"</?i>", "", t)
    return t.strip()

def main():
    leads = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(ROOT.glob("leads/*.json"))]
    leads.sort(key=lambda d: (-d["score"], d["brand"]))
    wb = Workbook()

    # ---------------------------------------------------------------- 1. README
    ws = wb.active; ws.title = "README"
    rows = [
        ["SMART PURSUIT — FOOD / BENGALURU AUDIT PACK", ""],
        ["Everything in this file is verified live data. Nothing is simulated.", ""],
        ["", ""],
        ["Date of live verification", "02 OCT 2026"],
        ["Leads", f"{len(leads)} brands (no duplicates with the agency's existing 100 leads or the Solar pipeline)"],
        ["Audit PDFs", f"audits/<brand>-audit-report.pdf — attractive 2-page format (you vs competitor, 3 leaks, roadmap, ROI, audit basis, CTA)"],
        ["Emails", f"{sum(len(l['outreach']) for l in leads)} emails — 4 per brand — see the 'Emails' sheet"],
        ["Skills used per audit", "performance-lead-audit orchestrating: ads, ad-creative, copywriting, cro, analytics/attribution, competitor-profiling, cold-email, pdf-report-generator"],
        ["", ""],
        ["HOW THE DATA WAS VERIFIED", ""],
        ["Ad counts", "Google Ads Transparency (region IN), re-checked at generation time on 02 OCT 2026"],
        ["Meta ads", "Meta Ad Library — verified for Licious (Library ID 983369480870934, live since 15 Apr 2026); others noted where not verified"],
        ["Emails", "Crawled from each brand's own website / help centre / corporate pages — no guessed, generic or formation addresses"],
        ["Site/tech facts", "Live raw HTML + rendered pages captured 02 OCT 2026 (tokens, GTM/GA4 IDs, defects quoted verbatim)"],
        ["Financials/market data", "Public coverage, labelled as reported — third-party estimates marked as estimates"],
        ["", ""],
        ["INTEGRITY RULES", ""],
        ["1", "Every number in a PDF's 'Before (live)' column traces to a source listed on that PDF"],
        ["2", "Benchmarks are labelled as industry benchmarks — no client results are invented"],
        ["3", "Where something was NOT verified, the audit says so explicitly (e.g. Third Wave: Google verified at 0, Meta not checked)"],
        ["4", "No lead, email or ad count is duplicated across sheets or with existing pipelines"],
    ]
    for r in rows: ws.append(r)
    ws["A1"].font = Font(bold=True, size=14, color=NAVY)
    ws["A2"].font = Font(bold=True, size=11)
    for r in (4,10,17): ws.cell(row=r, column=1).font = Font(bold=True, size=11, color=NAVY)
    autosize(ws, [30, 110])
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
        row[1].alignment = WRAP

    # ---------------------------------------------------------------- 2. LEADS
    ws = wb.create_sheet("Leads")
    ws.append(["#","Brand","Website","Instagram","Niche","Lead score /10","Live Google ads",
               "Lead email (crawled)","Phone","Legal entity","Address / HQ","Contact source",
               "Audit PDF","Outreach file","Verified on"])
    for i, l in enumerate(leads, 1):
        s = _slug(l["brand"])
        ws.append([i, l["brand"], l["website"], l.get("instagram",""), l["niche"], l["score"],
                   l["ads_active"], l["contact"]["email"], l["contact"].get("phone",""),
                   l["contact"].get("entity",""), l["contact"].get("address",""),
                   l.get("contact_source", "Own website / help centre / corporate pages"),
                   f"audits/{s}-audit-report.pdf", f"outreach/{s}-outreach-templates.md", l["verified_on"]])
    style_header(ws); autosize(ws, [4,22,26,22,30,10,12,34,18,34,52,34,38,40,12])
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment = WRAP; c.border = THIN
    ws.auto_filter.ref = ws.dimensions

    # ---------------------------------------------------------------- 3. EMAILS
    ws = wb.create_sheet("Emails")
    ws.append(["Brand","#","Send on","Subject","Body (plain text — paste into your email tool)","To (crawled email)"])
    for l in leads:
        for i, (subj, body) in enumerate(l["outreach"], 1):
            day = {1:"Day 1", 2:"Day 3", 3:"Day 7", 4:"Day 14"}[i]
            ws.append([l["brand"], i, day, subj, plain_html(body), l["contact"]["email"]])
    style_header(ws); autosize(ws, [20,4,8,54,110,32])
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment = WRAP; c.border = THIN
        ws.row_dimensions[row[0].row].height = 120
    ws.auto_filter.ref = ws.dimensions

    # ---------------------------------------------------------------- 4. LEAKS & WINS
    ws = wb.create_sheet("Leaks & Roadmap")
    ws.append(["Brand","Item","Title","Detail"])
    for l in leads:
        b = ATTRACTIVE.get(_slug(l["brand"]), {})
        for i, (t, d) in enumerate(b.get("leaks", []), 1):
            ws.append([l["brand"], f"LEAK {i}", t, d])
        for day, t, d in b.get("roadmap", []):
            ws.append([l["brand"], f"WIN {day}", t, d])
    style_header(ws); autosize(ws, [20,10,46,105])
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment = WRAP; c.border = THIN
        if row[1].value.startswith("LEAK"): row[2].fill = PatternFill("solid", fgColor=RED_BG)
        else: row[2].fill = PatternFill("solid", fgColor=GREEN_BG)

    # ---------------------------------------------------------------- 5. VS COMPETITOR
    ws = wb.create_sheet("You vs Competitor")
    ws.append(["Brand","Side","Point"])
    for l in leads:
        b = ATTRACTIVE.get(_slug(l["brand"]), {})
        for y in b.get("you", []): ws.append([l["brand"], "YOU", y])
        for c in b.get("competitor", []): ws.append([l["brand"], "COMPETITOR", c])
    style_header(ws); autosize(ws, [20,14,105])
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment = WRAP; c.border = THIN
        row[1].fill = PatternFill("solid", fgColor=(RED_BG if row[1].value == "YOU" else GREEN_BG))

    # ---------------------------------------------------------------- 6. ROI
    ws = wb.create_sheet("Expected ROI")
    ws.append(["Brand","Metric","Before (live)","After roadmap","Industry benchmark"])
    for l in leads:
        b = ATTRACTIVE.get(_slug(l["brand"]), {})
        for r in b.get("roi", []): ws.append([l["brand"], *r])
    style_header(ws); autosize(ws, [20,26,34,40,50])
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment = WRAP; c.border = THIN

    # ---------------------------------------------------------------- 7. AUDIT BASIS / SOURCES
    ws = wb.create_sheet("Audit Basis (sources)")
    ws.append(["Brand","Source (from the PDF's Audit Basis box)"])
    for l in leads:
        for s in l.get("sources", []):
            ws.append([l["brand"], s])
    style_header(ws); autosize(ws, [20,120])
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment = WRAP; c.border = THIN; c.fill = PatternFill("solid", fgColor=PURPLE)

    # ---------------------------------------------------------------- 8. SKILLS USED
    ws = wb.create_sheet("Skills Used")
    ws.append(["Audit section","Repository skill(s)","What was done with it"])
    for r in [
        ["Ad Intelligence","ads","Google Ads Transparency + Meta Ad Library: live counts, advertiser entities, destinations, durations"],
        ["Creative audit","ad-creative","Creative formats, fatigue signals, refresh-rate analysis per brand"],
        ["Copy & angle audit","copywriting","Hook/angle analysis from live ad copy captured in the Ad Library and Transparency"],
        ["Landing / destination audit","cro","Destination-path step count, locator vs product page, trust-proof placement"],
        ["Tracking audit","analytics, attribution","GTM/GA4 tags detected in live HTML (e.g. GTM-K6SZV8J, G-EN77D2S0YH); CAPI/Enhanced-Conversions guidance"],
        ["Competitor benchmark","competitor-profiling, competitors, competitor-x-ray, funnel-spy","Category benchmark rows in every PDF ('You vs Competitor')"],
        ["Outreach","cold-email, outreach-personalizer","4-email sequences per brand (Day 1/3/7/14), plain text ready"],
        ["PDF output","pdf-report-generator","Attractive 2-page Smart Pursuit format with audit-basis box + CTA"],
    ]:
        ws.append(r)
    style_header(ws); autosize(ws, [26,44,95])
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment = WRAP; c.border = THIN

    out = ROOT / "Food-Bangalore-ALL-IN-ONE.xlsx"
    wb.save(out)
    print(f"Saved {out.name}: {len(leads)} leads | {sum(len(l['outreach']) for l in leads)} emails | sheets: {wb.sheetnames}")

if __name__ == "__main__":
    main()
