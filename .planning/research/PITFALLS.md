# Domain Pitfalls: Restaurant Operations Automation

**Domain:** Multi-location restaurant ops — consolidated reporting, payroll prep, checklist app
**Project:** Rez Operations Suite (Moto Medi / Tikka Shack — 5 locations)
**Researched:** 2026-03-14

---

## Critical Pitfalls

Mistakes that cause rewrites, broken numbers, or client trust collapse.

---

### Pitfall 1: Food Cost % Calculated from Invoice Totals Alone

**What goes wrong:** The reporting Sheet calculates food cost % as BEK Entree invoice total / gross sales. This produces a permanently wrong number because it uses purchases, not actual COGS.

**Why it happens:** Invoice CSV data is available; inventory counts are not. Invoice total is the natural proxy, but it ignores beginning inventory and ending inventory. A week with heavy ordering and low sales looks artificially high; a week with low ordering and high sales looks artificially low.

**Correct formula:**
```
COGS = Beginning Inventory + Purchases (BEK invoices) - Ending Inventory
Food Cost % = COGS / Food Sales
```

**Consequences:** Rez makes margin decisions on a systematically skewed metric. If food cost is trending wrong direction, the root cause will never be visible.

**Prevention:** During Phase 1 (reporting Sheet), explicitly document in the Sheet itself — as a cell note or header annotation — that the food cost % row reflects purchases, not true COGS, and name the column "Food Purchases %" rather than "Food Cost %". If Rez does weekly inventory counts, add a COGS tab later. Never silently present a proxy metric as the real one.

**Detection (warning sign):** Food cost % swings more than 5-8% week-over-week with no obvious cause. Most operators run 28-35% food cost. Numbers outside that band without explanation usually indicate a calculation problem.

**Phase:** Phase 1 — Reporting Sheet. Address in design, not post-launch.

---

### Pitfall 2: Delivery Platform CSVs Use Different Revenue Definitions

**What goes wrong:** "Sales" in DoorDash CSV is not the same line item as "Sales" in UberEats CSV. Adding them together double-counts some amounts and misses others.

**Why it happens:** Each platform defines its columns independently:
- **DoorDash:** "Subtotal" = pre-tax, pre-fee order amount. "Net Total" = subtotal minus commissions minus error charges minus promotions.
- **UberEats:** "Sales" = cost before tax or Uber service fee. "Total" = Sales + Tax. "Uber Fee" is a separate column.
- **Grubhub:** Commission structure varies by contract tier; some operators are on "Basic" (lower commission, no marketing fee), others on "Plus" or "Premium" (higher commission, marketing support).

DoorDash also has an "Amendments" section covering error charges and adjustments that are deducted from payout — these are not in the Subtotal column but appear as separate line items in the CSV.

**Consequences:** A consolidated "Delivery Revenue" row that sums Subtotals across all three platforms overstates actual revenue received. Commissions may be hidden or double-counted depending on which column is used.

**Prevention:**
1. Before building any formula, manually export one week's CSV from each platform and map the columns side by side. Do this during sample data collection with Rez before writing a single VLOOKUP.
2. Always use the net payout figure — what actually deposits — not the order subtotal.
3. Create a separate mapping row in the Sheet that documents which CSV column name maps to which field.
4. Name consolidated fields explicitly: "DD Net Revenue," "UE Net Revenue," "GH Net Revenue" — never a single "Delivery Revenue" that hides the source.

**Detection:** Actual bank deposits from delivery platforms don't match Sheet's delivery revenue calculation.

**Phase:** Phase 1 — Reporting Sheet. Must be resolved before building any consolidation formula.

---

### Pitfall 3: Square CSV Export Format Varies by Report Type

**What goes wrong:** Square offers multiple CSV exports — Sales Summary, Transaction-level, Items, Labor — and they have fundamentally different structures. Paste-in instructions that work for one break silently for another.

