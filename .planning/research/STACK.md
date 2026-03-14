# Technology Stack

**Project:** Rez Operations Suite (Moto Medi / Tikka Shack)
**Researched:** 2026-03-14
**Overall confidence:** HIGH for web app layer; MEDIUM for CSV schema specifics (platform-dependent)

---

## Recommended Stack

### System 1: Google Sheets Reporting & Payroll (Google Apps Script)

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Google Apps Script (V8 runtime) | Current (auto-managed by Google) | All automation inside Sheets: CSV parsing, formula wiring, custom menus, sheet-to-sheet writes | Zero deployment friction — runs entirely inside Google Workspace, which Rez already lives in. No server, no auth setup, no API keys from Rez required. |
| `Utilities.parseCsv()` | Built-in GAS | Parse pasted/uploaded CSV text from Square, DoorDash, UberEats, Grubhub, BEK | Native method, handles delimiter edge cases, no dependencies. For large files, Blob + parsing via DriveApp is the fallback. |
| SpreadsheetApp `setValues()` (batch) | Built-in GAS | Write parsed data to raw data tabs in one call | Single batch write is ~70x faster than cell-by-cell writes. Critical rule: never call setValue() in a loop — always accumulate a 2D array and setValues() once. |
| Google Sheets named ranges + `QUERY()` | Built-in Sheets | Calculated metrics: food cost %, labor %, week-over-week variance | QUERY is SQL-like, readable by a non-technical ops partner. Named ranges make formula auditing possible. Conditional formatting handles variance flag coloring. |
| Apps Script time-driven triggers | Built-in GAS | Optional: future auto-pull or scheduled cleanup tasks | Already supported in GAS — not needed for v1 CSV-paste workflow but ready to enable. |

**Architecture pattern for GAS:** Custom menu → user pastes CSV text into a dialog or a staging cell → script reads that cell, Utilities.parseCsv() it, writes to a hidden "raw" tab, then pivot/QUERY formulas in reporting tabs pull from raw data. This keeps data entry and formula logic fully decoupled.

**Confidence:** HIGH — Google Apps Script is the canonical tool for Sheets automation. V8 runtime is the current default. Batch setValues() performance advantage is well-documented in official GAS best practices.

---

### System 2: Daily Checklist Web App (Next.js + Vercel + Google Sheets backend)

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Next.js | 15.x (15.2.x current as of March 2026) | App framework | Proven pattern already running on Josiah's stack (LeaseJenny dashboard). App Router + server actions keep Google Sheets writes off the client — no credentials leak. Vercel free tier handles 5-location tablet traffic easily. |
| Tailwind CSS | v4.x | Styling | v4 released January 2025. New CSS-first config (@theme in global.css, no tailwind.config.js) plays correctly with Next.js 15 Turbopack — Tailwind v3 has a known Turbopack `fs` resolution bug. Greenfield project: use v4. |
| `googleapis` npm | 171.x (171.4.0 verified) | Google Sheets read/write from Next.js server actions | Google's official Node.js client. Used for checklist completion writes and manager dashboard reads. JWT auth via service account — same pattern as LeaseJenny. |
| `google-spreadsheet` npm | 5.2.0 (verified current) | Alternative/supplement to raw googleapis for Sheets ops | Higher-level wrapper that simplifies row-level operations. Use for checklist submission writes where you need append-row semantics. Use raw googleapis for bulk reads in the manager dashboard where you need range-level control. |
| Vercel | Free tier | Hosting | Zero config with Next.js, existing pattern in Josiah's stack. Tablet bookmark URL is stable. |

