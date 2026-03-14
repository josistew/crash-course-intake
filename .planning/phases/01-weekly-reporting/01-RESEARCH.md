# Phase 1: Weekly Reporting - Research

**Researched:** 2026-03-14
**Domain:** Google Sheets formula architecture — multi-platform CSV paste-in, MATCH-based column mapping, QUERY consolidation, WoW variance
**Confidence:** HIGH (Sheets formula patterns), MEDIUM (exact CSV column names — must validate with Rez's actual exports)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Import Workflow**
- One import tab per platform (5 tabs: Square, DoorDash, UberEats, Grubhub, BEK)
- Clear-and-paste: operator clears last week's data, pastes new CSV. Prior week stored in a separate "Prior Week" tab for comparison
- Instructions tab as the first tab: step-by-step guide for each platform ("Go to Square > Reports > Sales Summary > Export CSV > Paste into Square tab")
- Weekly batch cadence: all 5 CSVs pasted in one sitting, Monday morning ritual
- MATCH-based column headers in all formulas — survive CSV column reordering

**Metric Definitions**
- Net revenue = after all delivery fees/commissions (what hits Rez's bank account)
- Purchase cost % = BEK purchases / total revenue. Labeled "Purchase Cost %" (not "Food Cost %") to be honest about no inventory counts
- Labor cost uses employee roster tab with static pay rates (hours × rate = estimated labor cost)
- Timing: match by order/transaction date, not payout date — aligns revenue with the week it was earned

**Visual Presentation**
- Summary tab: locations as columns, metrics as rows. KPIs only (5-6 key numbers per location), drill into location tab for full breakdown
- Week-over-week: arrow + percentage next to each metric (↑ +3.2% or ↓ -7.1%). Red/green color coding for >5% swings
- Brand separation: color-coded sections — Moto Medi locations in one color band, Tikka Shack in another

### Claude's Discretion
- Sheet structure: Claude decides tab count, naming, and organization beyond the import/summary/location pattern
- Specific conditional formatting thresholds beyond the 5% variance flag
- How prior week data is stored and referenced

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| RPT-01 | Operator can paste Square Sales Summary CSV into an import tab and data auto-populates location metrics | MATCH() header lookup pattern; Square exports Date, Net Sales, Location columns — validate exact names with Rez |
| RPT-02 | Operator can paste DoorDash CSV into an import tab and delivery revenue/orders auto-populate | DoorDash Report Builder exports; Payout column = net payout after commission — verify with Rez's actual export |
| RPT-03 | Operator can paste UberEats CSV into an import tab and delivery revenue/orders auto-populate | UberEats Manager > Analytics export; Net payout column differs from DoorDash — separate MATCH lookup required |
| RPT-04 | Operator can paste Grubhub CSV into an import tab and delivery revenue/orders auto-populate | Grubhub Restaurant Hub > Reports; less consistent format — must validate before writing any formulas |
| RPT-05 | Operator can paste BEK Entree CSV into an import tab and purchase/COGS data auto-populates | BEK exports invoice totals + line items; confirm food/non-food category column exists before summing |
| RPT-06 | Each location has a dedicated tab showing net revenue, food cost %, labor cost %, order volume (by platform), and avg ticket size | Per-location Calc tab pattern with SUMIF against import tabs; MATCH-based column refs |
| RPT-07 | Consolidated summary tab shows all 5 locations side-by-side with brand grouping (Moto Medi vs Tikka Shack) | QUERY consolidation or named ranges; locations as columns; brand banding via background color |
| RPT-08 | Week-over-week comparison shows prior week values and percentage change for each metric | Prior Week tab stores last week's snapshot; MATCH/VLOOKUP by date key, never row-offset |
| RPT-09 | Variance flags highlight any metric that changed >5% week-over-week (color-coded: red/green) | Conditional formatting rules on variance % column; formulas produce ↑/↓ symbol + % text |
| RPT-10 | Import tabs use column header matching (MATCH function) so formulas survive CSV column reordering | MATCH("Column Name", 1:1, 0) → INDEX pattern; documented below in Code Examples |
</phase_requirements>

---

## Summary

Phase 1 is a pure Google Sheets build — no code, no Apps Script required for v1. The architecture is: 5 import tabs (one per platform) where Rez pastes raw CSVs weekly, 5 location calculation tabs where MATCH-based formulas extract and compute metrics, a Prior Week snapshot tab for WoW comparison, and a Summary tab that consolidates all 5 locations side-by-side.

The highest implementation risk is not formula complexity — it is CSV column name assumptions. DoorDash, UberEats, Grubhub, and Square all use different column names, and those names can vary by account configuration. Every formula referencing a platform-specific column must use MATCH() against the actual header row, never a hardcoded column letter (like `C2`) or index. The plan must include a validation step where Rez provides real CSV exports before any platform-specific formulas are written.

The second important design choice is the WoW comparison pattern. Row-offset formulas ("prior week is always one row up") break the moment data is archived or a row is inserted. The correct pattern is date-keyed lookup: store this week's metrics to a named "Prior Week" snapshot tab, and reference those cells by date using MATCH/VLOOKUP. This is more setup but never silently breaks.

**Primary recommendation:** Build tab structure and MATCH formula scaffolding first. Get Rez's real CSV exports before writing any platform-specific column lookups. One wrong column name silently returns zero revenue.

---

## Standard Stack

### Core (Google Sheets only — no code for Phase 1)

| Tool | Version | Purpose | Why Standard |
|------|---------|---------|--------------|
| Google Sheets MATCH() | Native | Locate a column by header name dynamically | Survives CSV column reordering without formula updates |
| Google Sheets INDEX() | Native | Return a value from a located column | Paired with MATCH; the canonical lookup pair for flexible CSV references |
| Google Sheets SUMIF() / SUMIFS() | Native | Sum revenue/cost/hours by location and date | Correct tool for summing across import tab rows filtered by criteria |
| Google Sheets QUERY() | Native | Consolidate multi-tab data in Summary tab | SQL-like syntax; more readable than nested SUMIFS for cross-location rollup |
| Google Sheets Conditional Formatting | Native | Red/green >5% variance flags | Built-in; no formulas required — rule applied to variance % cells |
| Google Sheets ISNUMBER() | Native | Validate that pasted data parsed as numbers, not text | Catches silent paste failures where dollar amounts land as text |
| Google Sheets VALUE() / DATEVALUE() | Native | Force text-pasted numbers and dates into correct types | Required in Paste Zone → Cleaned Data transform |
| Google Sheets ARRAYFORMULA() | Native | Apply a formula to an entire column without copying down | Keeps formulas in row 2 only; automatically expands as data is pasted |
| Google Sheets TEXT() | Native | Format WoW output as "↑ +3.2%" string | Combines symbol + percentage into a single display cell |

### Supporting

| Tool | Version | Purpose | When to Use |
|------|---------|---------|-------------|
| Google Sheets Named Ranges | Native | Make formulas readable and tab-rename-safe | All cross-tab references; avoids tab-name-in-formula brittleness |
| Google Sheets Data Validation | Native | Dropdown menus and input guards on roster tab | Employee roster pay rate cells; location selector cells |
| TRIM() | Native | Strip whitespace from pasted text values | DoorDash and UberEats exports sometimes include leading/trailing spaces in text columns |
| PROPER() / UPPER() | Native | Normalize employee name capitalization | Employee names from Square clock-in may vary in capitalization |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| MATCH() + INDEX() | Fixed column letters (e.g., `=C2`) | Fixed letters break instantly when CSV columns reorder. MATCH is required per CONTEXT.md. |
| MATCH() + INDEX() | VLOOKUP() | VLOOKUP requires the lookup column to be leftmost. MATCH+INDEX works on any column arrangement — correct for CSV imports where column order is unpredictable. |
| Date-keyed WoW snapshots | Row-offset (`=A2-A1` style) | Row-offset silently breaks on archive or row inserts. Date-keyed is the only safe approach for weekly data. |
| QUERY() for Summary | Multiple SUMIFS | SUMIFS work but produce verbose formulas hard to audit. QUERY is more maintainable for non-technical ops partner review. |

---

## Architecture Patterns

### Recommended Tab Structure

```
Tab 1:  [Instructions]          — First tab; step-by-step per platform; READ ONLY
Tab 2:  [Square-Import]         — Paste Square Sales Summary CSV here
Tab 3:  [DoorDash-Import]       — Paste DoorDash weekly CSV here
Tab 4:  [UberEats-Import]       — Paste UberEats weekly CSV here
Tab 5:  [Grubhub-Import]        — Paste Grubhub weekly CSV here
Tab 6:  [BEK-Import]            — Paste BEK Entree invoice CSV here
Tab 7:  [Employee-Roster]       — Static: employee names, locations, pay rates
Tab 8:  [Prior-Week]            — Snapshot of last week's metrics (manual or formula copy)
Tab 9:  [LOC1-Calc]             — Location 1 (e.g., Moto Medi Lubbock) calc tab
Tab 10: [LOC2-Calc]             — Location 2 calc tab
Tab 11: [LOC3-Calc]             — Location 3 calc tab
Tab 12: [LOC4-Calc]             — Location 4 calc tab
Tab 13: [LOC5-Calc]             — Location 5 calc tab
Tab 14: [Summary]               — Consolidated view, all 5 locations as columns
```

**Tab naming convention:** Use short IDs in formulas (MML, TSL, etc.), not full names. This prevents tab rename from breaking cross-references.

**Color scheme for tab groups:**
- Import tabs: one background color (e.g., blue-gray)
- Calc tabs: neutral
- Summary / Prior-Week: highlighted (e.g., amber — the tabs Rez actually uses)
- Instructions / Roster: light green (reference tabs)

### Pattern 1: MATCH-Based Column Lookup (Core Pattern — Required for RPT-10)

**What:** Find any column by its header name, regardless of what column letter it lands in after a CSV paste. Return a value from that column for a specific row.

**When to use:** Every formula that references an import tab column. No exceptions.

**Example:**
```
=INDEX(Square_Import!A:Z, ROW(), MATCH("Net Sales", Square_Import!1:1, 0))
```

For a SUMIF against a located column, use the helper pattern:
```
=SUMIF(
  INDEX(Square_Import!A:Z, 0, MATCH("Location", Square_Import!1:1, 0)),
  "Moto Medi Lubbock",
  INDEX(Square_Import!A:Z, 0, MATCH("Net Sales", Square_Import!1:1, 0))
)
```

This is verbose. Name the column ranges to make it readable:
- Define named range `SQ_Location` = `=INDEX(Square_Import!A:Z, 0, MATCH("Location", Square_Import!1:1, 0))`
- Define named range `SQ_NetSales` = `=INDEX(Square_Import!A:Z, 0, MATCH("Net Sales", Square_Import!1:1, 0))`
- Then: `=SUMIF(SQ_Location, "Moto Medi Lubbock", SQ_NetSales)`

**CRITICAL:** The column header string in MATCH must exactly match what the CSV exports. This is the one thing that cannot be resolved without Rez's actual CSV files. Build placeholder named ranges first; fill in the real column names after Rez provides sample exports.

### Pattern 2: Paste Zone → Data Type Validation

**What:** A validation row below the import paste area that confirms data was parsed correctly (as numbers, not text).

**When to use:** Row 2 of every import tab (or a dedicated validation section below the paste area).

**Example:**
```
Validation row formula (per metric column):
=IF(ISNUMBER(INDEX(Square_Import!A:Z, 3, MATCH("Net Sales", Square_Import!1:1, 0))),
   "OK",
   "PASTE ERROR — Net Sales is text, not number")
```

Format this row with red background if the result is not "OK". Rez will see it immediately.

**Why:** Google Sheets frequently imports dollar amounts and dates as text strings when pasted from CSV. SUM of text = 0. This is the most common silent failure mode.

### Pattern 3: Week-Over-Week with Date-Keyed Snapshots

**What:** Store this week's metric values to a Prior-Week tab (keyed by week-ending date). Next week, WoW formulas MATCH against that date to pull prior values.

**Structure of Prior-Week tab:**
```
Row 1:  [Header] Week Ending | MML Net Rev | MML Purchase% | MML Labor% | ... (all KPIs for all locations)
Row 2:  [Date]   2026-03-09  | 12400       | 28.4%         | 31.2%      | ...
Row 3:  [Date]   2026-03-16  | (this week, filled after Monday paste)
```

**WoW formula on Summary tab:**
```
=INDEX(PriorWeek!B:B,
  MATCH(TODAY()-7, PriorWeek!A:A, 0))
```

Or more robustly, reference a named "week ending date" cell that Rez sets manually each Monday:
```
=INDEX(PriorWeek!B:B,
  MATCH(WeekEndingDate-7, PriorWeek!A:A, 0))
```

**Variance flag formula:**
```
=(ThisWeekValue - PriorWeekValue) / PriorWeekValue
```

**WoW display string:**
```
=IF(VariancePct > 0,
  "↑ " & TEXT(VariancePct, "+0.0%"),
  "↓ " & TEXT(VariancePct, "0.0%"))
```

**Conditional formatting rule:** Apply to variance % cells. Green fill if > +5%, red fill if < -5%.

### Pattern 4: Net Revenue Calculation (Multi-Platform)

**What:** Each location's net revenue = Square net sales (in-person) + DD payout + UE payout + GH payout. Each payout column is the net-after-fees value.

**Formula structure (on each Location Calc tab):**
```
Net Revenue =
  SUMIFS(SQ_NetSales, SQ_Location, [location ID], SQ_Date, ">="&WeekStart, SQ_Date, "<="&WeekEnd)
  + SUMIFS(DD_Payout, DD_Location, [location ID], DD_Date, ">="&WeekStart, DD_Date, "<="&WeekEnd)
  + SUMIFS(UE_Payout, UE_Location, [location ID], UE_Date, ">="&WeekStart, UE_Date, "<="&WeekEnd)
  + SUMIFS(GH_Payout, GH_Location, [location ID], GH_Date, ">="&WeekStart, GH_Date, "<="&WeekEnd)
```

**IMPORTANT:** Never sum a "Subtotal" or "Gross Sales" column from delivery platforms. DoorDash "Subtotal," UberEats "Sales," and Grubhub "Net sales" represent different things. Always use the payout/net-payout column — the money that actually hits the bank account.

### Pattern 5: Purchase Cost % Calculation

**What:** BEK total purchases ÷ total revenue for the week. Labeled "Purchase Cost %" everywhere — never "Food Cost %."

**Formula:**
```
Purchase Cost % =
  SUMIFS(BEK_Amount, BEK_Date, ">="&WeekStart, BEK_Date, "<="&WeekEnd)
  / NetRevenue
```

**If BEK has a food/non-food category column** (must confirm with Rez):
```
= SUMIFS(BEK_Amount, BEK_Category, "Food", BEK_Date, ">="&WeekStart, BEK_Date, "<="&WeekEnd)
  / NetRevenue
```

**Cell note to add:** "Purchase Cost % = BEK invoice total ÷ net revenue. This tracks food purchasing, not true COGS (which requires inventory counts). Week-to-week swings reflect order timing, not consumption."

### Pattern 6: Labor Cost % from Employee Roster

**What:** Estimated labor = employee hours (from Square clock-in import) × pay rate (from Employee Roster tab). No live payroll integration.

**Employee Roster tab structure:**
```
Col A: Employee Name (matches Square clock-in name exactly)
Col B: Location (location ID code)
Col C: Hourly Pay Rate (number)
Col D: Hire Date
Col E: Pay Tier (lookup label)
```

**Labor cost formula (per location):**
```
For each employee at this location:
  EstimatedPay = ClockInHours × VLOOKUP(EmployeeName, EmployeeRoster, 3, FALSE)

Labor Cost % = SUM(all EstimatedPay at this location) / NetRevenue
```

**In practice:** Use SUMPRODUCT to avoid looping:
```
=SUMPRODUCT(
  (SQ_Labor_Location="MML") * SQ_Labor_Hours *
  IFERROR(VLOOKUP(SQ_Labor_Names, Roster_Range, 3, FALSE), 0)
) / NetRevenue
```

### Pattern 7: Summary Tab Layout

**What:** Locations as columns, KPIs as rows. Brand separation via background color bands.

```
                | Moto Medi Lubbock | Moto Medi Amarillo | Moto Medi [3rd] | Tikka Shack [1] | Tikka Shack [2]
─────────────────────────────────────────────────────────────────────────────────────────────────────────────
Net Revenue     |    $14,200        |    $11,800          |    $9,600       |    $8,100       |    $7,400
  WoW           |    ↑ +3.2%        |    ↓ -1.1%          |    ↑ +5.8%     |    ↓ -8.2%      |    ↑ +0.6%
─────────────────────────────────────────────────────────────────────────────────────────────────────────────
Purchase Cost % |    29.1%          |    31.4%            |    28.8%        |    32.1%        |    30.5%
  WoW           |    ↑ +1.2%        |    ↓ -0.5%          |    ↑ +2.1%     |    ↓ -7.3% 🔴  |    ↑ +0.3%
─────────────────────────────────────────────────────────────────────────────────────────────────────────────
Labor Cost %    |    ...            |    ...              |    ...          |    ...          |    ...
─────────────────────────────────────────────────────────────────────────────────────────────────────────────
Order Volume    |    ...            |    ...              |    ...          |    ...          |    ...
─────────────────────────────────────────────────────────────────────────────────────────────────────────────
Avg Ticket      |    ...            |    ...              |    ...          |    ...          |    ...
```

**Mobile consideration:** Rez checks this on his phone. Keep columns narrow. Use column freeze on the metric label column. Summary should be readable without horizontal scrolling at mobile viewport — limit to 6 columns max (label + 5 locations).

### Anti-Patterns to Avoid

- **Hardcoded column letters:** `=C2` breaks silently when CSV is re-exported with different column order. Always MATCH("Column Name", 1:1, 0).
- **Row-offset WoW formulas:** `=A2 - A1` (prior week is always 1 row up) breaks on any row insert, archive, or blank-row separator. Always date-keyed.
- **Summing gross/subtotal columns from delivery platforms:** Each platform defines these differently. Only use the net-payout column — the only safe cross-platform comparator.
- **Using "Food Cost %" label:** Must be "Purchase Cost %" everywhere. Wrong label misleads on a metric Rez uses for business decisions.
- **Referencing tab names as strings in formulas:** If a tab is renamed, the formula breaks. Use named ranges that point to the tab content instead.
- **Pasting platform data without type validation row:** Text-as-number silently sums to zero. Always include the ISNUMBER validation row.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Column location in CSV | Custom position counter | MATCH("Header", row1, 0) | Native, zero maintenance, correct for any column order |
| Cross-platform revenue rollup | Separate formula per platform pasted together | SUMIFS with date range on each platform's import tab | Structured, auditable, extensible when platform is added |
| Data type enforcement | Manual formatting instructions to Rez | VALUE() + DATEVALUE() + ISNUMBER() validation row | Automated detection; Rez doesn't need to know to format-as-number |
| Variance display formatting | Manual "type the arrow" instruction | TEXT() formula with IF() for direction | Never wrong, never stale |
| Tab-level metric reference | IMPORTRANGE between tabs | Named ranges pointing to calc tab results | Named ranges survive tab structure changes |

**Key insight:** The most dangerous custom solutions here are not code — they are formulas that embed assumptions (column positions, row positions, tab names) that will silently break when CSVs are re-exported.

---

## Common Pitfalls

### Pitfall 1: Delivery Platform Revenue Definitions Differ
**What goes wrong:** DoorDash "Subtotal," UberEats "Sales," and Grubhub "Net sales" are not the same thing. Summing them produces inflated or wrong consolidated revenue.
**Why it happens:** Each platform defines revenue differently — some include taxes, some include tips, some are pre-commission.
**How to avoid:** Always use the net payout column from each platform (money that actually transfers to Rez's bank account). Label columns individually: "DD Net Revenue," "UE Net Revenue," "GH Net Revenue" — never a generic "Delivery Revenue."
**Warning signs:** Consolidated revenue is higher than expected compared to bank deposits.

### Pitfall 2: CSV Columns Paste as Text, Not Numbers
**What goes wrong:** Dollar amounts and dates from copy-paste land as text strings. SUM(), SUMIF(), and SUMIFS() return 0 silently. Rez sees $0 net revenue.
**Why it happens:** Google Sheets cannot infer data types from clipboard paste. Currency-formatted strings ("$1,234.00") are not numbers.
**How to avoid:** Add a Paste Zone → Cleaned Data transform using VALUE() and DATEVALUE(). Include an ISNUMBER() validation row that turns red on failure.
**Warning signs:** SUM of a column returns 0 even when data is visibly present.

### Pitfall 3: Square CSV Format Varies by Report Type
**What goes wrong:** Square has multiple CSV exports (Sales Summary, Transaction-level, Labor). Column names differ between them. The wrong export type produces mismatched MATCH() results.
**Why it happens:** Square's dashboard has many export entry points, and users navigate to different ones.
**How to avoid:** Instructions tab must specify the exact navigation path for each export type ("Reports > Sales Summary > select date range > Export CSV"). MATCH on header names catches wrong export type by returning #N/A instead of silently wrong data.
**Warning signs:** MATCH() returns #N/A for expected column names; or data appears but wrong values (transaction-level has different columns than summary-level).

### Pitfall 4: WoW Formula Breaks on Row Changes
**What goes wrong:** Row-offset WoW formula ("prior week is always row 2") fails when any row is inserted, deleted, or data is archived.
**Why it happens:** Relative row references break the moment the spreadsheet structure changes.
**How to avoid:** Date-keyed lookups only. Prior-Week tab stores values by date in column A. WoW formulas MATCH against (WeekEndingDate - 7).
**Warning signs:** WoW column shows #REF!, or worse — shows a wrong number with no error.

### Pitfall 5: BEK Sum Includes Non-Food Items
**What goes wrong:** BEK invoice CSV includes paper goods, cleaning supplies, and packaging alongside food items. Summing the entire invoice overstates Purchase Cost %.
**Why it happens:** BEK is a full-service restaurant distributor, not food-only.
**How to avoid:** Confirm whether BEK CSV has a Category column. If yes, SUMIFS with Category filter for food items only. If no, note the limitation in a cell comment and label metric "BEK Total Purchases %" to be fully honest.
**Warning signs:** Purchase Cost % seems unusually high; cross-check one week of BEK invoices manually.

### Pitfall 6: Grubhub Payout Lag
**What goes wrong:** Grubhub payments are delayed 7-10 days. Monday morning reporting shows blank Grubhub column, which pulls down the consolidated total.
**Why it happens:** Grubhub's payment cycle lags the transaction date.
**How to avoid:** Add a "Last Updated" date cell per platform import tab. Conditional format that cell red if it is more than 7 days before the week ending date. Include a note in the Instructions tab warning about Grubhub lag.
**Warning signs:** Grubhub column blank every Monday morning; consolidated totals look low.

### Pitfall 7: Employee Name Mismatch Between Square and Roster
**What goes wrong:** VLOOKUP for pay rate against employee roster returns #N/A because Square exports "Robert Smith" but roster has "Bob Smith." Labor cost shows 0 for that employee.
**Why it happens:** Nicknames, name changes, or inconsistent capitalization between Square team management and the roster tab.
**How to avoid:** Include a "Name in Square" column in the Employee Roster tab (separate from "Display Name"). Use that column as the VLOOKUP key. Add IFERROR(VLOOKUP(...), "NAME MISMATCH - check roster") for visibility.
**Warning signs:** Labor cost % looks low; check for VLOOKUP errors in labor calc rows.

---

## Code Examples

Verified patterns for Google Sheets formula work:

### MATCH-Based Column Lookup (RPT-10)
```
// Find column by header, return all values in that column as a range:
=INDEX(Square_Import!A:Z, 0, MATCH("Net Sales", Square_Import!1:1, 0))

// SUMIF using MATCH-located columns:
=SUMIF(
  INDEX(Square_Import!A:Z, 0, MATCH("Location", Square_Import!1:1, 0)),
  "MML",
  INDEX(Square_Import!A:Z, 0, MATCH("Net Sales", Square_Import!1:1, 0))
)
```

### Data Type Validation Row
```
// In a validation row below the paste area:
=IF(
  ISNUMBER(INDEX(Square_Import!A:Z, 3, MATCH("Net Sales", Square_Import!1:1, 0))),
  "OK",
  "ERROR: Net Sales is text. Re-paste and check format."
)
```

### WoW Variance Display String
```
// WeekEndDate = named cell with current week ending date
// PriorWeek_NetRev = named range pointing to prior week net revenue column

ThisWeek = [SUMIFS formula for current week net revenue]
PriorWeek = INDEX(PriorWeek!B:B, MATCH(WeekEndDate-7, PriorWeek!A:A, 0))
VariancePct = (ThisWeek - PriorWeek) / PriorWeek

// Display cell:
=IF(VariancePct >= 0,
  "↑ " & TEXT(VariancePct, "+0.0%"),
  "↓ " & TEXT(ABS(VariancePct), "0.0%"))
```

### Conditional Formatting Rule for Variance Flags
```
// Applied to variance % cells (not display string cells):
Rule 1: Cell value > 0.05  → Green fill (#d9ead3)
Rule 2: Cell value < -0.05 → Red fill (#fce8e6)
Rule 3: No other rules needed (within ±5% = neutral, no fill)
```

### Purchase Cost % with Category Filter
```
// If BEK CSV has a Category column:
=SUMIFS(
  INDEX(BEK_Import!A:Z, 0, MATCH("Total", BEK_Import!1:1, 0)),
  INDEX(BEK_Import!A:Z, 0, MATCH("Category", BEK_Import!1:1, 0)), "Food",
  INDEX(BEK_Import!A:Z, 0, MATCH("Invoice Date", BEK_Import!1:1, 0)), ">="&WeekStart,
  INDEX(BEK_Import!A:Z, 0, MATCH("Invoice Date", BEK_Import!1:1, 0)), "<="&WeekEnd
) / NetRevenue
```

### Labor Cost Estimate via SUMPRODUCT
```
// Assumes SQ_Labor_Names, SQ_Labor_Hours, SQ_Labor_Location are named ranges
// Roster_NameCol and Roster_RateCol are named ranges from Employee Roster tab
=SUMPRODUCT(
  (SQ_Labor_Location = "MML") *
  SQ_Labor_Hours *
  IFERROR(MATCH(SQ_Labor_Names, Roster_NameCol, 0), 0) *
  IFERROR(INDEX(Roster_RateCol, MATCH(SQ_Labor_Names, Roster_NameCol, 0)), 0)
) / MML_NetRevenue
```

### QUERY for Summary Consolidation (alternative to SUMIFS)
```
// If all location calc tabs have a standardized output row with location ID:
=QUERY(
  {LOC1_Calc!A:F; LOC2_Calc!A:F; LOC3_Calc!A:F; LOC4_Calc!A:F; LOC5_Calc!A:F},
  "SELECT Col1, SUM(Col2), SUM(Col3) WHERE Col1 IS NOT NULL GROUP BY Col1 LABEL SUM(Col2) 'Net Revenue'",
  1
)
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| VLOOKUP (column left-to-right only) | INDEX + MATCH (any column) | Always available, but INDEX+MATCH is now the standard recommendation | MATCH on header names enables CSV-resilient formulas |
| Fixed column letters in formulas | MATCH() on header row | Industry shift as CSV sources became common | Formulas survive platform export changes |
| Separate Sheets file for each platform | Multiple import tabs in one Sheet | Standard multi-tab pattern | Simpler for operator; one file to share |
| Row-based date navigation | Date-keyed VLOOKUP/MATCH for history | Emerged as best practice for reporting Sheets | WoW comparison never silently breaks |

**Deprecated/outdated:**
- VLOOKUP alone: cannot look left, brittle when columns reorder — use INDEX+MATCH
- Row-offset "prior week" references: silently wrong after any row change — use date-keyed
- Single "Delivery Revenue" total: meaningless across platforms — label and track per-platform

---

## Open Questions

1. **Exact CSV column names from each platform**
   - What we know: Each platform has documented export formats; general column categories are known (net payout, order count, date)
   - What's unclear: Exact column header strings that Rez's specific account and export path will produce. DoorDash Report Builder has configurable columns. Square column names differ by export type.
   - Recommendation: Build the tab structure and name placeholder named ranges. Do not finalize any MATCH("Column Name") string until Rez exports one week of real data from each platform. Validate via screen share or sample files before building the full formula suite.

2. **BEK Entree CSV — food vs. non-food category column**
   - What we know: BEK sells food and non-food items (paper goods, cleaning supplies)
   - What's unclear: Whether BEK's CSV export includes a product category column that can filter food-only rows
   - Recommendation: Rez should export one BEK invoice CSV and share column list. If category column exists, use SUMIFS filter. If not, sum all BEK purchases and label explicitly as "BEK Total Purchases %" with a cell note.

3. **Grubhub payout lag — actual timing for Rez's account**
   - What we know: Grubhub is documented as having slower payout cycles than DoorDash/Uber
   - What's unclear: Whether Rez experiences this as a Monday morning blank or whether his Grubhub data is available same-week
   - Recommendation: Note it in instructions tab; add the "Last Updated" date cell per import tab as a standard pattern. Rez will tell us on first use whether Grubhub is always blank on Monday.

4. **Location identifiers in Square and delivery platform CSVs**
   - What we know: Square allows location-level filtering in exports; delivery platforms may or may not include a location column (some accounts may have separate merchant accounts per location)
   - What's unclear: Whether Rez has one Square account covering all 5 locations (one CSV, filter by location) or separate accounts (separate CSVs per location)
   - Recommendation: Confirm account structure with Rez. If separate accounts, the import tab structure changes (one tab per location-platform pair instead of one tab per platform filtered by location).

---

## Validation Architecture

> `nyquist_validation` is enabled in config.json — section required.

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Manual formula audit + cell validation rows (no automated test framework — pure Sheets build) |
| Config file | None — validation is built into the Sheet itself (ISNUMBER rows, named range checks) |
| Quick run command | Open Summary tab → check all validation rows show "OK" → check variance column has no #N/A or #REF! |
| Full suite command | Paste one week of real CSV from each platform → confirm all 5 KPIs populate correctly per location |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| RPT-01 | Square CSV paste auto-populates location metrics | Manual smoke | Paste Square CSV → verify MML Net Revenue cell shows non-zero number | ❌ Wave 0: add ISNUMBER validation row to Square-Import tab |
| RPT-02 | DoorDash CSV paste auto-populates delivery revenue/orders | Manual smoke | Paste DoorDash CSV → verify DD Net Revenue per location | ❌ Wave 0: add ISNUMBER validation row to DoorDash-Import tab |
| RPT-03 | UberEats CSV paste auto-populates delivery revenue/orders | Manual smoke | Paste UberEats CSV → verify UE Net Revenue per location | ❌ Wave 0: add ISNUMBER validation row to UberEats-Import tab |
| RPT-04 | Grubhub CSV paste auto-populates delivery revenue/orders | Manual smoke | Paste Grubhub CSV → verify GH Net Revenue per location | ❌ Wave 0: add ISNUMBER validation row to Grubhub-Import tab |
| RPT-05 | BEK CSV paste auto-populates purchase/COGS data | Manual smoke | Paste BEK CSV → verify Purchase Cost % is a reasonable % (not 0, not >100%) | ❌ Wave 0: add ISNUMBER validation row to BEK-Import tab |
| RPT-06 | Location tabs show all 5 KPIs | Unit (formula check) | Open each Location Calc tab → verify all 5 KPI cells show numbers, no errors | ❌ Wave 0: build location calc tabs with all required KPI formulas |
| RPT-07 | Summary tab shows 5 locations side-by-side with brand grouping | Visual + formula | Open Summary tab → verify 5 location columns, Moto Medi and Tikka Shack sections color-coded | ❌ Wave 0: build Summary tab layout |
| RPT-08 | WoW comparison shows prior week values and change % | Integration | Populate Prior-Week tab manually with test data → verify WoW % calculates correctly | ❌ Wave 0: build Prior-Week tab and WoW formulas |
| RPT-09 | Variance flags highlight >5% changes with red/green | Visual | Manually set a metric to >5% change → verify conditional formatting fires | ❌ Wave 0: add conditional formatting rules to variance % cells |
| RPT-10 | Formulas survive CSV column reordering | Unit (resilience test) | Reorder columns in Square-Import paste → verify metrics still populate correctly | ❌ Wave 0: implement MATCH pattern on all import column references |

### Sampling Rate
- **Per task commit:** Open Summary tab, confirm all KPI cells are non-error and non-zero (with test data pasted)
- **Per wave merge:** Full paste of sample CSVs for all 5 platforms → all 5 location tabs → Summary tab review → WoW comparison check
- **Phase gate:** All 10 RPT requirements verified with Rez's real exported CSVs before marking Phase 1 complete

### Wave 0 Gaps
- [ ] `Square-Import` tab — ISNUMBER validation row covering Net Sales, Date, Location columns
- [ ] `DoorDash-Import` tab — ISNUMBER validation row covering net payout, order count, date columns
- [ ] `UberEats-Import` tab — ISNUMBER validation row
- [ ] `Grubhub-Import` tab — ISNUMBER validation row + "Last Updated" date cell with staleness flag
- [ ] `BEK-Import` tab — ISNUMBER validation row for amount/total column
- [ ] `Prior-Week` tab — date-keyed structure (column A = week ending date, columns B-Z = KPI values per location)
- [ ] All 5 `[LOC]-Calc` tabs — KPI formula rows covering all 5 metrics (RPT-06)
- [ ] `Summary` tab — layout with locations as columns, KPI rows, WoW display cells (RPT-07, RPT-08)
- [ ] Conditional formatting rules on variance % cells in Summary tab (RPT-09)
- [ ] Named ranges for all MATCH-based column lookups on each import tab (RPT-10)
- [ ] `Employee-Roster` tab with name/location/rate structure (supports labor cost % formulas)
- [ ] `Instructions` tab — step-by-step per platform (first tab, as decided in CONTEXT.md)

*(All gaps are Sheets structure — no test framework install required)*

---

## Sources

### Primary (HIGH confidence)
- Google Sheets MATCH() + INDEX() — native function documentation (behavior verified; canonical lookup pattern for CSV imports)
- Google Sheets SUMIFS() — native function (standard multi-criteria aggregation)
- Google Sheets QUERY() — native function (SQL-like cross-range consolidation)
- Google Sheets Conditional Formatting — native feature (rules applied to value ranges)
- [Google Apps Script Best Practices](https://developers.google.com/apps-script/guides/support/best-practices) — batch write pattern, Utilities.parseCsv()
- [Apps Script CSV Import Sample](https://developers.google.com/apps-script/samples/automations/import-csv-sheets) — official import pattern
- [DoorDash Merchant Financials](https://merchants.doordash.com/en-us/learning-center/financials) — payout column documentation
- [UberEats Comprehensive Payment Reports](https://help.uber.com/en/merchants-and-restaurants/article/download-comprehensive-payment-details-reports) — analytics download path
- [Square Labor vs Sales Report](https://squareup.com/help/us/en/article/6140-employee-timecard-reporting) — exact report path for clock-in exports

### Secondary (MEDIUM confidence)
- [Restaurant COGS vs Invoice Total — Toast](https://pos.toasttab.com/blog/on-the-line/restaurant-cost-of-goods-sold) — supports "Purchase Cost %" vs "Food Cost %" labeling decision
- [Restaurant365 — Food Cost Percentage](https://www.restaurant365.com/blog/how-to-calculate-food-cost-percentage-and-margins/) — industry standard definitions
- DoorDash Report Builder column specifics — confirmed via merchant portal docs; exact column names require Rez's account validation

### Tertiary (LOW confidence — must validate with Rez's real exports)
- Exact DoorDash CSV column names — known generally ("Payout," "Commission"), exact strings unconfirmed
- Exact UberEats CSV column names — known generally ("Net payout," "Marketplace fee"), exact strings unconfirmed
- Exact Grubhub CSV column names — least consistent platform; treat as unknown until Rez exports sample
- BEK Entree CSV category column — existence unconfirmed; must validate before building food-filter formula

---

## Metadata

**Confidence breakdown:**
- Standard stack (Google Sheets formula patterns): HIGH — MATCH/INDEX/SUMIF/QUERY are well-documented native functions; patterns are stable
- Tab architecture: HIGH — clear separation of import, calc, summary, and prior-week tabs is a standard Sheets reporting pattern
- Formula patterns: HIGH — MATCH-based column lookup, date-keyed WoW, ISNUMBER validation are proven patterns
- Platform-specific CSV column names: LOW — must be validated against Rez's actual exports before any formulas are finalized
- BEK category filter: LOW — category column existence unconfirmed

**Research date:** 2026-03-14
**Valid until:** 2026-09-14 (formula patterns are stable; platform CSV formats may change — re-validate column names if DoorDash/Uber update their portals)
