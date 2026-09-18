#!/usr/bin/env python3
"""Render the client brief Markdown to a self-contained, styled HTML page.

Features: cover block, sticky table of contents, styled tables/call-outs, the
architecture diagram as HTML, print CSS (A4) and a scroll-spy TOC.

Run:  /home/user/pdfenv/bin/python tools/md_to_html.py
"""
import html
import os
import re

import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "ServiceNow-Impact-Australia-Client-Brief.md")
OUT = os.path.join(ROOT, "site", "brief.html")
os.makedirs(os.path.dirname(OUT), exist_ok=True)


def is_table_row(line):
    s = line.strip()
    return s.startswith("|") and s.endswith("|")


def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_sep_row(line):
    return is_table_row(line) and all(re.fullmatch(r":?-{2,}:?", c) for c in split_row(line))


def diagram_html():
    cols = [
        ("1. Your estate (consumer instance)", "navy", [
            "Impact Store Application — Impact Common / Content / Health",
            "Platform Health — Scan Engine, HealthScan, real-time prevention, AI fixes",
            "Value data collection — Performance Analytics packs per product",
            "Users &amp; roles — Platform Owner, Admin, Developer, Team Lead, Executive",
            "Instance Observer — off-instance observability",
        ]),
        ("2. Secure sync layer", "green", [
            "Service Bridge — automated registration (preferred) or manual (regulated / GCC)",
            "Inbound + outbound payloads; status must read <b>Active replication</b>",
        ]),
        ("3. Impact Delivery Instance", "blue", [
            "Impact Squad — CSM / CSE / Platform Architect / SAM",
            "Activity Center — conversations, tasks, files, calendar",
            "Value management — objectives, outcomes, value reports",
            "Catalogues — Accelerators, Initiatives, PARs, Capability Maps",
        ]),
        ("4. Business outcomes", "navy", [
            "Adoption · Platform health · Performance &amp; availability · Value realised · Upgrade readiness",
            "Cadence: quarterly reviews moving Foundations → Steady State",
        ]),
    ]
    cells = []
    for title, tone, bullets in cols:
        lis = "".join("<li>%s</li>" % b for b in bullets)
        cells.append('<div class="diag-col"><div class="diag-head %s">%s</div>'
                     '<ul class="diag-body">%s</ul></div>' % (tone, title, lis))
    return ('<div class="diagram"><div class="diag-row">%s</div>'
            '<div class="diag-loop">Foundations → Steady State cadence: monthly operational &amp; health reviews · '
            'quarterly outcome, support and executive reviews</div>'
            '<div class="diag-note">Callouts: Scan Engine findings are NOT transmitted to IDI · '
            'Feature availability depends on package, add-ons, roles and plugins</div></div>' % "".join(cells))


def build():
    raw = open(SRC, encoding="utf-8").read().splitlines()
    title = raw[0].lstrip("# ").strip()
    subtitle = next((l.strip() for l in raw[1:]
                     if l.strip() and not l.strip().startswith(("#", "|", ">"))), "")
    meta_start = next(k for k, l in enumerate(raw) if is_table_row(l))
    meta_end = meta_start
    while meta_end < len(raw) and is_table_row(raw[meta_end]):
        meta_end += 1
    meta_rows = [split_row(l) for l in raw[meta_start:meta_end] if not is_sep_row(l)]
    quote = next((l for l in raw[meta_end:] if l.strip().startswith(">")), "")
    body_start = next(k for k, l in enumerate(raw) if re.match(r"^##\s+1\.", l))
    body_md = "\n".join(raw[body_start:])

    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists",
                                       "attr_list", "md_in_html"])
    body = md.convert(body_md)

    # replace the rendered mermaid fence with the styled diagram
    body = re.sub(r'<pre><code class="language-mermaid">.*?</code></pre>',
                  diagram_html(), body, flags=re.S)
    # any other fence keeps a light code style
    body = body.replace("<pre><code>", '<pre class="code"><code>')

    # headings -> ids (for TOC links and anchor navigation)
    used = {}

    def slug(text):
        s = re.sub(r"<[^>]+>", "", text)
        s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:70] or "section"
        used[s] = used.get(s, 0) + 1
        return s if used[s] == 1 else "%s-%d" % (s, used[s])

    toc_items = []

    def add_id(m):
        level, attrs, text = m.group(1), m.group(2), m.group(3)
        sid = slug(text)
        if level in ("2", "3"):
            toc_items.append((int(level), sid, re.sub(r"<[^>]+>", "", text)))
        return '<h%s id="%s"%s>%s</h%s>' % (level, sid, attrs, text, level)

    body = re.sub(r"<h([1-6])([^>]*)>(.*?)</h\1>", add_id, body, flags=re.S)

    toc_html = "\n".join(
        '<a class="toc-l%d" href="#%s">%s</a>' % (lvl, sid, html.escape(txt))
        for lvl, sid, txt in toc_items)

    meta_html = "".join(
        "<tr><th>%s</th><td>%s</td></tr>" % (md_inline(c[0]), md_inline(c[1]))
        for c in meta_rows if len(c) >= 2)
    quote_html = md_inline(quote.strip()[1:].strip()) if quote else ""

    page = TEMPLATE.format(
        title=html.escape(re.sub(r"\*\*", "", title)),
        subtitle=html.escape(re.sub(r"[*]", "", subtitle)),
        meta=meta_html, quote=quote_html, toc=toc_html, body=body)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(page)
    return OUT


