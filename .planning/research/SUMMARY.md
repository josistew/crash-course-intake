# Research Summary: Rez Operations Suite

**Project:** Moto Medi / Tikka Shack — 5-location restaurant operations automation
**Synthesized:** 2026-03-14
**Research files:** STACK.md, FEATURES.md, ARCHITECTURE.md, PITFALLS.md

---

## Executive Summary

Rez Operations Suite is a three-subsystem internal tool for a multi-location fast-casual operator running two brands across 5 locations. The system replaces a scattered manual workflow (multiple POS dashboards, platform portals, spreadsheets) with a consolidated weekly reporting engine, a payroll prep layer, and a tablet-facing daily checklist app. All three subsystems live within Google Workspace — two as Google Sheets with formula engines, one as a Next.js app that writes to Sheets via service account. This is not a SaaS product; it is purpose-built internal tooling for one client.

The recommended approach is strictly CSV-first for v1. Rather than building brittle API integrations against Square, DoorDash, UberEats, and Grubhub, the reporting system accepts weekly CSV pastes into import tabs, feeds formula-driven calculation tabs, and surfaces a consolidated Summary tab. This pattern has near-zero setup friction, stays entirely within Google Workspace where Rez already operates, and degrades gracefully when a platform changes its export format. The checklist app is the only component requiring code: a Next.js 15 app on Vercel using the same googleapis service account pattern already running on Josiah's stack.

The highest-risk elements are data quality problems, not code complexity. Delivery platform CSVs use inconsistent revenue definitions that will silently produce wrong consolidated totals if not mapped individually. Overtime calculations break if Square exports are pulled per-location rather than across all locations before aggregating hours. Food cost calculation must be labeled as "Food Purchases %" rather than "Food Cost %" until inventory count data is available. Building the paste zone, validation rows, and per-platform column mapping docs are more important to get right than any formula or UI.

---

## Key Findings

### From STACK.md

| Technology | Purpose | Rationale |
|------------|---------|-----------|
| Google Apps Script (V8) | Sheets automation — CSV parsing, custom menus, sheet-to-sheet writes | Zero deployment friction; runs inside Google Workspace; free |
| `Utilities.parseCsv()` (built-in GAS) | Parse pasted/uploaded CSV text | Handles quoted fields, embedded commas, CRLF — custom split() breaks on DoorDash edge cases |
| SpreadsheetApp `setValues()` (batch) | Write parsed data to raw tabs | Batch write is ~70x faster than cell-by-cell; must never call setValue() in a loop |
| Google Sheets `QUERY()` + named ranges | Calculated metrics and consolidation | SQL-like, readable by non-technical ops partner; auditable |
| Next.js 15.x + Vercel | Checklist web app | Proven on Josiah's stack (LeaseJenny); App Router server actions keep credentials server-side |
| Tailwind CSS v4.x | Checklist app styling | v4 required with Next.js 15 Turbopack — v3 has a documented `fs` resolution bug with Turbopack |
| `googleapis` 171.x + `google-spreadsheet` 5.2.0 | Sheets API from Next.js | Official Google client + higher-level wrapper; same service account pattern as LeaseJenny |

**Critical version constraints:**
- Use Tailwind v4, not v3, for Next.js 15 Turbopack compatibility
- Do NOT use `next-pwa` (webpack conflict with Turbopack) or `react-papaparse` (unmaintained)
- Do NOT use `shadcn/ui` with Tailwind v4 until shadcn fully supports it

**Gusto note:** Smart Import is flexible on column order and names — but verify the exact required headers from Gusto's sample template before building the payroll output tab.

---

### From FEATURES.md

**Table Stakes — build these or it's worse than manual:**

Weekly Reporting:
- Net revenue per location per week (Square + delivery CSVs combined)
- Food purchases % as proxy for food cost (BEK Entree CSV / food sales)
- Labor cost % (Square hours + wage lookup)
- Week-over-week comparison with variance flags (>5% threshold)
- Consolidated summary across all 5 locations (rollup tab)
- Cross-brand comparison (Moto Medi vs Tikka Shack)

