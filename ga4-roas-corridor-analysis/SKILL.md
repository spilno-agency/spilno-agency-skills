---
name: ga4-roas-corridor-analysis
description: |
  Conducts a complete Google Ads efficiency analysis through Google Analytics 4 and builds a branded report as a Google Doc.
  Uses the "ROAS corridor" method — takes actual ROAS variance over 6 months and forecasts revenue growth at higher budget levels.
  Trigger this skill whenever the user asks (in any language): "ROAS analysis for [site]", "analyze Google Ads for [site]", "ROAS corridor for [site]", "Google Ads budget forecast", "what happens if I increase budget by X", "revenue per 1 unit of ad spend", "ROAS [site]", "Google Ads efficiency [site]", "analyze GA4 ads", "ad effectiveness analysis [site]", or any request to evaluate ROAS / budget forecast / Google Ads efficiency from GA4 data.
  Trigger AGGRESSIVELY whenever Google Ads, ROAS, GA4, ad budget, or revenue forecast are mentioned together with a specific site — even if the user doesn't explicitly say "skill", "report", or "corridor".
---

# GA4 ROAS Corridor Analysis

Automates Google Ads efficiency analysis via the Google Analytics 4 UI and produces a branded Google Doc report.

## When to use

The user wants to understand:
- how much revenue 1 unit of ad spend brings
- how ROAS has fluctuated over recent months
- what happens to revenue if budget is increased by 10k / 25k / 50k
- whether it's worth scaling ads

## Inputs from the user

**Required:**
- Site domain (e.g. `example.com`)
- GA4 access in Chrome under the user's Google account