**Why it happens:** Sales Summary CSV has 1-3 summary rows with columns like "Total Gross Sales," "Total Discounts," "Total Net Sales," "Total Fees." Transaction CSV has one row per payment with timestamps and individual amounts. Instructions that say "paste your Square export" without specifying which export produce wrong results.

**Specific format issue:** Sales Summary is a human-readable dashboard export with mixed row types — there is no consistent primary key column. Transaction CSV is long-form and requires aggregation before use.

**Also:** Square's CSV column headers change when you toggle which columns are visible in the dashboard view before export. An operator who exports with "Tax" column unchecked will produce a CSV missing that column. The Sheet will silently reference the wrong column index.

**Prevention:**
1. Document the exact export path step-by-step in the Sheet (e.g., "Reports > Sales Summary > Export > CSV"). Include a screenshot or inline instructions.
2. Use column header names (e.g., `MATCH("Total Net Sales", header_row, 0)`) rather than fixed column indices to find values. This survives column reordering.
3. Specify exactly which Square report type the Sheet expects. Use the Sales Summary for weekly reporting; use the Labor/Timecard report for hours.
4. On first use with Rez, have them export while you watch via screen share.

**Detection:** Formula returns 0 or a text error immediately after a fresh paste. Headers don't match expected column names.

**Phase:** Phase 1 — Reporting Sheet. Also applies to Phase 2 — Payroll Sheet (timecard CSV).

---

### Pitfall 4: Overtime Calculation Breaks for Multi-Location Employees

**What goes wrong:** An employee works 22 hours at Moto Medi Lubbock and 22 hours at Tikka Shack in the same week — 44 hours total, 4 hours overtime. But if you pull Square's timecard export per location, each location shows 22 hours (no overtime). The overtime is invisible.

**Why it happens:** Square's timecard export can be filtered by location. If hours are summed per-location rather than per-employee across all locations before applying the 40-hour threshold, overtime is never triggered.

**Also:** Texas does not have daily overtime (no 8-hour-per-day rule) — only federal 40-hour weekly. However, if Rez ever expands to New Mexico or Colorado, those states have daily overtime rules. The Sheet as built for Texas will produce wrong numbers in other jurisdictions without a flag.

**Blended rate edge case:** For employees with multiple pay rates (e.g., cross-trained as cook and cashier at different rates), Square calculates overtime using a weighted blended rate. If the payroll Sheet tries to replicate this manually using a simpler formula, the overtime premium will be miscalculated.

**Prevention:**
1. The payroll Sheet must aggregate hours by employee name (or ID) across all location tabs before applying the overtime threshold — not sum hours after applying the threshold per location.
2. Export Square's "Labor cost by location" CSV which exports all locations in a single file. Do not export per location and then merge; this is where errors enter.
3. For employees with multiple wages, flag them clearly in the payroll Sheet and note that their overtime premium requires the blended rate calculation. Surface this as "manual review required" rather than automating incorrectly.
4. Add a visible cell label: "Overtime rule: TX — Federal 40hr weekly only."

**Detection:** An employee shows 0 overtime in the Sheet but Gusto flags them during payroll run.

**Phase:** Phase 2 — Payroll Sheet. This is the highest-risk calculation in the entire project.

---

### Pitfall 5: Google Sheets as Checklist Backend — Concurrent Write Collisions

**What goes wrong:** Two staff at the same location tap checklist items nearly simultaneously (e.g., both tap "Sanitize prep station" at 8:01am). Both writes succeed but one silently overwrites the other. Timestamp or completion record is lost.

**Why it happens:** Google Sheets API has no row-level locking. Concurrent writes via Apps Script or fetch calls to the Sheets API can race. This is documented behavior — concurrent form submissions to the same Sheet can lose entries.

**At Rez's scale:** 5 locations, ~2-5 staff per location opening shift, 15-20 checklist items each. Simultaneous submissions are unlikely but possible, especially at shift handoff moments.

