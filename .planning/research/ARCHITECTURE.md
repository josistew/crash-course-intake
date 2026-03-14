# Architecture Patterns

**Domain:** Restaurant operations automation suite — multi-location, hybrid spreadsheet + web app
**Researched:** 2026-03-14
**Confidence:** HIGH (component architecture), MEDIUM (CSV format specifics), HIGH (Google Sheets API patterns)

---

## System Overview

Three distinct subsystems that share one Google account as their integration layer:

```
[CSV Exports from Square / DoorDash / UberEats / Grubhub / BEK]
        |
        v
[Reporting Sheet — import tabs + formula engine]
        |
        v
[Summary Tab — consolidated view, payroll prep output]

[Checklist App (Next.js)]
        |
        v  (Google Sheets API via Service Account)
[Checklist Sheet — completion log]
        |
        v
[Manager View tab — live dashboard]
```

These subsystems are **loosely coupled**. The reporting Sheet and the checklist Sheet are separate files. They share a Google account but do not reference each other's data. This is intentional — it keeps each system independently testable, avoids formula fragility across files, and lets Rez share each with different people.

---

## Component Boundaries

### Component 1: Weekly Reporting Sheet

**Responsibility:** Accept raw data pastes, calculate metrics, surface variance flags, produce consolidated summary.

**Inputs:**
- Square sales CSV (one per location, weekly)
- Square clock-in CSV (one per location, weekly)
- DoorDash Merchant Portal weekly CSV (downloadable from Reports > Create Report)
- UberEats Restaurant Manager CSV (similar reporting portal)
- Grubhub Restaurant Hub CSV
- BEK Entree invoice/order CSV (food distributor export)

**Internal tab structure:**

| Tab | Purpose |
|-----|---------|
| `[Location]-Import` (x5) | Paste raw CSV data here per location |
| `[Platform]-Import` | Paste raw delivery platform CSVs here |
| `BEK-Import` | Paste BEK food cost data here |
| `[Location]-Calc` (x5) | Formula-driven calculations per location |
| `Summary` | QUERY/SUMIF consolidation across all locations |
| `WoW-Variance` | Week-over-week comparison with conditional formatting |

**Outputs:**
- Summary tab visible to Rez and ops partner (share Sheet, not export)
- Payroll prep tab (formatted for Gusto CSV import or manual entry)

**Does NOT communicate with:** Checklist app directly. No cross-file references.

---

### Component 2: Payroll Sheet (may live as tabs in Reporting Sheet)

**Responsibility:** Track labor hours, overtime flags, graduated pay tiers, produce Gusto-ready output.

**Decision point:** This can be additional tabs in the Reporting Sheet or a separate Sheet file. Recommendation — tabs within the same Reporting Sheet for v1, since all source data (Square clock-in exports) is already flowing there. Split into its own file only if the Reporting Sheet becomes unwieldy.

**Inputs:**
- Square clock-in CSV (same import tab used by Reporting Sheet — avoid double entry)

**Internal structure:**

| Tab | Purpose |
|-----|---------|
| `Hours-Raw` | Parsed hours per employee per week |
| `Overtime-Tracker` | Running weekly OT calculation with alerts |
| `Pay-Tiers` | Milestone tracker (90 days, cert dates, current tier) |
| `Payroll-Output` | Gusto-ready format — regular hours, OT, any adjustments |

**Outputs:**
- Payroll-Output tab: Rez downloads or copies to Gusto

---

### Component 3: CSV Parsing Pipeline

**What it is:** NOT a separate system — it is the import tab pattern baked into the Reporting Sheet itself.

**Mechanism:**

Two approaches, ordered by preference:

1. **Paste-in import tabs (v1 — recommended):** Rez copies CSV content from each platform's export, pastes into a dedicated import tab. Formulas reference those tabs. Zero external tooling, zero OAuth, zero setup friction.

2. **Apps Script trigger (v1.5, optional enhancement):** A bound Apps Script on the Reporting Sheet can accept a CSV file dropped into a designated Drive folder and auto-paste it to the correct import tab. Uses `Utilities.parseCsv()` + `sheet.getRange().setValues()`. This is an upgrade path, not a requirement for v1.

**Format realities per source:**