Payroll Prep:
- Daily + weekly hours per employee from Square clock-in CSV
- Overtime flag and calculation (Texas: federal 40hr/week only)
- Graduated pay tier tracker (90-day and certification milestones)
- Gusto-ready export format (match their import template exactly)

Daily Checklist:
- Opening, closing, cleaning, equipment checklists per location
- Location + shift selector at session start
- Tap-to-complete with timestamp and staff name
- Optional notes per item
- Manager dashboard — all-location completion status

**Differentiators worth building in v1:**
- Tablet-optimized UI (large tap targets, not mobile-responsive afterthought — shared store tablet is the actual device)
- Per-platform delivery revenue labeled separately (DD Net Revenue, UE Net Revenue, GH Net Revenue)
- BEK Entree integration with explicit "Food Purchases %" label

**Anti-features — explicitly do not build in v1:**
- API-based auto-pull from any platform (high setup cost, brittle, not needed yet)
- User accounts / authentication for checklist app (friction for shared tablet; name entry at session start is sufficient)
- Real-time clock-in monitoring (Rez confirmed end-of-day summaries are sufficient)
- Inventory management, in-app scheduling, push notifications, recipe costing
- Multi-tenant abstraction (build for Rez specifically; extract patterns later)

---

### From ARCHITECTURE.md

Three loosely coupled subsystems sharing one Google account as the integration layer — intentionally no cross-file IMPORTRANGE references:

**Component 1: Weekly Reporting Sheet (Google Sheets)**
- Import tabs per location + per platform receive paste-in CSV data
- Calculation tabs (per location) apply formula engine: net revenue, food%, labor%, order volume, avg ticket
- Summary tab: QUERY consolidation across all locations
- WoW-Variance tab: conditional formatting with color-coded thresholds
- Tab structure is append-only historical: date-keyed rows, never row-offset formulas

**Component 2: Payroll Tabs (within Reporting Sheet)**
- Hours-Raw: parsed from Square clock-in import (same import tab as Component 1 — no double entry)
- Overtime-Tracker: cross-location aggregate before 40hr threshold, not per-location
- Pay-Tiers: milestone tracker seeded manually by Rez
- Payroll-Output: formatted to match Gusto import template exactly

**Component 3: CSV Parsing Pipeline**
- Not a separate system — the import tab pattern inside the Reporting Sheet
- Each platform has its own named mapping function; routes through platform selector
- Parse by column header name (MATCH()), never by fixed column index — platforms rename columns without warning
- Paste Zone → Cleaned Data transform applies VALUE(), DATEVALUE(), TRIM() before any formula touches the data

**Component 4: Checklist Web App (Next.js)**
- Separate Google Sheet (never references Reporting Sheet)
- Checklist-Template tab: master task list editable by Rez
- Completions-Log tab: append-only (spreadsheets.values.append only — never update in place)
- Manager-View tab: QUERY pre-calculates summary; Next.js reads it, doesn't compute it
- No authentication for v1; location + staff name captured at session start

**Critical architecture decisions:**
- No IMPORTRANGE between Reporting Sheet and Checklist Sheet
- Parse import tabs by column header MATCH(), not column index
- Append-only writes to Completions-Log (no race condition risk from single-row appends)
- All Google credentials in Vercel env vars only — never client-side

---

### From PITFALLS.md

**Top pitfalls ordered by severity:**

**Critical — address before building:**

1. **Delivery platform revenue definitions differ** (Phase 1) — DoorDash "Subtotal," UberEats "Sales," and Grubhub net revenue are not equivalent. Summing them produces wrong consolidated totals. *Prevention: Manually map one week's CSV from each platform before writing a single VLOOKUP. Always use net payout column. Label columns "DD Net Revenue," "UE Net Revenue," "GH Net Revenue" — never a single "Delivery Revenue."*

2. **Food cost % label is wrong if using invoice totals** (Phase 1) — BEK invoice total ÷ sales produces a purchase ratio, not true COGS. Week-to-week swings will be misleading. *Prevention: Label the column "Food Purchases %" explicitly. Add cell note documenting the limitation. Build true COGS only when inventory count data is available.*