def md_inline(text):
    t = html.escape(str(text))
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    return t


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root {{
  --navy:#03213f; --blue:#1f4e79; --green:#03754d; --light:#e6f4ee;
  --grey:#f2f4f7; --mid:#5c6b7a; --rule:#d9e2ec;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:"Segoe UI",Roboto,-apple-system,"Helvetica Neue",Arial,sans-serif;
  color:var(--navy); background:#eef2f6; line-height:1.62; }}
a {{ color:var(--blue); }}
.layout {{ display:flex; max-width:1500px; margin:0 auto; align-items:flex-start; }}
nav.toc {{ position:sticky; top:0; width:330px; flex:0 0 330px; height:100vh; overflow-y:auto;
  background:#fff; border-right:1px solid var(--rule); padding:20px 16px 60px; }}
nav.toc h2 {{ font-size:.72rem; letter-spacing:.13em; text-transform:uppercase; color:var(--mid);
  margin:0 0 10px; }}
nav.toc a {{ display:block; text-decoration:none; color:var(--blue); padding:3px 6px;
  border-radius:4px; font-size:.82rem; }}
nav.toc a:hover {{ background:var(--grey); }}
nav.toc a.toc-l2 {{ font-weight:700; color:var(--navy); margin-top:9px; font-size:.86rem; }}
nav.toc a.toc-l3 {{ padding-left:16px; color:var(--mid); }}
nav.toc a.active {{ background:var(--light); color:var(--green); font-weight:600; }}
main {{ flex:1; min-width:0; background:#fff; padding:0 0 80px; }}
.wrap {{ max-width:940px; margin:0 auto; padding:0 34px; }}
header.cover {{ background:var(--navy); color:#fff; padding:46px 0 34px; }}
header.cover .wrap {{ max-width:940px; }}
header.cover h1 {{ font-size:2.1rem; margin:0 0 8px; line-height:1.2; }}
header.cover .sub {{ color:#7fd8b0; font-weight:600; font-size:1.02rem; margin-bottom:22px; }}
table.meta {{ width:100%; border-collapse:collapse; font-size:.82rem; background:#fff;
  border-radius:6px; overflow:hidden; }}
table.meta th {{ text-align:left; vertical-align:top; width:150px; background:var(--grey);
  color:var(--navy); padding:8px 10px; border:1px solid var(--rule); font-size:.78rem; }}
table.meta td {{ vertical-align:top; padding:8px 10px; border:1px solid var(--rule); color:#22364a; }}
.callout {{ background:var(--grey); border-left:4px solid var(--green); padding:12px 16px;
  border-radius:0 6px 6px 0; margin:22px 0; font-size:.92rem; }}
.idiagramwrap {{ }}
h2 {{ font-size:1.32rem; color:#fff; background:var(--navy); padding:9px 14px; border-radius:6px;
  margin:38px 0 14px; }}
h3 {{ font-size:1.09rem; color:var(--blue); margin:26px 0 8px; }}
h4 {{ font-size:.97rem; color:var(--green); margin:18px 0 6px; }}
p, li {{ font-size:.93rem; }}
ul, ol {{ padding-left:24px; }}
li {{ margin:3px 0; }}
table {{ width:100%; border-collapse:collapse; margin:16px 0 22px; font-size:.8rem; }}
th {{ background:var(--blue); color:#fff; text-align:left; padding:7px 9px; border:1px solid #b6c4d2;
  vertical-align:top; }}
td {{ padding:7px 9px; border:1px solid #b6c4d2; vertical-align:top; color:#22364a; }}
tbody tr:nth-child(even) td {{ background:var(--grey); }}
code {{ background:var(--grey); padding:1px 5px; border-radius:3px;
  font-family:"DejaVu Sans Mono",Consolas,monospace; font-size:.82em; }}
hr {{ border:0; border-top:1px solid var(--rule); margin:34px 0; }}
blockquote {{ margin:20px 0; background:var(--grey); border-left:4px solid var(--green);
  padding:12px 16px; border-radius:0 6px 6px 0; font-size:.92rem; }}
blockquote p {{ margin:6px 0; }}
blockquote p:first-child {{ margin-top:0; }}
blockquote p:last-child {{ margin-bottom:0; }}
.diagram {{ margin:22px 0 28px; }}
.diag-row {{ display:grid; grid-template-columns:1.5fr 1fr 1.45fr 1fr; gap:12px; }}
.diag-col {{ display:flex; flex-direction:column; }}
.diag-head {{ color:#fff; font-weight:700; font-size:.82rem; padding:8px 10px;
  border-radius:6px 6px 0 0; }}
.diag-head.navy {{ background:var(--navy); }}
.diag-head.green {{ background:var(--green); }}
.diag-head.blue {{ background:var(--blue); }}
.diag-body {{ margin:0; padding:10px 12px 12px 26px; background:var(--light);
  border:1px solid var(--rule); border-top:0; border-radius:0 0 6px 6px; font-size:.78rem;
  flex:1; }}
.diag-body li {{ margin:4px 0; }}
.diag-loop {{ background:#d9e2ec; color:var(--navy); text-align:center; padding:9px 12px;
  border-radius:5px; margin-top:12px; font-size:.83rem; }}
.diag-note {{ text-align:center; color:var(--mid); font-size:.78rem; margin-top:9px; }}
.actions {{ display:flex; gap:10px; flex-wrap:wrap; margin:6px 0 0; }}
.btn {{ display:inline-block; padding:9px 15px; border-radius:5px; text-decoration:none;
  font-size:.85rem; font-weight:600; background:var(--green); color:#fff; border:0; cursor:pointer; }}
.btn.alt {{ background:#fff; color:var(--navy); border:1px solid var(--rule); }}
@media (max-width:1080px) {{ nav.toc {{ display:none; }} .diag-row {{ grid-template-columns:1fr; }} }}
@media print {{
  body {{ background:#fff; }}
  nav.toc, .actions, .noprint {{ display:none; }}
  .layout {{ display:block; }}
  main {{ padding:0; }}
  header.cover {{ background:#fff; color:var(--navy); padding:0 0 14px; border-bottom:2px solid var(--green); }}
  header.cover .sub {{ color:var(--green); }}
  table.meta th {{ background:var(--grey); }}
  h2 {{ background:var(--navy) !important; -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
  th, .diag-head, .diag-body, .diag-loop, .callout, tbody tr:nth-child(even) td {{
    -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
  h2, h3 {{ break-after:avoid; }}
  table, .diagram, .callout {{ break-inside:avoid; }}
  @page {{ size:A4; margin:14mm; }}
}}
</style>
</head>
<body>
<div class="layout">
<nav class="toc">
  <h2>Sections</h2>
  {toc}
</nav>
<main>
  <header class="cover">
    <div class="wrap">
      <h1>{title}</h1>
      <div class="sub">{subtitle}</div>
      <table class="meta">{meta}</table>
      <div class="actions noprint" style="margin-top:16px">
        <a class="btn" href="ServiceNow-Impact-Australia-Client-Brief.pdf" download>Download PDF (A4)</a>
        <button class="btn alt" onclick="window.print()">Print this page</button>
        <a class="btn alt" href="index.html">← All deliverables</a>
      </div>
    </div>
  </header>
  <div class="wrap">
    <blockquote class="callout">{quote}</blockquote>
    {body}
  </div>
</main>
</div>
<script>
(function () {{
  var links = [].slice.call(document.querySelectorAll('nav.toc a'));
  var targets = links.map(function (a) {{ return document.getElementById(a.getAttribute('href').slice(1)); }});
  function onScroll() {{
    var y = window.scrollY + 130, best = 0;
    targets.forEach(function (t, i) {{ if (t && t.offsetTop <= y) best = i; }});
    links.forEach(function (a, i) {{ a.classList.toggle('active', i === best); }});
  }}
  window.addEventListener('scroll', onScroll, {{ passive: true }});
  onScroll();
}})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    print("wrote:", build())