**What NOT to use:**
- `next-pwa` (webpack-based, conflicts with Turbopack in Next.js 15) — use Next.js native PWA manifest support instead if offline mode is needed (it isn't for v1)
- `react-papaparse` — last published 2 years ago, not actively maintained; use papaparse directly if CSV parsing is needed client-side
- `shadcn/ui` with Tailwind v4 — shadcn's `tailwindcss-animate` dependency had migration pain as of March 2025; if using shadcn, pin Tailwind v3 until shadcn fully supports v4

**Confidence:** HIGH for Next.js + Vercel pattern (proven on this stack), HIGH for googleapis, MEDIUM for Tailwind v4 (very new; minor edge cases with specific plugin combos)

---

### System 3: CSV Data Sources (Square, Delivery Platforms, BEK)

| Source | Export Method | Key Data Points | Notes |
|--------|--------------|-----------------|-------|
| Square POS (Sales) | Dashboard → Reports → Export CSV | Gross sales, net sales, discounts, taxes, refunds by day/location | Square export UI is reliable; location filter available per report |
| Square Shifts (Labor) | Dashboard → Reports → Operations → Labor vs. Sales → Export CSV | Team member name, clock-in, clock-out, hours, tips | Labor vs. Sales CSV is the correct report — not the raw timecard view |
| DoorDash | Merchant Portal → Report Builder | Sales, fees, commission, payout, order count | Report Builder Financial CSV includes UTC + local timestamps; two separate reports often needed (Transactions Overview + Payouts) |
| UberEats | Uber Eats Manager → Analytics → Download | Similar structure to DoorDash; net sales, service fees, order count | Column names differ from DoorDash — GAS script must handle each platform with a separate parser/mapper |
| Grubhub | Grubhub Restaurant Portal → Reports | Weekly summaries, payouts | Less consistent export format than DoorDash/Uber; treat as a separate mapping case |
| BEK Entree | BEK online portal → CSV export | Invoice totals, line items, food category breakdown | Primary use: food cost calculation. BEK exports are consistent and well-structured. |
| Gusto (output, not input) | Sheet generates → Rez pastes into Gusto Smart Import | Employee name, hours (decimal), pay type | Gusto Smart Import accepts flexible CSV formats and auto-maps columns — no rigid template required. Hours must be decimal (8.5 not 8:30). |

**CSV parsing strategy for GAS:**
Each platform gets its own named mapping function in the Apps Script codebase. A platform selector in the custom menu routes the parsed CSV through the correct column-mapping config. This isolates breakage: if DoorDash changes their export format, only one function needs updating.

**Confidence:** MEDIUM — DoorDash column specifics verified via merchant portal docs; UberEats and Grubhub column names require confirmation against Rez's actual exports. Gusto Smart Import flexibility confirmed via official Gusto help docs.

---

### Supporting Libraries (Next.js app only)

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `papaparse` | 5.5.3 (verified current) | Client-side CSV parse if drag-and-drop CSV upload UI is added to web app | Only needed if the checklist app grows to include a reporting upload UI. Not needed for v1 checklist-only scope. |
| `date-fns` | 4.x | Date formatting for checklist timestamps, week-over-week calculations | Lightweight, tree-shakeable, no Moment.js baggage |
| `zustand` | 5.x | Lightweight client state for checklist UI (current step, location selection, completion state before submit) | Simpler than Redux for this use case; no server state needed since completion is submitted immediately |

---

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| Sheets automation | Google Apps Script | Zapier / Make | Zapier costs money at scale; GAS is free and stays inside Google Workspace. Rez already uses Zapier elsewhere — keeping reporting logic in GAS avoids another paid dependency. |
| Sheets automation | Google Apps Script | Python script + Google Sheets API | Requires a server or scheduled cloud function to run — unnecessary complexity when GAS runs natively inside Sheets. |
| Web app | Next.js 15 | Remix | Next.js is the proven pattern on Josiah's stack (LeaseJenny). No reason to switch frameworks mid-engagement. |
| Styling | Tailwind v4 | CSS Modules | Tailwind v4's speed advantage is real (5ms incremental builds vs 44ms in v3). Tablet-facing UI needs rapid iteration. |
| Database | Google Sheets (googleapis) | Supabase / PlanetScale | Rez already lives in Google Workspace; Sheets is inspectable without a dashboard. Supabase adds auth, schema management, and a separate billing surface for a checklist that stores ~50 rows/day. |
| CSV parsing (GAS) | `Utilities.parseCsv()` | Custom split() logic | Built-in method handles quoted fields, embedded commas, and CRLF line endings correctly. Custom parsing breaks on edge cases in DoorDash exports. |

---

## Installation

```bash
# Next.js checklist app (create new project)
npx create-next-app@latest rez-checklist --typescript --tailwind --app

# Core dependencies
npm install googleapis google-spreadsheet date-fns zustand

# Dev dependencies
npm install -D @types/node
```

**Note on Tailwind v4:** `create-next-app` with `--tailwind` installs whichever Tailwind version is current at time of scaffolding. Verify `tailwind` version after creation — if v3 is installed, upgrade:

```bash
npm install tailwindcss@latest @tailwindcss/postcss@latest
```

**Google Apps Script:** No npm. Open the Sheet → Extensions → Apps Script. Paste script directly. Enable V8 runtime under Project Settings (it's the default for new scripts created after 2020).

---

## Key Architectural Constraints

1. **No client-side Google credentials.** All Sheets reads/writes from the Next.js app must go through server actions or API routes. Service account JSON lives in Vercel env vars only.

2. **Batch writes in GAS.** Never setValue() in a loop. Always: read all CSV data → build 2D array → one setValues() call. Execution time limit is 6 minutes per GAS run; batch writes stay well under this for 5-location weekly data.

3. **Separate raw tabs from formula tabs.** GAS writes to "raw_square", "raw_doordash", etc. All QUERY/SUMIF formulas reference these tabs. This prevents GAS from overwriting formula cells.

4. **Platform CSV schema is volatile.** DoorDash and UberEats have changed their export formats historically. Build one mapping config object per platform rather than hardcoded column indices — makes updates a single-line change.

---

## Sources

- [Google Apps Script Best Practices — official](https://developers.google.com/apps-script/guides/support/best-practices)
- [Apps Script CSV Import Sample — official](https://developers.google.com/apps-script/samples/automations/import-csv-sheets)
- [V8 Runtime Overview — official](https://developers.google.com/apps-script/guides/v8-runtime)
- [Node.js Quickstart — Google Sheets API official](https://developers.google.com/workspace/sheets/api/quickstart/nodejs)
- [googleapis npm — 171.4.0](https://www.npmjs.com/package/googleapis) (version verified via npm CLI)
- [google-spreadsheet npm — 5.2.0](https://www.npmjs.com/package/google-spreadsheet) (version verified via npm CLI)
- [papaparse npm — 5.5.3](https://www.npmjs.com/package/papaparse) (version verified via npm CLI)
- [Next.js — 15.1.6](https://www.npmjs.com/package/next) (version verified via npm CLI)
- [Tailwind CSS v4.0 release announcement](https://tailwindcss.com/blog/tailwindcss-v4)
- [Next.js PWA Guide — official](https://nextjs.org/docs/app/guides/progressive-web-apps)
- [Gusto Smart Import — official help](https://support.gusto.com/article/999914471000000/Run-payroll-with-Smart-Import)
- [DoorDash Merchant Financials — official](https://merchants.doordash.com/en-us/learning-center/financials)
- [Square Labor vs Sales Report — official](https://squareup.com/help/us/en/article/6140-employee-timecard-reporting)
- [Tailwind v3 Turbopack fs bug (GitHub)](https://github.com/tailwindlabs/tailwindcss/issues/18997)
