# Push the Food/Bengaluru pack into `vamsy16/arena-performance-marketing`

The agent's token cannot push to this repo (403, confirmed several times), so the branch
travels as a **git bundle** and you push it with your own credentials.

**Bundle (v3 — current):** `food-bengaluru-arena-v3.bundle` (417 KB)
**Branch inside:** `arena/01a0fae3-arena-v3`, based directly on `main` @ **143d3fb**
(the commit where you uploaded the Partha reference PDF), so it merges cleanly.

## What v3 contains (vs the v2 bundle)

All 11 audits have been rebuilt in the format of
`partha-dental-skin-hair-clinic-audit.pdf` — the 7-page, evidence-only
**Paid Media & Measurement Audit**:

1. Navy cover with metric cards (live ad counts, tag families, findings count), prepared-for and contact boxes
2. Contents + `01` method (including: *where a value could not be measured it is reported as unavailable; nothing is inferred to fill a gap*)
3. `02` the ad account — live label/value table — plus a **coverage table** (measured / not measured / unavailable, with the method for each)
4. `03` findings — severity pill, numbered title, monospace `key: value` evidence block quoting the raw measurement, italic analysis
5. Evidence register — every number in the report and where it came from
6. `04` opportunity score — 5 dimensions × 4 dots, overall /20, grade, and the amber qualification box
7. `05` next steps ordered by effort against impact, with the "happy to walk through this on a short call" CTA

Plus: **`VERIFY-THE-DATA.md`** — a 49-row guide mapping every claim in every audit to the
exact public URL where you or the lead can check it (Google Ads Transparency per domain,
Meta Ad Library links including individual creative IDs, the site URL to view-source for
each tag ID, header-check links), plus a list of what no one outside the company can verify
(spend, ROAS, CPA).

`Food-Bangalore-ALL-IN-ONE.xlsx` now has **14 sheets** — the original 8 plus
`Findings (severity+evidence)`, `Opportunity Score`, `Coverage (measured vs not)`,
`Evidence Register`, `Verify These (links)`, `Cannot be verified`. Outreach emails and the
README were updated to reference the 7-page audit. Each audit is per-lead (Licious, Akshayakalpa Organic, Anand Sweets,
Chai Point, The Baker's Dozen, Cothas Coffee, Early Foods, iD Fresh Food, Third Wave
Coffee, Frozen Bottle, Milky Mist).

Everything sits under `niches/food-bengaluru/` (unchanged path from v1/v2).

## How to push (one option is enough)

### Option A — fetch the bundle, then push

```bash
git clone https://github.com/vamsy16/arena-performance-marketing.git
cd arena-performance-marketing
git fetch /path/to/food-bengaluru-arena-v3.bundle arena/01a0fae3-arena-v3:arena/01a0fae3-arena-v3
git push -u origin arena/01a0fae3-arena-v3
```

### Option B — apply as a patch

```bash
git clone https://github.com/vamsy16/arena-performance-marketing.git
cd arena-performance-marketing
git checkout -b arena/01a0fae3-arena-v3
git bundle unbundle /path/to/food-bengaluru-arena-v3.bundle   # lists the commits
git pull /path/to/food-bengaluru-arena-v3.bundle arena/01a0fae3-arena-v3
git push -u origin arena/01a0fae3-arena-v3
```

Then open a PR from `arena/01a0fae3-arena-v3` into `main`:
https://github.com/vamsy16/arena-performance-marketing/compare/main...arena/01a0fae3-arena-v3

## After it is pushed

Tell me and I will delete the bundle and this file from `ServiceNowDocs` — they exist
only as transport.