| Source | Export mechanism | Key columns expected |
|--------|-----------------|---------------------|
| Square Sales | Dashboard > Reports > Sales Summary > Export | Date, Location, Gross Sales, Net Sales, Discounts, Refunds, Taxes |
| Square Clock-In | Dashboard > Team > Shifts > Export shifts | Employee name, Job, Clock-in, Clock-out, Total hours, Location |
| DoorDash | Merchant Portal > Reports > Create Report > Financial or Sales > Download CSV | Date, Order count, Subtotal, Commission, Payout |
| UberEats | Restaurant Manager > Reports > Download | Date, Orders, Gross sales, Marketplace fee, Net payout |
| Grubhub | Restaurant Hub > Financials > Export | Date, Net sales, Commission, Adjustment, Payout |
| BEK Entree | Account portal > Export invoice history | Invoice date, Item, Category, Qty, Unit cost, Total |

**Note:** Exact column names vary by account configuration and platform version. The import tabs should be flexible — use row 1 as a "raw header" reference, parse by column index or MATCH() rather than hardcoded column letters. This prevents breakage when DoorDash renames a column.

**Does NOT communicate with:** Next.js app. Entirely within Google Sheets.

---

### Component 4: Checklist Web App (Next.js)

**Responsibility:** Tablet-facing daily checklist UI. Serves opening/closing/cleaning/equipment checklists per location and shift. Writes completions to Google Sheets. Serves manager dashboard from same Sheet data.

**Internal structure:**

```
/app
  /page.tsx              — Location + shift selector landing
  /[location]/[shift]/   — Checklist view for that context
  /manager/              — Read-only dashboard, all locations
/app/api
  /complete/route.ts     — Server action: write completion to Sheet
  /checklist/route.ts    — Read checklist template from Sheet
/lib
  /sheets.ts             — Google Sheets API client (googleapis)
  /auth.ts               — Service account credential setup
```

**Google Sheet used as data store (separate file from Reporting Sheet):**

| Tab | Purpose |
|-----|---------|
| `Checklist-Template` | Master list of checklist items (editable by Rez) |
| `Completions-Log` | Append-only log: timestamp, location, shift, item, who |
| `Manager-View` | Pivot/QUERY summary by location × date (auto-calculated) |

**Authentication:**

Service Account (same pattern used in LeaseJenny dashboard). Next.js holds `GOOGLE_SERVICE_ACCOUNT_KEY` and `GOOGLE_SHEET_ID` as Vercel environment variables. No user-facing OAuth. Tablet accesses the bookmarked URL — no login required for checklist workers. Manager view is same URL path, not password-protected for v1 (Rez acceptable).

**Read path:** Next.js → Sheets API → `Checklist-Template` tab → render items
**Write path:** User taps complete → Server Action → Sheets API → append row to `Completions-Log`
**Manager view:** Next.js → Sheets API → `Manager-View` tab (QUERY formula pre-calculates in Sheet)

**Does NOT communicate with:** Reporting Sheet. Independent Google Sheet file.

---

## Data Flow

### Weekly Reporting Flow

```
Monday morning ritual:
1. Rez logs into Square, exports Sales CSV for each location → pastes into [Location]-Import tabs
2. Rez logs into Square, exports Shifts CSV → pastes into Hours-Raw import tab
3. Rez logs into DoorDash/UberEats/Grubhub portals, downloads weekly CSV each → pastes into platform import tabs
4. Rez logs into BEK Entree, exports invoice CSV → pastes into BEK-Import tab
5. Formula engine fires automatically → Summary tab updates → WoW-Variance flags populate
6. Rez reviews Summary, shares with ops partner
7. Rez opens Payroll-Output tab → copies to Gusto (or exports for manual entry)
```

### Checklist Completion Flow

```
Morning (store opens):
1. Staff picks up shared tablet, opens bookmarked URL
2. Taps location → taps shift (Opening)
3. Checklist items load from Checklist-Template tab
4. Staff taps each item as complete (optional note)
5. Each tap → Server Action → appends row to Completions-Log with timestamp

Evening (manager check):
6. Manager opens /manager route
7. Next.js reads Manager-View tab → shows completion status per location
```

---

## Suggested Build Order

Dependencies drive this order:

### Phase 1: CSV Import Architecture + Formula Engine (Reporting Sheet)

Build first because everything else depends on having clean data flowing in. No other component depends on this being perfect — but Rez cannot validate payroll or reporting outputs until this exists.

- Create Reporting Sheet with import tabs
- Build location-level calculation tabs with formulas for net revenue, food cost %, labor cost %, order volume, avg ticket
- Build Summary consolidation tab with QUERY across locations
- Add WoW variance logic and conditional formatting

**No code required — pure Sheets architecture.**

### Phase 2: Payroll Tabs (within Reporting Sheet)