3. **Square CSV export format varies by report type** (Phase 1 + 2) — Sales Summary, Transaction-level, and Labor CSVs have fundamentally different structures. Column visibility toggles in the Square dashboard change what's exported. *Prevention: Document exact export path step-by-step. Use MATCH() on header names, never fixed column indices. Validate with Rez via screen share on first use.*

4. **Overtime breaks for multi-location employees** (Phase 2) — If Square exports are pulled per location, an employee at 22hrs in each of two locations shows 0 overtime. Federal law requires aggregate. *Prevention: Use Square's "Labor cost by location" CSV which includes all locations. Aggregate hours by employee across all location tabs before applying 40hr threshold.*

5. **Concurrent write collisions on Sheets checklist backend** (Phase 3) — Two staff tapping simultaneously can lose one write. Sheets has no row-level locking. *Prevention: Append-only writes via spreadsheets.values.append (atomic for single rows). Implement exponential backoff on API errors. Consider Vercel KV as write buffer if volume warrants.*

**Moderate pitfalls:**

6. **Paste zone data type parsing** — Pasting CSV directly into Sheets cells imports dollar amounts and dates as text strings. SUM returns 0 silently. *Prevention: Paste Zone → Cleaned Data tab with VALUE(), DATEVALUE(), TRIM(). Add ISNUMBER() validation row.*

7. **WoW comparison breaks on data archival** — Row-offset formulas ("previous week is 1 row up") fail when data is archived. *Prevention: Date-keyed VLOOKUP/MATCH for all cross-week references.*

8. **Grubhub payout lag** — Grubhub statements lag 7-10 days, causing blank columns on Monday morning reporting. *Prevention: Per-platform "Last Updated" date cell + conditional format flag when Grubhub is stale.*

9. **Tab rename breaks Summary formulas** — Location tab names referenced by string will produce #REF errors if renamed. *Prevention: Use location ID codes in data (MML, TSL, etc.) and QUERY/FILTER against IDs, not tab names.*

10. **Ghost checklist sessions** — Shared tablet retains a prior shift's partial session. *Prevention: Shift selector prominently on load; sessions keyed on location + date + shift; prior shift visible but read-only.*

---

## Implications for Roadmap

The feature dependency chain and pitfall distribution strongly support a 3-phase build that mirrors the research's own recommendation. The order is driven by data dependencies and risk concentration, not complexity.

### Suggested Phase Structure

---

**Phase 1: Weekly Reporting Sheet**

*Rationale:* All other systems are downstream of having clean data flowing. This is the highest-ROI deliverable — eliminates Rez's most time-consuming manual work immediately. Contains the most dangerous pitfalls (delivery platform mismatches, food cost labeling, paste zone data parsing) which must be designed correctly from the start, not retrofitted.

*Delivers:*
- Reporting Sheet with import tabs per location (Square) + per platform (DoorDash, UberEats, Grubhub) + BEK
- Paste Zone → Cleaned Data transform with ISNUMBER validation
- Per-location calculation tabs: net revenue, food purchases %, labor %, order volume, avg ticket
- Summary consolidation tab with cross-location + cross-brand view
- WoW-Variance tab with conditional formatting, date-keyed (not row-offset)
- Per-platform freshness date indicators

*Features from FEATURES.md:* Net revenue per location, food purchases %, labor %, order volume, avg ticket, WoW comparison + variance flags, consolidated summary, cross-brand comparison

*Pitfalls to prevent:* P1 (delivery revenue definitions), P2 (food cost label), P3 (Square export format), P6 (paste zone parsing), P7 (WoW row-offset), P8 (Grubhub lag), P9 (tab rename), P13 (BEK non-food items)

*No code required — pure Sheets architecture.*

*Research flag:* Low — Sheets formula patterns are well-documented. The only uncertainty is exact CSV column names from DoorDash/UberEats/Grubhub/Square, which must be validated against Rez's actual exports before formula build. Do NOT build formulas from assumed column names.