**Also:** Sheets API quota: 300 read requests per minute per project. If the manager dashboard auto-refreshes and 5 tablets are also writing concurrently, the quota can be hit during busy periods, causing the checklist app to throw a "rate limit exceeded" error.

**Prevention:**
1. Use Google Apps Script LockService for all write operations from the checklist app (script-level lock). This serializes writes and prevents race conditions.
2. Alternatively — and preferably for the Next.js architecture — write checklist data to a lightweight database (Vercel KV, PlanetScale free tier, or Supabase free tier) and sync to Sheets on a schedule, keeping Sheets as a read-only reporting view rather than live write target.
3. Design the checklist data model so each checklist item is its own row with a composite key (location + date + shift + item_id). Append-only writes are far safer than update-in-place.
4. Implement exponential backoff for API errors in the Next.js app — don't let a single rate limit error show a broken screen to a staff member.

**Detection:** Manager dashboard shows fewer completions than expected. Staff report they tapped items that didn't save.

**Phase:** Phase 3 — Checklist App. Architecture decision must be made before building the write layer.

---

### Pitfall 6: "Paste Your CSV Here" Instructions Fail Silently Due to Date/Number Format Parsing

**What goes wrong:** When an operator pastes a CSV into Google Sheets manually (rather than via File > Import), Sheets parses values based on the active locale. Dollar amounts like "$1,234.56" import as text, not numbers. Dates like "03/14/2026" may import as text or as a date depending on Sheets locale settings. Formulas built on these cells return 0 or #VALUE.

**Why it happens:** Paste-as-text treats the whole clipboard as strings. Even File > Import can misdetect number vs. currency columns. The problem is invisible until a SUM formula returns 0 on a column that looks numeric.

**Also specific to this project:** DoorDash timestamps are in UTC by default ("Timestamp (UTC)" column). If the reporting Sheet uses date comparisons without converting timezone, a transaction that occurred at 11pm CT appears on the next day's report.

**Prevention:**
1. In the reporting Sheet, include a dedicated "Paste Zone" tab where raw CSV data lands, with a corresponding "Cleaned Data" tab that applies `VALUE()`, `DATEVALUE()`, and `TRIM()` transforms. Never run calculations directly on pasted data.
2. Document the correct import method: File > Import > Upload > Separator type: Comma > Convert text to numbers/dates/formulas: checked.
3. For DoorDash specifically: add a UTC-to-CT offset column (`=A2 - TIME(6,0,0)` or `TIME(5,0,0)` for CDT) as part of the Cleaned Data transform.
4. Add a data validation check row that counts cells in key columns using `ISNUMBER()` and alerts if count is 0.

**Detection:** SUM on a revenue column returns 0 despite visible numbers in cells. ISNUMBER() returns FALSE on what looks like a number.

**Phase:** Phase 1 — Reporting Sheet. Design the paste zone before any formula structure.

---

## Moderate Pitfalls

---

### Pitfall 7: Consolidated Summary Tab Drifts Out of Sync When Location Tabs Are Renamed

**What goes wrong:** The summary tab references location tabs by name (e.g., `='Moto Medi Lubbock'!B12`). If a tab is renamed ("Moto Medi - Lubbock" with a dash), all references break silently — they return a #REF error or 0 depending on how the formula is built.

**Prevention:** Use INDIRECT() with a named cell that holds the location tab name, or standardize tab names using a naming convention enforced by a setup checklist given to Rez. Document tab names as a contract: "Do not rename these tabs." Better: use a location ID column in data (location code like "MML," "MMA," "MMA2," "TS1," "TS2") and QUERY/FILTER against that ID rather than referencing separate location tabs.

**Phase:** Phase 1 — Reporting Sheet structure design.

---

### Pitfall 8: Week-over-Week Comparison Breaks at Month/Quarter Boundaries

**What goes wrong:** The variance flag logic compares "this week" to "last week" by subtracting 7 from the current week's row index. When you archive past weeks to a new tab or clear old data, the formula references a blank row and flags every metric as >5% change (or errors).

