# Push the Food/Bengaluru pack into arena-performance-marketing

This session's GitHub token can write to **ServiceNowDocs only**, so the pack is staged here
as a git bundle (155 KB) containing the complete commit `f92d5d2` for the branch
`arena/01a0fae3-arena-performance-marketing`.

## 3 commands (run anywhere you have GitHub access)

```bash
git clone https://github.com/vamsy16/arena-performance-marketing.git apm && cd apm
curl -sL -o /tmp/food.bundle "https://github.com/vamsy16/ServiceNowDocs/raw/arena/01a0fae3-servicenowdocs/handoff/food-bengaluru-arena.bundle"
git fetch /tmp/food.bundle "refs/heads/arena/01a0fae3-arena-performance-marketing:refs/remotes/bundle/food" \
  && git push origin refs/remotes/bundle/food:refs/heads/arena/01a0fae3-arena-performance-marketing
```

Then open the PR: https://github.com/vamsy16/arena-performance-marketing/compare/main...arena/01a0fae3-arena-performance-marketing

## What the commit contains
- `niches/food-bengaluru/` — 11 lead JSONs, 11 branded audit PDFs, 11 outreach files (4 emails each),
  `ALL-EMAIL-SEQUENCES.md` (44 emails), `LEADS-INDEX.csv`, rebuild scripts
- `README.md` — new Food/Bengaluru niche section
- `data/seen_leads.json` — the 11 brands registered as day 3 (total 111, no overlap)

## After it's pushed
Delete this `handoff/` folder — it is only a transport file.