Build second because it shares the same Square clock-in import tab from Phase 1. Adding payroll logic before Phase 1 is complete creates formula dependencies on unfinished data.

- Hours-Raw parsing from Square clock-in import
- Overtime-Tracker running total
- Pay-Tiers milestone tracker (manual data entry by Rez to seed)
- Payroll-Output formatted tab

**No code required.**

### Phase 3: Checklist Web App (Next.js)

Build third — completely independent of the Sheets reporting work. Can be built in parallel with Phase 2 by a second developer, but if sequential, build after reporting is validated so Rez's attention isn't split.

- Create Checklist Google Sheet with Template, Completions-Log, Manager-View tabs
- Scaffold Next.js app with Vercel deploy
- Implement Service Account auth
- Build location/shift selector UI
- Build checklist view with tap-to-complete
- Implement completions write via Server Actions
- Build manager dashboard view

**This is the only phase requiring code.**

---

## Integration Points Summary

| From | To | Mechanism | Direction |
|------|----|-----------|-----------|
| Rez (manual) | Reporting Sheet import tabs | Paste CSV | Push |
| Square export | Reporting Sheet | Manual paste, CSV format | Push |
| DoorDash/UberEats/Grubhub export | Reporting Sheet | Manual paste, CSV format | Push |
| BEK export | Reporting Sheet | Manual paste, CSV format | Push |
| Reporting Sheet formulas | Summary + Payroll tabs | QUERY / SUMIF / array formulas | Internal |
| Next.js checklist app | Checklist Sheet | Google Sheets API (Service Account) | Read + Write |
| Next.js manager view | Checklist Sheet | Google Sheets API (Service Account) | Read only |

There is intentionally **no integration between the Reporting Sheet and the Checklist Sheet** in v1. They are separate concerns, separate files, accessed by separate parties. Connecting them would add fragility and complexity for no immediate user value.

---

## Scalability Considerations

| Concern | Now (v1) | Later (Phase 2+) |
|---------|----------|-----------------|
| Data entry | Manual CSV paste weekly | Square API + DoorDash Reporting API (announced, available to merchants) |
| Reporting Sheet scale | 5 locations × 52 weeks easily within 5M cell limit | Fine indefinitely |
| Checklist data store | Google Sheets sufficient for daily logs across 5 locations | If approaching millions of rows, migrate Completions-Log to Supabase |
| Multi-user conflict | Not a concern — paste-in is single-writer | Not a concern |
| Next.js hosting | Vercel free tier | Free tier sufficient for internal-only tablet traffic |

---

## Critical Architecture Decisions

**Do not use cross-file IMPORTRANGE between Reporting Sheet and Checklist Sheet.** It creates dependency coupling that breaks when either file is renamed or permissions change.

**Do not store checklist completion data in the same Sheet as reporting data.** Operational write volume to the Checklist log tab (many rows per day, 5 locations) mixed with fragile reporting formulas creates instability.

**Use append-only log for checklist completions, not an update-in-place pattern.** Append via `spreadsheets.values.append` is the safest write operation with no race conditions and produces a full audit trail. Never try to update an existing row in the Completions-Log — only ever add new rows.

**Parse import tabs by column header match, not by fixed column letter.** DoorDash, UberEats, and Square all change their CSV column names without warning. Use MATCH() to find the right column dynamically: `=INDEX(A:A, MATCH("Net Sales", 1:1, 0))`.

---

## Sources

- [Google Sheets as Database with Next.js — The New Stack](https://thenewstack.io/how-to-use-google-sheets-as-a-database-with-react-and-ssr/)
- [Next.js 14 App Router Google Sheets Integration — DEV Community](https://dev.to/julimancan/use-nextjs-14-app-router-to-store-subscriber-info-in-google-sheets-for-free-4jea)
- [Import CSV data with Apps Script — Google Developers](https://developers.google.com/apps-script/samples/automations/import-csv-sheets)
- [DoorDash Merchant Reporting — DoorDash Learning Center](https://merchants.doordash.com/en-us/learning-center/reporting)
- [DoorDash Available Reports — Developer Docs](https://developer.doordash.com/en-US/docs/reporting/overview/available_reports/)
- [Square Timecard and Scheduling Reports](https://squareup.com/help/us/en/article/6140-employee-timecard-reporting)
- [Custom Functions in Google Sheets — Google Developers](https://developers.google.com/apps-script/guides/sheets/functions)
- [Consolidating Multi-Tab Data in Google Sheets — The Bricks](https://www.thebricks.com/resources/guide-how-to-make-a-report-from-multiple-google-sheets)