**Prevention:** Store weekly data in append-only rows with an explicit date column. Build the WoW comparison using VLOOKUP or MATCH against the date column, not row offsets. Never build formulas that assume "previous week is always 1 row up."

**Phase:** Phase 1 — Reporting Sheet.

---

### Pitfall 9: Checklist Completion Timestamps Are Meaningless Without Location Context

**What goes wrong:** The manager dashboard shows "Opening checklist 100% complete" but doesn't show which staff member completed it or which location. When an item is disputed ("Was the fryer cleaned?"), there is no audit trail.

**Prevention:** Every checklist write must include at minimum: location_id, shift (opening/closing/cleaning), item_id, staff_name (or device_id if anonymous), timestamp. Do not allow anonymous completions. If staff don't want to log in, use a single tap on a "Who is completing this?" selector at the start of each shift session — store it in local state for that session.

**Phase:** Phase 3 — Checklist App. Data model decision, not a UI decision.

---

### Pitfall 10: Grubhub Payout Reporting Lags by 7-10 Days

**What goes wrong:** Grubhub merchant statements are typically available 7-10 days after the close of a payout period. If the weekly reporting workflow requires all platform data by Monday morning, Grubhub data for the previous week may not yet be available, causing the weekly report to always show Grubhub as blank or from the week prior.

**Prevention:** Design the reporting Sheet to explicitly flag data freshness. Add a "Last updated" date cell per platform. Add a conditional format: if the Grubhub date is more than 10 days old, highlight the Grubhub column yellow with label "Pending." Do not sum Grubhub into the consolidated total in a way that silently excludes it when empty — either always include (with 0 as placeholder) or always flag the omission.

**Phase:** Phase 1 — Reporting Sheet. Confirm Grubhub's actual payout lag with Rez during sample data review.

---

## Minor Pitfalls

---

### Pitfall 11: Gusto Payroll Import Requires Specific Column Names and Order

**What goes wrong:** Gusto accepts CSV payroll uploads but requires exact column headers. A payroll prep Sheet that exports columns in a different order or with different header names will fail the Gusto import, forcing manual entry.

**Prevention:** Download Gusto's sample import template and reverse-engineer the exact required column names and order before designing the payroll Sheet output tab. The output tab should be formatted to exactly match Gusto's import template, not a Rez-friendly view.

**Phase:** Phase 2 — Payroll Sheet. Verify Gusto import format before building the output layer.

---

### Pitfall 12: Tablet Browser State Creates Ghost Checklist Sessions

**What goes wrong:** A shared tablet at a location has a checklist session half-completed from the morning shift. The afternoon closer picks up the tablet and sees the morning's partially-completed list. They either complete items that don't apply to their shift, or assume items are already done when they haven't been verified.

**Prevention:** Checklist app must show shift selector prominently on load. Each shift creates a new session keyed on (location + date + shift). Previous shift completions should be visible but read-only, clearly labeled "Morning shift — completed by [name]." Do not allow cross-shift item completion. Auto-expire the active session at shift end time (configurable per location).

**Phase:** Phase 3 — Checklist App UX design.

---

### Pitfall 13: BEK Entree Invoice CSV May Include Non-Food Line Items

**What goes wrong:** BEK Entree is a broadline distributor — they supply food, paper goods, cleaning supplies, and equipment. If the food cost % calculation sums the entire invoice total from BEK CSV, non-food items inflate the numerator.

**Prevention:** During sample data collection with Rez, inspect at least 4 weeks of BEK invoices. If the CSV has a category or department column, filter to food-only lines before summing. If there is no category column, ask Rez whether BEK orders are food-only or mixed. Flag this assumption explicitly in the Sheet.

**Phase:** Phase 1 — Reporting Sheet. Validate during data collection before formula build.

---

## Phase-Specific Warning Map