---

**Phase 2: Payroll Prep Tabs**

*Rationale:* Shares the Square clock-in import tab from Phase 1 — no additional data entry burden on Rez. Builds directly on the data pipeline established in Phase 1. Contains the second-highest-risk pitfall (overtime cross-location aggregation) which must be architecturally correct before Rez runs a single payroll.

*Delivers:*
- Hours-Raw tab: parsed from Square clock-in import (shared from Phase 1)
- Cross-location employee aggregation before overtime threshold
- Overtime-Tracker with TX-only rule labeled explicitly
- Pay-Tiers milestone tracker (seeded manually by Rez with hire dates, cert dates)
- Payroll-Output tab formatted to match Gusto import template exactly

*Features from FEATURES.md:* Daily + weekly hours per employee, overtime flag + calculation, graduated pay tier tracker, Gusto-ready export

*Pitfalls to prevent:* P4 (cross-location overtime), P11 (Gusto import format), P3 (Square clock-in CSV export path)

*No code required.*

*Research flag:* Low for hours/overtime logic; Medium for Gusto output tab — download Gusto's sample import template before designing the output tab structure, not after.

---

**Phase 3: Daily Checklist Web App**

*Rationale:* Completely independent of Phases 1-2 (separate Google Sheet, separate data store). Can be parallelized with Phase 2 if two developers are available. If sequential, build after reporting is validated so Rez's attention and trust is established before introducing a new system. Most visible to frontline staff — first impression matters.

*Delivers:*
- Checklist Google Sheet: Checklist-Template, Completions-Log, Manager-View tabs
- Next.js 15 app on Vercel with service account auth
- Location + shift selector (session-scoped, not user-scoped)
- Tap-to-complete checklist with timestamp + staff name capture
- Opening, closing, cleaning, equipment checklist categories per location
- Completions written via Server Actions → append-only to Completions-Log
- Manager dashboard reading from Manager-View tab (QUERY pre-calculated in Sheet)

*Features from FEATURES.md:* Full checklist feature set; tablet-optimized UI (large tap targets, clear shift context); manager dashboard

*Pitfalls to prevent:* P5 (concurrent write collisions — append-only model + exponential backoff), P9 (checklist context on completions — location + shift + staff per session), P12 (ghost sessions — session expiry + read-only prior shift view)

*This is the only phase requiring code.*

*Research flag:* Medium — Next.js + googleapis pattern is proven on Josiah's stack. The write-to-Sheets concurrent access question should be validated early: if Rez anticipates heavy simultaneous usage, evaluate Vercel KV as a write buffer before committing to direct Sheets writes.

---

**Phase 4 (Defer):**
- API-based auto-pull from Square, DoorDash, UberEats, Grubhub
- True COGS calculation (requires inventory count workflow)
- Actual vs. theoretical food cost (requires recipe data)
- Quarterly KPI bonus report (depends on stable Phase 1 baseline)
- Shift handoff notes

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Next.js 15 + googleapis + GAS pattern is proven on existing Josiah projects. Tailwind v4 is new but documented. |
| Features | MEDIUM-HIGH | Core features well-established from restaurant ops domain research. Rez-specific workflows inferred from project context — validate during kickoff. |
| Architecture | HIGH | Component boundaries, tab structure, and data flow are well-documented patterns. Append-only Sheets write pattern is solid. |
| Pitfalls | HIGH (COGS, Sheets concurrency, overtime logic) / MEDIUM (delivery CSV column names) / LOW (Grubhub payout lag, BEK category filter) | High-confidence pitfalls from official docs. Delivery CSV column names require hands-on validation with Rez's actual exports. |

**Overall Confidence: MEDIUM-HIGH**

---

## Gaps to Validate Before Building

These are known unknowns that research could not resolve — must be addressed in kickoff or during sample data collection:

1. **Exact CSV column names from DoorDash, UberEats, Grubhub, and Square** — Do not build any formulas until Rez exports one week of actual data from each platform. Column names are platform-specific, account-configuration-specific, and change without warning.

