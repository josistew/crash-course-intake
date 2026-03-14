# Phase 2: Payroll Prep - Research

**Researched:** 2026-03-14
**Domain:** openpyxl workbook extension — Square Labor CSV import, cross-location overtime aggregation, pay tier milestone tracking, Gusto Smart Import output tab
**Confidence:** HIGH (formula patterns, openpyxl extension), MEDIUM (Gusto column mapping flexibility), LOW (exact Square Labor CSV column names — must validate with Rez's real export)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Import Workflow**
- Square POS is the clock-in system
- One Square Labor CSV paste per pay period
- Cross-location hours aggregated per employee BEFORE overtime threshold (PAY-04)
- Daily breakdown showing hours per day, rolling into weekly total

**Overtime Tracking**
- Color-coded: green (<32 hrs), yellow (32-38 hrs), red (38+ hrs)
- Running tracker through the week — flags approaching overtime by mid-week
- Federal 40-hour weekly threshold (Texas has no state OT law — federal only)

**Pay Tier Tracking**
- Graduated = milestone-based raises at 90 days and certifications (confirmed by Rez)
- Employee roster: hire date, current rate, tier, next milestone date, days-until
- Auto-flag when approaching a milestone
- Exact tier rules and raise amounts TBD — need from Rez on Monday

**Gusto Integration**
- Gusto is the payroll system
- Output tab formatted for Gusto Smart Import (flexible column mapping)
- Columns needed: employee name, total hours, overtime hours, current pay rate
- Rez reviews the prep tab then submits to Gusto manually

### Claude's Discretion
- Whether payroll lives in the same workbook as weekly reporting or a separate file
- Tab naming and organization within the payroll section
- How the Employee Roster from Phase 1 is reused or extended
- Specific conditional formatting details beyond the green/yellow/red scheme

### Deferred Ideas (OUT OF SCOPE)
- Square API integration for automated labor data pull (v2)
- Direct Gusto API submission (v2)
- Daily automated clock-in summary push (v2)
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| PAY-01 | Operator can paste Square Labor CSV and daily hours per employee per location auto-populate | MATCH-based column lookup on Square Labor import tab; same pattern as Phase 1 import tabs |
| PAY-02 | Weekly total hours per employee calculated with running daily breakdown | SUMIFS by employee name + date range; daily columns computed via SUMIFS filtered to single date |
| PAY-03 | Overtime tracker flags employees approaching 40 hours by mid-week (green <32, yellow 32-38, red 38+) | SUMIFS cross-location aggregate → conditional formatting FormulaRule pattern from Phase 1 |
| PAY-04 | Cross-location hours aggregated per employee before overtime threshold applied | Single Labor-Import tab with Location column; SUMIFS on employee name across ALL locations before comparison to 40hr threshold |
| PAY-05 | Employee roster tab with hire date, pay rate, pay tier, next milestone date, days-until-milestone | Extends existing Employee-Roster tab; add Hire Date, Next Milestone, Days Until columns with TODAY()-based formula |
| PAY-06 | Pay tier tracker auto-flags employees approaching a graduated raise milestone | Conditional formatting on Days-Until column (<=30 days = flag); TODAY()-milestone date formula |
| PAY-07 | Gusto-ready prep output tab with employee name, total hours, overtime hours, current pay rate | Gusto Smart Import is flexible — any clear column headers work; no rigid template required |
</phase_requirements>

---

## Summary

Phase 2 extends the Phase 1 openpyxl workbook by adding four new tabs: a Square Labor import tab, an Overtime Tracker tab, an extended Employee Roster (or pay tier addendum), and a Gusto-Output tab. All formula patterns are identical to Phase 1 — MATCH-based column headers, SUMIFS for aggregation, conditional formatting via FormulaRule. No new libraries or techniques are required.

The architectural decision of whether to extend the existing workbook or create a separate payroll file should be resolved in favor of the same workbook. The Labor-Import tab shares the same paste-in pattern as the other import tabs already built in Phase 1, and the Employee Roster already exists. Extending the workbook keeps Rez in one file and avoids IMPORTRANGE brittleness across files. Tab ordering simply appends the payroll section after the Summary tab.

The highest-risk element in this phase is the cross-location overtime calculation. The formula must aggregate hours across ALL locations for a given employee before comparing to 40 hours. If individual per-location SUMIFS are written instead, an employee working 25 hours at location A and 20 hours at location B shows zero overtime — but legally owes 5 hours at 1.5x. The architecture must use a single Labor-Import tab covering all locations, not separate per-location labor tabs. Gusto Smart Import is genuinely flexible: it accepts any column order and auto-maps, so the output tab design is low-risk once the hours aggregation is correct.

**Primary recommendation:** Extend the Phase 1 workbook. Add Labor-Import, Overtime-Tracker, and Payroll-Output tabs. The Employee Roster tab already has Hire Date and Pay Tier columns — extend it in place with milestone date and days-until columns rather than creating a duplicate tab.

---

## Standard Stack

### Core (extending Phase 1 — no new libraries)

| Tool | Version | Purpose | Why Standard |
|------|---------|---------|--------------|
| openpyxl | 3.1.x (same as Phase 1) | Extend workbook with new tabs | Already installed; same patterns already used in build_weekly_report.py |
| Google Sheets SUMIFS() | Native | Aggregate hours by employee across all locations and by date | Multi-criteria: employee name + date range (or specific date) + week boundary |
| Google Sheets MATCH() + INDEX() | Native | Locate Square Labor CSV columns by header name | Same MATCH pattern from Phase 1; handles column reordering |
| Google Sheets conditional formatting (FormulaRule) | Native | Green/yellow/red overtime zones | Same FormulaRule pattern already used for WoW variance flags in Phase 1 |
| Google Sheets TODAY() | Native | Days-until-milestone calculation | `=milestone_date - TODAY()` updates automatically each day without re-pasting |
| Google Sheets ISNUMBER() | Native | Validate pasted labor data parsed as numbers not text | Same validation row pattern from Phase 1 import tabs |

### Supporting

| Tool | Version | Purpose | When to Use |
|------|---------|---------|-------------|
| Google Sheets VLOOKUP / IFERROR | Native | Look up pay rate from Roster for each employee in output tab | Join hours to rate; IFERROR catches name mismatches |
| Google Sheets MAX() with 0 | Native | Compute overtime hours = MAX(total - 40, 0) | Prevents negative overtime values |
| openpyxl FormulaRule | 3.1.x | Conditional formatting for overtime zones | Same class already imported in build_weekly_report.py |
| openpyxl DataValidation | 3.1.x | Location dropdown on Labor-Import tab | Already used in Employee Roster builder |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Extending Phase 1 workbook | Separate payroll .xlsx file | Separate file avoids tab clutter but requires Rez to manage two files. Single file wins: one place to paste, one file to share with accountant. |
| Single Labor-Import tab (all locations) | Separate labor import per location | Per-location tabs make cross-location overtime aggregation fragile and error-prone. Single tab with Location column is architecturally correct. |
| SUMIFS for cross-location aggregate | SUMPRODUCT | Both work. SUMIFS is more readable for a non-technical reviewer; SUMPRODUCT is needed if employee names need fuzzy/trim matching. Start with SUMIFS, fall back to SUMPRODUCT if name-match errors occur. |

**Installation:** No new packages. Phase 1's openpyxl install is sufficient:
```bash
pip3 install openpyxl  # already installed from Phase 1
```

---

## Architecture Patterns

### Recommended Tab Structure (Phase 2 additions, inserted after Summary)

```
[existing Phase 1 tabs: Instructions → ... → Summary]
↓ Phase 2 appends:
Tab 15: [Labor-Import]      — Paste Square Labor CSV here (all locations in one paste)
Tab 16: [Overtime-Tracker]  — Cross-location aggregate per employee; green/yellow/red
Tab 17: [Payroll-Output]    — Gusto-ready: name, total hrs, OT hrs, pay rate, gross est.
```

The Employee-Roster tab (Tab 7 from Phase 1) is extended in place — milestone date and days-until columns are added as new columns to the right of the existing structure. No new Roster tab is created.

### Pattern 1: Single Labor-Import Tab (Critical for PAY-04)

**What:** One Square Labor import tab covering all 5 locations in a single paste. The CSV already contains a Location column. SUMIFS filters by employee + location + date.

**Why this is critical:** If Rez exports labor data separately per location and uses separate import tabs, an employee appearing in two location exports will have their hours summed independently. Cross-location overtime aggregation requires all rows in one table.

**Square Labor CSV — confirmed structure (placeholder headers):**
```
Row 1: [Headers — validate exact names with Rez's real export]
       Date | Employee Name | Location | Job Title | Clock In | Clock Out | Regular Hours | Overtime Hours | Total Hours
Row 2+: [One row per shift per employee]
```

**IMPORTANT:** Square's "Export Shifts" creates one row per shift (not one row per employee per day). An employee working a split shift has two rows. Aggregation must use SUMIFS across all rows for that employee, not assume one row per employee per day.

**MATCH-based column lookup (same pattern as Phase 1):**
```
// Named range for Total Hours column from Labor-Import:
=INDEX('Labor-Import'!A:Z, 0, MATCH("Total Hours", 'Labor-Import'!1:1, 0))

// Named range for Employee Name column:
=INDEX('Labor-Import'!A:Z, 0, MATCH("Employee Name", 'Labor-Import'!1:1, 0))

// Named range for Date column:
=INDEX('Labor-Import'!A:Z, 0, MATCH("Date", 'Labor-Import'!1:1, 0))
```

Column name strings ("Total Hours", "Employee Name") are placeholders — must be replaced with Rez's actual export headers.

### Pattern 2: Cross-Location Hours Aggregation (Core of PAY-02, PAY-04)

**What:** For each employee, sum ALL their hours from the Labor-Import tab regardless of which location they worked. Then apply overtime threshold.

**Overtime-Tracker tab layout:**
```
Col A: Employee Name (unique list — pulled from Roster or manually keyed)
Col B: Mon Hours   (SUMIFS: employee + date = Monday)
Col C: Tue Hours
Col D: Wed Hours
Col E: Thu Hours
Col F: Fri Hours
Col G: Sat Hours
Col H: Sun Hours
Col I: Weekly Total   (=SUM(B:H) for this employee's row)
Col J: Overtime Hours (=MAX(I-40, 0))
Col K: Regular Hours  (=MIN(I, 40))
Col L: Status         (=IF(I>=38,"HIGH",IF(I>=32,"WARN","OK")) — drives conditional formatting
```

**Weekly total formula (all locations, all shifts):**
```
// Employee name in A2; WeekStart and WeekEnd are named cells on Overtime-Tracker tab
=SUMIFS(
  LaborHours,        // named range: Total Hours column from Labor-Import
  LaborEmployee,     // named range: Employee Name column
  A2,                // this employee
  LaborDate,         // named range: Date column
  ">="&WeekStart,
  LaborDate,
  "<="&WeekEnd
)
```

**Daily breakdown formula (e.g., Monday column):**
```
=SUMIFS(
  LaborHours,
  LaborEmployee, A2,
  LaborDate, Monday_Date  // named cell or formula: WeekStart + 0 for Mon, +1 for Tue, etc.
)
```

**Overtime hours:**
```
=MAX(WeeklyTotal - 40, 0)
```

**Status cell (drives conditional formatting):**
```
=IF(WeeklyTotal >= 38, "HIGH", IF(WeeklyTotal >= 32, "WARN", "OK"))
```

### Pattern 3: Overtime Color-Coding (PAY-03)

Apply conditional formatting to the Weekly Total column (Col I) on Overtime-Tracker tab. Use FormulaRule against the Status column or directly against the value:

**FormulaRule for green/yellow/red on Col I:**
```python
# In openpyxl builder (same pattern as Phase 1 WoW rules):
from openpyxl.formatting.rule import CellIsRule, FormulaRule

# Red: 38+ hours (overtime threshold approaching/exceeded)
red_rule = CellIsRule(
    operator="greaterThanOrEqual", formula=["38"],
    fill=PatternFill(fgColor="FCE8E6")
)
# Yellow: 32-38 hours (approaching)
yellow_rule = FormulaRule(
    formula=["AND(I2>=32, I2<38)"],
    fill=PatternFill(fgColor="FFF9C4")
)
# Green: under 32 hours (safe)
green_rule = CellIsRule(
    operator="lessThan", formula=["32"],
    fill=PatternFill(fgColor="D9EAD3")
)

ws.conditional_formatting.add("I2:I50", red_rule)
ws.conditional_formatting.add("I2:I50", yellow_rule)
ws.conditional_formatting.add("I2:I50", green_rule)
```

**Priority note:** openpyxl applies rules in the order added. Red must be added before Yellow so the red rule takes priority over yellow for values >= 38.

### Pattern 4: Pay Tier Milestone Tracking (PAY-05, PAY-06)

**What:** Extend the existing Employee-Roster tab with columns for milestone tracking. No separate tab needed.

**Additional columns to add to Employee Roster (continuing from col G "Notes"):**
```
Col H: Next Milestone Date   (date value — manually set by Rez; e.g., hire_date + 90)
Col I: Milestone Type        (text: "90-Day Review", "Food Handler Cert", "Shift Lead Cert", etc.)
Col J: Days Until Milestone  (formula: =H2 - TODAY()   — auto-updates daily)
Col K: Milestone Status      (formula: =IF(J2<=0,"OVERDUE",IF(J2<=30,"SOON","OK")) — drives flag)
```

**Days Until formula:**
```
=H2 - TODAY()
```
Format as number (not date). Negative = overdue. Zero = due today. Positive = days remaining.

**Conditional formatting on Days Until column (Col J):**
```python
# Orange flag: milestone within 30 days
milestone_warn = FormulaRule(
    formula=["AND(J2>0, J2<=30)"],
    fill=PatternFill(fgColor="FFE0B2"),  # amber
    font=Font(bold=True)
)
# Red flag: milestone overdue (negative days)
milestone_overdue = FormulaRule(
    formula=["J2<=0"],
    fill=PatternFill(fgColor="FCE8E6"),
    font=Font(bold=True, color="CC0000")
)
```

**Note on tier rules:** Rez has not yet provided the exact milestone amounts and tier progression rules. The roster structure should be built with Milestone Date and Type columns. The actual dates and types will be entered by Rez. The formula for Days Until and the conditional flag work regardless of the specific tier rules.

### Pattern 5: Gusto-Output Tab (PAY-07)

**What:** A formatted output tab Rez can copy-paste or export to Gusto's Smart Import.

**Gusto Smart Import behavior (MEDIUM confidence):**
- Accepts any file format: .csv, .xlsx, and many others
- Accepts any column order — auto-maps during import wizard
- No rigid required column names — Rez maps columns interactively on first use
- Zeros override previously entered information; blanks do not

**Output tab column structure (use clear, descriptive names Gusto will auto-recognize):**
```
Col A: Employee Name        (VLOOKUP from Overtime-Tracker → Employee-Roster)
Col B: Regular Hours        (=MIN(WeeklyTotal, 40)  — capped at 40)
Col C: Overtime Hours       (=MAX(WeeklyTotal - 40, 0))
Col D: Current Pay Rate     (VLOOKUP from Employee-Roster Hourly Rate column)
Col E: Estimated Gross Pay  (= Regular Hours * Rate + Overtime Hours * Rate * 1.5)
Col F: Pay Period           (named cell showing week ending date)
```

**Column naming note:** Gusto recognizes "Regular Hours," "Overtime Hours," "Employee Name" as common patterns. Use these exact strings in the header row. When Gusto's import wizard appears, it will auto-suggest mappings and Rez confirms them. After the first successful import, Gusto saves the mapping — subsequent imports are one-click.

**Formula for Employee Name column (pulling from Overtime-Tracker employee list):**
```
// Direct reference — Payroll-Output Col A links to Overtime-Tracker Col A
='Overtime-Tracker'!A2
```

**Formula for Pay Rate column:**
```
=IFERROR(
  VLOOKUP(A2, 'Employee-Roster'!A:D, 4, FALSE),
  "RATE NOT FOUND — check Roster"
)
```

**Estimated Gross Pay:**
```
=(B2 * D2) + (C2 * D2 * 1.5)
```

Label as "Estimated Gross Pay" with a cell note: "This estimate uses the current pay rate from the Employee Roster. Verify against Gusto for actual payroll amounts — tips, deductions, and tax withholding are not included."

### Pattern 6: Extending the openpyxl Script (Implementation Pattern)

**What:** Phase 2 adds new builder functions to `build_weekly_report.py` and appends new tab definitions to the `tab_defs` list in `build_workbook()`.

**Pattern — extend tab_defs:**
```python
# In build_workbook(), after the existing tab definitions:
tab_defs = [
    # ... existing Phase 1 tabs ...
    ("Labor-Import",     TAB_IMPORT, lambda ws: build_labor_import(ws)),
    ("Overtime-Tracker", TAB_AMBER,  lambda ws: build_overtime_tracker(ws)),
    ("Payroll-Output",   TAB_AMBER,  lambda ws: build_payroll_output(ws)),
]
```

**Employee-Roster extension — add columns in build_employee_roster():**
The function already writes 7 columns. Phase 2 adds cols H-K by appending to the header list and extending the data rows.

**Do NOT create a new build_employee_roster_v2() function.** Extend the existing one in-place so the tab position (Tab 7) and color remain unchanged.

**New sample data in sample_data.py:**
Add `SQUARE_LABOR_HEADERS` already exists (placeholder). Add `PAYROLL_OUTPUT_SAMPLE` list with computed rows based on existing `SQUARE_LABOR_SAMPLE_ROWS` and `EMPLOYEE_ROSTER`.

### Anti-Patterns to Avoid

- **Separate labor import tab per location:** Makes PAY-04 (cross-location OT) impossible to implement correctly. All locations in one tab.
- **Computing OT per location before aggregating:** `MAX(loc_a_hours - 40, 0) + MAX(loc_b_hours - 40, 0)` is legally wrong. Aggregate first, then apply threshold.
- **Creating a separate payroll workbook file:** Forces Rez to manage two files and breaks the shared Employee Roster. Extend the same workbook.
- **Hardcoding Square Labor column letters:** Square's export format is subject to change. All column references via MATCH on header name.
- **Assuming one row per employee per day in Square export:** Square "Export Shifts" creates one row per shift. A split-shift employee has multiple rows per day. SUMIFS must aggregate all rows.
- **Using TODAY() as the week start reference:** TODAY() changes daily, which would make daily breakdowns recalculate inconsistently. Use a named "Week Start" cell that Rez sets manually each Monday (same pattern as WeekEndingDate in Phase 1).

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Cross-location OT aggregation | Custom loop summing per-location then combining | Single SUMIFS on one Labor-Import tab with all locations | SUMIFS handles this natively; per-location approach has wrong math |
| Days-until-milestone countdown | Manual date calculator or JavaScript date math | `=milestone_date - TODAY()` | TODAY() is native; auto-updates every day without any code |
| Overtime cap at 40 hours | IF(total>40, total-40, 0) — readable but requires two cells | `=MAX(total-40, 0)` | Idiomatic single-cell formula; handles edge case of exactly 40 cleanly |
| Regular hours capped at 40 | Another IF | `=MIN(total, 40)` | Same pattern — idiomatic |
| Gusto column mapping | Custom rigid template matching Gusto internals exactly | Clear descriptive headers + let Gusto Smart Import auto-map | Gusto's importer is genuinely flexible; building a rigid template creates a maintenance burden if Gusto's format ever changes |
| Employee name lookup for pay rate | Repeated VLOOKUP in every formula | Named range for Roster lookup range + IFERROR wrapper | Consistent with Phase 1 pattern; one place to update if Roster columns shift |

---

## Common Pitfalls

### Pitfall 1: Per-Location Overtime Calculation (PAY-04 — Critical)
**What goes wrong:** SUMIFS computes hours per location first. Employee with 22hr at MML + 22hr at MMA = 0 overtime displayed. Rez runs payroll without OT premium. This is a wage theft violation.
**Why it happens:** Building per-location labor tabs (mirroring the per-location calc tab pattern from Phase 1) feels natural but is architecturally wrong for OT purposes.
**How to avoid:** Single Labor-Import tab. Overtime-Tracker SUMIFS uses employee name as the only grouping dimension — not employee + location. Location column is available for display/audit but not used as a SUMIFS criterion in the OT calc.
**Warning signs:** An employee who Rez knows works multiple locations shows zero overtime on the tracker.

### Pitfall 2: Square Labor CSV — Multiple Rows per Shift
**What goes wrong:** Assuming one row per employee per day. Employee with two shifts on Monday has two rows. SUMIFS correctly aggregates both; VLOOKUP or INDEX on a single row would miss the second.
**Why it happens:** Square "Export Shifts" is shift-level, not day-level or week-level.
**How to avoid:** SUMIFS (not VLOOKUP or INDEX) for all hours aggregation. Add a note in Instructions tab: "Square labor export has one row per shift — multiple rows per employee per day is normal."
**Warning signs:** Hours seem low for employees known to work multiple shifts; VLOOKUP only returns first matching row.

### Pitfall 3: Square Labor CSV Column Names (Must Validate)
**What goes wrong:** MATCH("Employee Name", ...) returns #N/A because Square exports "Team Member" or "First Name / Last Name" as separate columns.
**Why it happens:** Square's actual export column names are not publicly documented. Sample data in `sample_data.py` uses placeholder names ("Employee Name", "Total Hours") that may not match Rez's actual export.
**How to avoid:** Build Labor-Import tab with placeholder headers clearly marked. Validate column names with Rez's real export before writing any MATCH formulas. Update `SQUARE_LABOR_HEADERS` in sample_data.py after validation.
**Warning signs:** All labor hours show 0 or #N/A on Overtime-Tracker after Rez's first paste.

### Pitfall 4: Milestone Dates Require Rez's Input Before PAY-06 Works
**What goes wrong:** Days-Until-Milestone column shows errors because Next Milestone Date cells are empty. Conditional formatting fires on blank cells.
**Why it happens:** Exact tier rules and raise dates are TBD — Rez needs to provide them on Monday.
**How to avoid:** Use IFERROR wrapper on the Days-Until formula. Conditional formatting rule should include a check for non-blank: `=AND(H2<>"", J2<=30)`.
**Warning signs:** Every employee row shows as milestone-flagged even without dates entered.

### Pitfall 5: Week Boundaries for Daily Breakdown
**What goes wrong:** Using TODAY() as the week reference means Monday's hours disappear from the "Monday" column by Wednesday (TODAY() has moved forward).
**Why it happens:** TODAY() is dynamic; using it as the weekly reference produces incorrect daily breakdowns.
**How to avoid:** Named cell "WeekStart" (a manually-entered date, same as Phase 1's "WeekEndingDate" pattern). Rez sets it each Monday. Daily column formulas use `WeekStart + 0` (Mon), `WeekStart + 1` (Tue), etc.
**Warning signs:** Mid-week, early-week daily columns drop to zero while Friday column fills correctly.

### Pitfall 6: Pay Rate Lookup Failure (Name Mismatch)
**What goes wrong:** VLOOKUP for pay rate returns #N/A or 0 because "Marcus Johnson" in Square export differs from "Marcus J." in Employee Roster.
**Why it happens:** Phase 1 already anticipated this — Employee Roster has "Square Name" column as the VLOOKUP key. Phase 2 must use the same key.
**How to avoid:** Payroll-Output VLOOKUP uses Column B (Square Name) from Employee Roster, not Column A (Display Name). IFERROR returns "RATE NOT FOUND — check Roster" as visible error text.
**Warning signs:** Estimated Gross Pay column shows 0 or text error for some employees.

---

## Code Examples

Established patterns from Phase 1 that Phase 2 reuses:

### Cross-Location Weekly Hours Aggregate
```python
# Formula string written into Overtime-Tracker via openpyxl:
# WeekStart is a named range cell; LaborHours/LaborEmployee/LaborDate are named ranges

total_hours_formula = (
    "=SUMIFS("
    "LaborHours,"          # Total Hours column from Labor-Import
    "LaborEmployee,A2,"    # Match this employee (name in col A)
    "LaborDate,\">=\"&WeekStart,"
    "LaborDate,\"<=\"&WeekEnd"
    ")"
)
```

### Daily Hours Breakdown (Monday column = B)
```python
monday_formula = (
    "=SUMIFS("
    "LaborHours,"
    "LaborEmployee,A2,"
    "LaborDate,WeekStart"   # WeekStart = Monday; +1 = Tue, etc.
    ")"
)
```

### Overtime and Regular Hours
```python
# Overtime (col J, assuming weekly total in col I):
overtime_formula = "=MAX(I2-40,0)"

# Regular (col K):
regular_formula = "=MIN(I2,40)"
```

### Pay Rate Lookup with Error Handling
```python
# In Payroll-Output, col D (rate lookup from Employee Roster col B/D):
rate_formula = (
    '=IFERROR('
    'VLOOKUP(A2,\'Employee-Roster\'!B:D,3,FALSE),'
    '"RATE NOT FOUND — check Roster"'
    ')'
)
```

### Milestone Days Until (Employee Roster extension, col J)
```python
# H2 = Next Milestone Date (date value)
days_until_formula = "=IFERROR(H2-TODAY(),\"\")"
ws.cell(row=r_idx, column=10).number_format = "0"  # display as integer days
```

### Conditional Formatting — Three-Zone Overtime (openpyxl)
```python
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import PatternFill, Font

# Apply to weekly total column, e.g. "I2:I100"
FILL_RED    = PatternFill(fgColor="FCE8E6", fill_type="solid")
FILL_YELLOW = PatternFill(fgColor="FFF9C4", fill_type="solid")
FILL_GREEN  = PatternFill(fgColor="D9EAD3", fill_type="solid")

# Red rule first (highest priority in openpyxl — first added wins ties)
ws.conditional_formatting.add("I2:I100",
    CellIsRule(operator="greaterThanOrEqual", formula=["38"], fill=FILL_RED))
ws.conditional_formatting.add("I2:I100",
    FormulaRule(formula=["AND(I2>=32,I2<38)"], fill=FILL_YELLOW))
ws.conditional_formatting.add("I2:I100",
    CellIsRule(operator="lessThan", formula=["32"], fill=FILL_GREEN))
```

### Extending tab_defs in build_workbook()
```python
# Phase 2 appends to the existing list — no changes to Phase 1 builders:
tab_defs = [
    # ... existing 14 Phase 1 tabs unchanged ...
    ("Labor-Import",      TAB_IMPORT, lambda ws: build_labor_import(ws)),
    ("Overtime-Tracker",  TAB_AMBER,  lambda ws: build_overtime_tracker(ws)),
    ("Payroll-Output",    TAB_AMBER,  lambda ws: build_payroll_output(ws)),
]
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Per-location OT calculation | Single-table cross-location aggregate then OT | Best practice from FLSA compliance | Legally correct; catches multi-location employees |
| Manual payroll prep spreadsheet | Formula-driven OT tracker with conditional flags | Ongoing shift in restaurant ops tooling | Rez sees OT risk mid-week, not after the fact |
| Fixed Gusto CSV template | Gusto Smart Import flexible column mapping | ~2022-2023 (Gusto feature evolution) | No rigid template to maintain; format tolerant |
| Row-based milestone tracking | Date-keyed formula with TODAY() diff | Standard Sheets pattern | Countdown auto-updates daily; no manual recalculation |

**Deprecated/outdated:**
- Fixed-column Gusto import format: Smart Import replaces this; no need to reverse-engineer Gusto's internal column structure
- Per-location overtime tracking: legally incorrect for multi-location employees; avoid

---

## Open Questions

1. **Exact Square Labor CSV column names**
   - What we know: Square exports include employee name, location, clock-in/out times, regular hours, overtime hours, total hours — but exact header strings are unconfirmed
   - What's unclear: Whether Square exports "Employee Name" or "Team Member" or "First Name"/"Last Name" as separate columns; whether it's one row per shift or one per day
   - Recommendation: Build Labor-Import tab with placeholder headers clearly labeled as PLACEHOLDER. Rez exports one week of real data before any MATCH formula strings are finalized. Validate via screen share or sample file.

2. **Pay period: weekly vs biweekly**
   - What we know: Federal OT is weekly (168-hour workweek); pay frequency is separate from OT calculation period
   - What's unclear: Whether Rez pays weekly or biweekly — affects how many rows Gusto-Output shows and what "pay period" means on the output tab
   - Recommendation: Build for weekly by default (simpler); confirm with Rez Monday. If biweekly, the Overtime-Tracker still calculates OT weekly (required by law), but Payroll-Output would show two weeks of data.

3. **Exact pay tier rules and milestone amounts**
   - What we know: 90-day milestone and certification milestones confirmed by Rez; raise amounts TBD
   - What's unclear: How many tiers exist, what the raise increments are, whether certifications have fixed dates or are event-triggered
   - Recommendation: Build the roster column structure (Next Milestone Date, Milestone Type, Days Until) with empty data. Rez fills in the actual dates and types. Flag in Instructions tab: "Next Milestone Date and Milestone Type must be entered manually per employee."

4. **Whether any current employees actually work across multiple locations**
   - What we know: Architecture must handle this correctly regardless
   - What's unclear: Whether this is a current real scenario for Rez's team or a theoretical edge case
   - Recommendation: Build the cross-location architecture correctly regardless. If no employee currently works multiple locations, the formula still works — it just never shows cross-location hours for anyone.

5. **Gusto's exact column mapping behavior on first import**
   - What we know: Smart Import is described as flexible with auto-mapping; no rigid template required
   - What's unclear: Whether Gusto saves column mappings after first use, and whether "Overtime Hours" must be a separate column or if Gusto computes it from total hours
   - Recommendation: Include both Regular Hours and Overtime Hours as separate explicit columns. Gusto can always ignore a column but cannot infer what isn't there. After Rez's first Gusto import, note which column names Gusto auto-recognized to refine the output tab headers.

---

## Validation Architecture

> nyquist_validation is enabled in config.json — section required.

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Manual formula audit + ISNUMBER validation rows (same as Phase 1 — pure Sheets build, no automated test framework) |
| Config file | None — validation is built into the Sheet (ISNUMBER rows, visible error text cells) |
| Quick run command | Open Overtime-Tracker → paste sample labor data → confirm weekly totals are non-zero and color zones fire correctly |
| Full suite command | Paste Rez's real Square Labor CSV → verify all employees appear with correct cross-location totals → verify Payroll-Output has matching rows → check OT math manually for one employee |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| PAY-01 | Square Labor CSV paste auto-populates daily hours per employee per location | Manual smoke | Paste sample Labor CSV → verify Overtime-Tracker shows non-zero hours for all employees | ❌ Wave 0: build Labor-Import tab with ISNUMBER validation row |
| PAY-02 | Weekly total hours calculated with running daily breakdown | Unit (formula check) | Verify daily column sum equals weekly total column for each employee row | ❌ Wave 0: build Overtime-Tracker with daily + weekly formulas |
| PAY-03 | Overtime tracker color-codes green/yellow/red by threshold | Visual smoke | Set one employee's hours to 33 (should be yellow); set another to 39 (red); set another to 20 (green) | ❌ Wave 0: add FormulaRule conditional formatting to weekly total column |
| PAY-04 | Cross-location aggregate before OT threshold | Integration (critical) | Enter employee "X" with 22hr at MML + 22hr at MMA in Labor-Import → verify Overtime-Tracker shows 44 total, 4 OT hours | ❌ Wave 0: confirm SUMIFS does NOT filter by location in OT aggregate formula |
| PAY-05 | Employee roster shows hire date, rate, tier, next milestone, days-until | Unit (formula check) | Open Employee-Roster → confirm Days Until column shows integer days from today to milestone | ❌ Wave 0: extend Employee-Roster with milestone columns H-K |
| PAY-06 | Pay tier tracker flags employees approaching milestone | Visual smoke | Set one employee milestone to TODAY()+15 → verify amber flag fires; set to TODAY()-1 → verify red overdue fires | ❌ Wave 0: add conditional formatting to Days Until column |
| PAY-07 | Gusto-ready output tab has name, total hrs, OT hrs, pay rate | Manual integration | Open Payroll-Output → verify all employees from Overtime-Tracker appear with correct rate from Roster → verify Estimated Gross Pay math for one employee | ❌ Wave 0: build Payroll-Output tab with VLOOKUP formulas |

### Sampling Rate
- **Per task commit:** Open Overtime-Tracker with sample data → verify no #N/A or 0-for-known-employees errors
- **Per wave merge:** Full sample data paste into Labor-Import → verify all 7 PAY requirements visible in the sheet
- **Phase gate:** Rez pastes real Square Labor CSV → all employee names resolve → OT colors correct → Payroll-Output exported to Gusto and accepted (first real payroll run)

### Wave 0 Gaps
- [ ] `Labor-Import` tab — ISNUMBER validation row covering Total Hours, Employee Name, Date columns (PAY-01)
- [ ] `Labor-Import` tab — placeholder header row clearly marked as "PLACEHOLDER — update with Rez's actual Square export headers"
- [ ] `Overtime-Tracker` tab — daily columns Mon-Sun with SUMIFS formulas (PAY-02)
- [ ] `Overtime-Tracker` tab — Weekly Total, Overtime Hours, Regular Hours formulas (PAY-02, PAY-03, PAY-04)
- [ ] `Overtime-Tracker` tab — WeekStart named cell (manually set each Monday) (PAY-02)
- [ ] `Overtime-Tracker` tab — FormulaRule conditional formatting on Weekly Total column (PAY-03)
- [ ] `Employee-Roster` tab — extend with cols H (Next Milestone Date), I (Milestone Type), J (Days Until), K (Status) (PAY-05)
- [ ] `Employee-Roster` tab — conditional formatting on Days Until column (PAY-06)
- [ ] `Payroll-Output` tab — all columns with VLOOKUP to Roster for pay rate (PAY-07)
- [ ] `sample_data.py` — extend SQUARE_LABOR_SAMPLE_ROWS to include multi-location employee for PAY-04 test
- [ ] `Instructions` tab — update with Square Labor export navigation path (placeholder until column names confirmed)

*(All gaps are Sheets/openpyxl structure — no test framework install required)*

---

## Sources

### Primary (HIGH confidence)
- Phase 1 `01-RESEARCH.md` — MATCH+INDEX, SUMIFS, FormulaRule patterns verified and already implemented in build_weekly_report.py
- Phase 1 `build_weekly_report.py` — openpyxl extension pattern confirmed; tab_defs append pattern works; conditional formatting classes already imported
- Phase 1 `sample_data.py` — `SQUARE_LABOR_HEADERS` placeholder already defined; `EMPLOYEE_ROSTER` structure with hire date and pay tier columns already exists
- [Square Labor API — Timecard objects](https://developer.squareup.com/docs/labor-api/how-it-works) — field names: team_member_id, location_id, start_at, end_at, wage (hourly_rate, job_title)
- [Square Timecard Reporting](https://squareup.com/help/us/en/article/6140-employee-timecard-reporting) — confirmed three export options: "Export shifts", "Labor cost by location", "Labor vs sales"
- [FLSA overtime rules](https://www.dol.gov/agencies/whd/overtime) — federal 40hr/week threshold; Texas has no additional state OT law; cross-location aggregation required by FLSA

### Secondary (MEDIUM confidence)
- [Gusto Smart Import support page](https://support.gusto.com/article/999914471000000/Run-payroll-with-Smart-Import) — confirmed: flexible file formats accepted (.csv, .xlsx), auto column mapping, zeros override/blanks do not, no reformatting required
- Square Community forums — confirmed: "Export Shifts" creates one row per shift (not per day); "Job title" column confirmed present; Regular/Overtime hours fields confirmed in export
- [Square Overtime FAQ](https://squareup.com/help/us/en/article/6570-timecards-faqs) — confirmed Square tracks regular and overtime hours; overtime defined by state rules (Texas = federal only)

### Tertiary (LOW confidence — must validate)
- Exact Square Labor CSV column header strings — not publicly documented; placeholder names in sample_data.py are reasonable guesses based on API field names but MUST be validated against Rez's real export
- Gusto column auto-recognition specifics — "Regular Hours" and "Overtime Hours" are likely recognized but not officially documented as specific required strings

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — openpyxl extension pattern is proven (Phase 1 complete); no new libraries
- Formula architecture: HIGH — SUMIFS cross-location aggregate is a standard, documented formula pattern
- Overtime logic: HIGH — FLSA 40hr/week federal rule is unambiguous; Texas has no state supplement
- Square Labor CSV exact column names: LOW — not publicly documented; must validate with Rez's real export
- Gusto Smart Import flexibility: MEDIUM — confirmed flexible/auto-mapping from official support page; exact recognized column strings not documented

**Research date:** 2026-03-14
**Valid until:** 2026-06-14 (formula patterns stable; Square export format could change without notice — re-validate column names if Square updates their dashboard)