| Phase | Topic | Likely Pitfall | Mitigation |
|-------|-------|----------------|------------|
| Phase 1 | Reporting Sheet — revenue | Delivery platform column mismatches | Map all CSVs manually before formula build |
| Phase 1 | Reporting Sheet — food cost | Invoice total ≠ COGS | Label as "Food Purchases %" explicitly |
| Phase 1 | Reporting Sheet — data paste | Currency/date parsing as text | Design paste zone + ISNUMBER validation |
| Phase 1 | Reporting Sheet — WoW comparison | Row-offset formula breaks at boundaries | Date-keyed VLOOKUP, not row offsets |
| Phase 1 | Reporting Sheet — Grubhub | Payout lag causes blank columns | Per-platform freshness date + flag |
| Phase 1 | Reporting Sheet — BEK | Non-food items in invoice total | Inspect and filter by category |
| Phase 2 | Payroll Sheet — overtime | Cross-location hours not aggregated | Employee-level aggregate before threshold |
| Phase 2 | Payroll Sheet — output | Gusto import format mismatch | Match Gusto template exactly |
| Phase 2 | Payroll Sheet — Square export | Wrong report type selected | Document exact export path with steps |
| Phase 3 | Checklist App — data | Concurrent write collisions | LockService or append-only separate DB |
| Phase 3 | Checklist App — sessions | Ghost sessions across shifts | Shift selector + session expiry |
| Phase 3 | Checklist App — audit | No attribution on completions | Require location + staff name per session |

---

## Sources

- Square timecard export community discussion: https://community.squareup.com/t5/Questions-How-To/How-can-I-export-timecards/m-p/120215
- Square overtime / blended rate: https://squareup.com/help/us/en/article/6570-timecards-faqs
- DoorDash payout columns and error charges: https://merchants.doordash.com/en-us/learning-center/payout-and-monthly-statement
- DoorDash error charges: https://merchants.doordash.com/en-us/learning-center/doordash-merchant-refund
- UberEats payment details report: https://help.uber.com/en/merchants-and-restaurants/article/download-comprehensive-payment-details-reports
- Google Sheets concurrent write benchmark: https://tanaikech.github.io/2021/09/15/benchmark-concurrent-writing-to-google-spreadsheet-using-form/
- Google Apps Script LockService: https://developers.google.com/apps-script/reference/lock
- Google Sheets API rate limits: https://developers.google.com/workspace/sheets/api/limits
- Google Apps Script quotas: https://developers.google.com/apps-script/guides/services/quotas
- Restaurant COGS vs. invoice total: https://pos.toasttab.com/blog/on-the-line/restaurant-cost-of-goods-sold
- Food cost percentage pitfalls: https://get.chownow.com/blog/restaurant-food-cost-percentage/
- Square CSV wrong format / QuickBooks import issues: https://trestlefinance.com/guides/square-csv-export-wrong-format-quickbooks-fix
- Google Sheets as database limitations: https://medium.com/@eric_koleda/why-you-shouldnt-use-google-sheets-as-a-database-55958ea85d17
- Google Sheets 10M cell limit and performance: https://thodigitals.com/limitations-of-google-sheets/
- KitchenHub on commission model opacity: https://www.trykitchenhub.com/post/what-marketplaces-arent-telling-you-how-commission-models-are-quietly-changing

**Confidence levels:**
- Square CSV format issues: MEDIUM (community forum + official docs, no direct column mapping verified)
- Delivery platform column differences: MEDIUM (official help docs confirm different terminology, exact CSV headers not personally verified)
- COGS vs. invoice total pitfall: HIGH (multiple official restaurant accounting sources agree)
- Google Sheets concurrent write issue: HIGH (Google official docs + benchmark data)
- Overtime cross-location edge case: HIGH (Square official docs confirm blended rate behavior)
- Grubhub payout lag: LOW (widely reported in restaurant owner communities, not officially documented)
- BEK non-food line items: LOW (logical inference from broadline distributor model; verify with Rez's actual invoices)