2. **Whether Rez does weekly inventory counts** — Determines whether true COGS calculation is achievable in Phase 1 or remains a Phase 4 item. If counts exist, the food cost calculation can be accurate from day one.

3. **BEK Entree invoice CSV structure** — Confirm whether the CSV has a food/non-food category column. If mixed with paper goods and cleaning supplies, the food cost calculation requires a filter step before summing.

4. **Gusto Smart Import column requirements** — Download Gusto's sample import template before building the Payroll-Output tab. Do not assume column names.

5. **Grubhub payout lag for Rez specifically** — Confirm actual lag with Rez before deciding whether Grubhub is included in Monday morning reporting or flagged as pending.

6. **Whether any employees work across multiple locations** — This determines whether the overtime pitfall (cross-location aggregation) is an immediate concern or a theoretical one. If it applies to even one employee, the payroll architecture must handle it correctly from Phase 2 day one.

7. **Checklist concurrent usage volume** — Confirm how many staff are on a shift at each location and whether simultaneous tablet use is realistic. This determines whether append-only Sheets writes are sufficient or a write buffer (Vercel KV) is needed.

---

## Sources (Aggregated)

**Google / Official:**
- [Google Apps Script Best Practices](https://developers.google.com/apps-script/guides/support/best-practices)
- [Apps Script CSV Import Sample](https://developers.google.com/apps-script/samples/automations/import-csv-sheets)
- [V8 Runtime Overview](https://developers.google.com/apps-script/guides/v8-runtime)
- [Node.js Quickstart — Google Sheets API](https://developers.google.com/workspace/sheets/api/quickstart/nodejs)
- [Google Apps Script LockService](https://developers.google.com/apps-script/reference/lock)
- [Google Sheets API rate limits](https://developers.google.com/workspace/sheets/api/limits)
- [Next.js PWA Guide](https://nextjs.org/docs/app/guides/progressive-web-apps)
- [Gusto Smart Import](https://support.gusto.com/article/999914471000000/Run-payroll-with-Smart-Import)

**Platform-Specific:**
- [DoorDash Merchant Financials](https://merchants.doordash.com/en-us/learning-center/financials)
- [DoorDash Payout and Monthly Statement](https://merchants.doordash.com/en-us/learning-center/payout-and-monthly-statement)
- [UberEats Comprehensive Payment Reports](https://help.uber.com/en/merchants-and-restaurants/article/download-comprehensive-payment-details-reports)
- [Square Labor vs Sales Report](https://squareup.com/help/us/en/article/6140-employee-timecard-reporting)
- [Square Overtime / Blended Rate](https://squareup.com/help/us/en/article/6570-timecards-faqs)

**Restaurant Industry:**
- [Restaurant COGS vs Invoice Total — Toast](https://pos.toasttab.com/blog/on-the-line/restaurant-cost-of-goods-sold)
- [Food Cost Percentage — Restaurant365](https://www.restaurant365.com/blog/how-to-calculate-food-cost-percentage-and-margins/)
- [Restaurant Technology Turning Point — FSR Magazine](https://www.fsrmagazine.com/feature/restaurants-reach-a-technology-turning-point-rooted-in-simplicity/)
- [Best Restaurant Ops Software 2026 — Operandio](https://operandio.com/best-restaurant-operations-software/)
- [Digital Checklists for Restaurants — StaffedUp](https://staffedup.com/digital-checklists-for-restaurants/)

**Technical:**
- [googleapis npm 171.4.0](https://www.npmjs.com/package/googleapis)
- [google-spreadsheet npm 5.2.0](https://www.npmjs.com/package/google-spreadsheet)
- [Tailwind CSS v4.0 release](https://tailwindcss.com/blog/tailwindcss-v4)
- [Tailwind v3 Turbopack fs bug](https://github.com/tailwindlabs/tailwindcss/issues/18997)
- [Concurrent Sheets write benchmark](https://tanaikech.github.io/2021/09/15/benchmark-concurrent-writing-to-google-spreadsheet-using-form/)