**Optional (with defaults):**
- Analysis period — defaults to **last 6 complete months**
- Currency — defaults to local currency of the property
- Agency / brand name for the report (see [Configuration](#configuration))

## Required input prompt

**Before starting the analysis**, ALWAYS ask the user via `AskUserQuestion` (4 questions):

1. **Project domain to analyze:** (e.g. `example.com`)
2. **Model growth at +10 000 budget?** (yes / no, default yes)
3. **Model growth at +25 000 budget?** (yes / no, default yes)
4. **Model growth at +50 000 budget?** (yes / no, default yes)

If the domain was already passed as a command argument — skip question #1, but still ask 2–4 to confirm scenarios. The user can disable any scenario (then exclude it from final tables) or add a custom one (via "Other").

Don't guess these — ask first, then work.

## Configuration

The skill produces a report branded with your agency name. To customize:

1. Create a file `~/.claude/skills/ga4-roas-corridor-analysis/config.json` with:
   ```json
   {
     "agency_name": "Your Agency Name",
     "default_responsible": "Your Name",
     "doc_title_template": "Revenue growth forecast for budget increase in Google Ads / {domain} / {agency_name}",
     "currency_symbol": "грн",
     "language": "uk"
   }
   ```
2. If no config — defaults: `agency_name = "{AGENCY_NAME}"` (placeholder user can find/replace), `language = "uk"`, `currency_symbol = "грн"`.
3. CSS styling in the HTML template is a sensible default (Montserrat, clean tables). Override it in the config under `css` key if needed.

## Prerequisites

1. **Claude for Chrome** extension installed and the user is logged into Google with an account that has GA4 access.
2. The GA4 property has **e-commerce tracking** with a **purchase** event configured.
3. The GA4 property is linked to Google Ads (otherwise Cost will be zero — warn the user and offer to pull Cost from Google Ads UI directly).

## Algorithm

### Step 1. Find the GA4 property

Open https://analytics.google.com via `navigate`. Click the property selector in the top-left, type the domain (without TLD, e.g. `example` for `example.com`) in the search box. If nothing is found — ask the user to switch Google accounts. Find the property and click it. Remember the `property_id` from the URL (format `/a<account_id>p<property_id>/`).

### Step 2. Navigate to "Conversion Performance" report

Direct URL is unstable — use sidebar navigation:
1. Click the "Advertising" icon (left panel, ~3rd icon from top)
2. In the submenu click "Conversion performance" (under "Conversions")

"Conversion performance" is the only GA4 UI report where Cost and Revenue are available per month per channel.

### Step 3. Filter by purchase

Top of report — click the conversion-events dropdown (default shows "X of Y conversions"). **Uncheck** everything except **"[domain] purchase"**. Click "Apply".

Verify the filter — the dropdown should now show the specific purchase event name.

### Step 4. Collect monthly data for 6 months

For each of the last 6 complete months:

1. Click the date picker in the top-right
2. In "Start date" / "End date" fields type the first and last day of the month in `YYYY-MM-DD`
3. Click "Apply"
4. Wait 6 seconds for load
5. Extract table data via JavaScript:

```javascript
var rows = document.querySelectorAll('tr');
var data = [];
rows.forEach(r => {
  var cells = r.querySelectorAll('td');
  if (cells.length > 4) {
    var line = [];
    cells.forEach(c => line.push(c.innerText.replace(/\s+/g,' ').trim()));
    data.push(line.join(' || '));
  }
});
data.join('\n')
```

Column order: `Channel | All conversions | Ad cost | CPA | Impressions | Clicks | CPC | Total revenue | ROAS`.

From each month take ONLY Google Ads channels:
- **Cross-network** (this is Performance Max)
- **Paid Shopping**
- **Paid Search**

Sum their Cost and Revenue — these are your monthly Google Ads Cost / Revenue.

**Important: use `browser_batch`** for each cycle (open date picker → enter both dates → click Apply → wait) — significantly faster than individual calls.

### Step 5. Calculations

For each month: `ROAS = Revenue / Cost`.

Across the 6 points calculate:
- **MIN ROAS** — lowest value (pessimistic scenario)
- **MAX ROAS** — highest (optimistic)
- **AVG ROAS** — arithmetic mean (baseline)
- **Standard deviation** σ
- **Coefficient of variation** CV = σ / AVG

CV < 15% → corridor stable, forecast reliable.
CV > 25% → warn user about instability.

### Step 6. Revenue growth forecast

Current monthly budget = avg Cost across 6 months.
Current monthly revenue = avg Revenue across 6 months.

For each scenario (only those the user confirmed in the input prompt):

| Scenario | Pessimistic (Δ × MIN) | Baseline (Δ × AVG) | Optimistic (Δ × MAX) |

Separately — absolute new-revenue table: `(current budget + Δ) × ROAS`.

### Step 7. Create the Google Doc report

Call the Google Drive `create_file` tool (mcp tool name depends on connected Drive MCP) with parameters:
- `title`: `{doc_title_template}` from config, filled with `{domain}` and `{agency_name}`
- `contentMimeType`: `text/html`
- `textContent`: HTML per template below

HTML is created as a file on Drive. Then:
1. Open `https://drive.google.com/file/d/[FILE_ID]/view` in Chrome
2. Click "Open with" → "Google Docs"
3. Wait for conversion — a new Google Doc with formatting is created

Alternatively — after `create_file` use the URL `https://docs.google.com/document/d/[FILE_ID]/edit` and tell the user.

### Step 8. Present the result

Give the user:
- Clickable link to the Google Doc
- Short chat summary: average ROAS, corridor, recommended scenario
- 1–2 caveats (if any — low CV, incomplete year, small Paid Search sample, etc.)

## HTML template for Google Doc

Default CSS in `<head>` (clean Montserrat-based style; override via config):

```css
body, p, h1, h2, h3, table, td, th, li { font-family: 'Montserrat', sans-serif; line-height: 1.5; text-align: left; }
h1 { font-size: 15pt; font-weight: bold; margin: 0 0 12pt 0; }
h2 { font-size: 13pt; font-weight: bold; margin: 18pt 0 8pt 0; }
h3 { font-size: 13pt; font-weight: bold; margin: 14pt 0 6pt 0; }
p, li, td, th { font-size: 11pt; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0; }
td, th { border: 1pt solid #000; padding: 4pt 6pt; font-size: 10pt; }
th { background: #f0f0f0; font-weight: bold; }
.num { text-align: right; }
ol { padding-left: 24pt; }
ol li { margin-bottom: 4pt; }
```

Document structure (numbered sections, no trailing period in headings):

**IMPORTANT — Pageless mode & collapsible sections:** After the Google Doc is created, ALWAYS switch it to Pageless mode (File → Page setup → "Pageless" tab → Apply). In this mode all H2 headings auto-collapse — the user can hide service sections and see the essentials immediately.

Section order:

1. **Header** (h1):
   - Document title (H1) — **"Revenue growth forecast for budget increase in Google Ads for [domain]"**
   - Fields: Responsible, Updated (format `DD/MM/YY`), Project, Analysis period
2. **"Technical analysis details"** (NO number — preamble, usually collapsed) — GA4 report name, menu path, property ID, account. H2 heading without numeric prefix so it doesn't shift numbering. Source-of-data quick-reference.
3. **"1. Task description"** — formulation: "Forecast how much project [domain] revenue grows when monthly Google Ads budget is increased by [scenarios]. Method — ROAS corridor based on actual GA4 data for [period]".
4. **"2. What was done"** — numbered list of steps
5. **"3. Monthly Google Ads dynamics"** — 6-month table (Month / Cost / Revenue / Purchases / ROAS) + bottom row "Total 6 months"
6. **"4. ROAS corridor"** — table with MIN / AVG / MAX / σ / CV
7. **"5. Revenue growth forecast"** — table Δ Budget × confirmed scenarios
8. **"6. Total monthly revenue forecast"** — table: Scenario / Budget / Min revenue / Avg / Max
9. **"7. Key observations"** — numbered list 4–6 items
10. **"8. Method limitations"** (usually collapsed) — mandatory numbered list of three limitations (use verbatim wording):
    1. "**Linear extrapolation.** The forecast assumes ROAS stays in the historical corridor at any budget. In reality marginal ROAS is usually lower than average — each additional dollar buys less-targeted traffic (diminishing returns). So actual growth at +25k / +50k may be 20–40% below optimistic."
    2. "**Competition ignored.** The method doesn't model competitor actions in the Google Ads auction. If competitors raise bids, part of the extra budget goes to costlier impressions without conversion lift. For accuracy you need Search Lost Impression Share (Rank) and Auction Insights from Google Ads UI."
    3. "**Market saturation ignored.** GA4 doesn't show how many impressions are still available. If a campaign already wins >80% of impressions (Impression Share), additional budget yields little. Check this separately in Google Ads → Search Lost IS (Budget)."
11. **"9. Conclusion"** — which scenario to start with, with caveats. ALWAYS reference limitations from section 8 (e.g. "considering limitations from §8 we recommend starting with…").
12. **"10. TL;DR"** — the headline summary, SHORT (3–5 lines max). Format — numbered list with confirmed scenarios:
    1. "Budget increase of **+10 000** → revenue grows by **+X** (min to max)."
    2. "Budget increase of **+25 000** → revenue grows by **+Y** (min to max)."
    3. "Budget increase of **+50 000** → revenue grows by **+Z** (min to max)."
    No extra explanations. This is the TL;DR the client reads when everything else is collapsed.

Formatting rules:
- Large numbers space-separated by thousands: `1 340 400`, not `1340400`
- Numbers in tables right-aligned (`class="num"`)
- Bold the min / avg / max ROAS and key forecast figures
- Keep technical terms as-is in any language (PMax, Cross-network, Paid Shopping, ROAS, CPA, CPC)

## Technical notes (important)

**GA4 date picker:**
- Click the date range top-right (opens panel)
- "Start date" field — triple_click → type new date → Tab
- "End date" field — triple_click → type → Tab
- Click "Apply"

**Google Docs canvas:**
Google Docs renders content on canvas, so standard selectors may not work for text manipulation. To select doc sections use coordinate click + Shift+click. For scrolling — `scroll` action at a doc coordinate.

**JavaScript-extracted table may be truncated:**
If `data.join('\n')` shows `[TRUNCATED]` — some channels were cut. Usually not critical, since we only care about Cross-network, Paid Shopping, Paid Search — always in top-5.

**If Cost = 0 for all Google Ads channels:**
Google Ads is not linked in GA4. Warn the user and offer:
1. Go to Admin → Product Links → Google Ads links and configure the link
2. Alternatively — pull Cost directly from Google Ads UI ("Campaigns → segment By month" report)

**If GA4 account/property not found by domain:**
- Check which Google account is logged in (avatar top-right)
- Suggest switching accounts

**"Responsible" field in the doc:**
Defaults to the logged-in user's name (from GA avatar or email). If unsure — insert `{AGENCY_NAME}` placeholder and tell the user to replace.

**"Updated" field:**
Today's date in `DD/MM/YY` format from system context.

## What NOT to do

- Don't use the standard "Acquisition → Traffic acquisition" report for Cost — no spend column there
- Don't take attributed revenue from Advertising hub if total revenue from Traffic acquisition is available — total is more correct for forecasting
- Don't extrapolate Paid Search ROAS to large budgets — small sample (<20 purchases/month)
- Don't show a forecast without a warning if CV > 20% — ROAS is unstable and the forecast is risky
- Don't delete the intermediate HTML file after Google Doc conversion (permanent deletion is a prohibited action — let the user delete it)

## Trigger examples

| User request | Triggers? |
|---|---|
| "ROAS analysis for example.com" | ✅ |
| "analyze Google Ads for site.com over a year" | ✅ |
| "what's the ROI on advertising for example.com" | ✅ |
| "what happens to revenue if I add 30k to Google Ads budget" | ✅ |
| "ROAS corridor site.com" | ✅ |
| "make a Google Ads report" (no specific site) | ❌ — ask for domain first |
| "configure a Google Ads campaign" | ❌ — different task |
| "create an ad creative" | ❌ — creative, not analysis |

## Pre-flight checklist (run mentally before finalizing)

- [ ] 6 data points collected (monthly)
- [ ] Cost ≠ 0 in all months (else Google Ads is not linked)
- [ ] Purchase filter is active (not the default "X of Y")
- [ ] MIN / AVG / MAX / σ / CV calculated
- [ ] Google Doc created with branded style (Montserrat or your CSS override, numbered sections)
- [ ] Document title in the format `{doc_title_template}` from config
- [ ] Required fields present (Responsible, Updated, Source data)
- [ ] "Technical analysis details" section (no number) at the start, right after the header
- [ ] Document switched to Pageless mode
- [ ] Section "10. TL;DR" added at the end with confirmed scenarios
- [ ] User given a clickable Doc URL
