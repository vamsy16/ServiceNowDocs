# Push the Food/Bengaluru pack (v2) into arena-performance-marketing

This session's GitHub token can write to **ServiceNowDocs only**, so the pack travels as a git
bundle. The bundle contains the complete commit **`a7434a9`** on branch **`arena/01a0fae3-arena-v2`**,
based on the current `main` (`409ff5f`, which already includes the first merged pack).

## 3 commands (run in a terminal with your GitHub login)

```bash
git clone https://github.com/vamsy16/arena-performance-marketing.git apm && cd apm
curl -sL -o /tmp/food.bundle "https://github.com/vamsy16/ServiceNowDocs/raw/arena/01a0fae3-servicenowdocs/handoff/food-bengaluru-arena.bundle"
git fetch /tmp/food.bundle "refs/heads/arena/01a0fae3-arena-v2:refs/remotes/bundle/v2" && git push origin refs/remotes/bundle/v2:refs/heads/arena/01a0fae3-arena-v2
```

Then open the PR:
https://github.com/vamsy16/arena-performance-marketing/compare/main...arena/01a0fae3-arena-v2

## What v2 changes

- **Audits rebuilt in the house ATTRACTIVE format** (the format of your attached clinic audit):
  metrics row → YOU vs COMPETITOR → 3 LEAKS (live-verified) → 3 QUICK WINS roadmap →
  EXPECTED ROI → AUDIT BASIS (sources) → our commitment → dark CTA.
- **`Food-Bangalore-ALL-IN-ONE.xlsx`** — one workbook, 8 sheets: README, Leads, Emails (all 44),
  Leaks & Roadmap, You vs Competitor, Expected ROI, Audit Basis (39 sources), Skills Used.
- `leads/*.json` now carry `contact_source` (exact crawl location of every email).
- Earlier text-format PDFs archived in `audits/_previous-text-format/`.

## After it's pushed
Delete the `handoff/` folder here — it is only a transport file.
