---
phase: 02-payroll-prep
plan: 02
subsystem: payroll-formula-engine
tags: [overtime-tracker, payroll-output, cross-location-ot, sumifs, vlookup, conditional-formatting]
completed: 2026-03-14

dependency-graph:
  requires:
    - 02-01 (build_labor_import, PAYROLL_SAMPLE_EMPLOYEES, EMPLOYEE_ROSTER 11-col)
  provides:
    - build_overtime_tracker (Overtime-Tracker tab builder — cross-location SUMIFS aggregation)
    - build_payroll_output (Payroll-Output tab builder — Gusto-ready gross pay output)
    - 17-tab workbook with all Phase 1 + Phase 2 tabs
  affects:
    - scripts/build_weekly_report.py (two new builders + tab_defs update + instructions update)
    - Rez-Weekly-Report.xlsx (regenerated with 17 tabs)

tech-stack:
  added: []
  patterns:
    - MATCH-based SUMIFS for cross-location OT aggregation (not hardcoded column letters)
    - No Location filter in daily SUMIFS — PAY-04 compliance (aggregate across ALL locations)
    - CellIsRule for simple >= and < thresholds on Weekly Total column
    - FormulaRule for compound AND conditions (WARN zone) and status text matching
    - VLOOKUP on Employee-Roster col B (Square Name) not col A (Display Name)
    - IFERROR wrapping around gross pay calc to handle RATE NOT FOUND text gracefully

key-files:
  created: []
  modified:
    - scripts/build_weekly_report.py
    - Rez-Weekly-Report.xlsx

decisions:
  - "SUMIFS formulas use INDEX/MATCH for column resolution on Labor-Import — survives real Square Labor CSV column reorder at paste time"
  - "Labor-Import MATCH targets row 2 (not row 1) because row 1 is the PLACEHOLDER notice — headers live in row 2"
  - "B$1 as WeekStart anchor uses row-absolute reference (not $B$1) so formula can be copied across rows while staying in row 1"
  - "VLOOKUP range Employee-Roster!B:D uses 3rd column (col D = Hourly Rate) via the Square Name key in col B — not display name in col A"

metrics:
  duration: 7 minutes
  completed: 2026-03-14T20:30:00Z
  tasks: 1 of 2 (checkpoint:human-verify at Task 2)
  files_modified: 2
---

# Phase 2 Plan 02: Overtime-Tracker and Payroll-Output Summary

**One-liner:** Cross-location overtime aggregation engine with MATCH-based SUMIFS (no Location filter, PAY-04 compliant) and Gusto-ready Payroll-Output with VLOOKUP pay rate lookup — 17-tab workbook complete.

## Tasks Completed

| Task | Name | Commit | Key Output |
|------|------|--------|------------|
| 1 | Build Overtime-Tracker and Payroll-Output tabs, wire into workbook | 48b8e1e | build_overtime_tracker(), build_payroll_output(), 17-tab tab_defs |

## What Was Built

### Task 1 — build_weekly_report.py

**`build_overtime_tracker(ws)`** creates the Overtime-Tracker tab:

- Row 1: "Week Starting:" label + B1 manual entry cell (FILL_MANUAL_ENTRY, pre-populated with 2026-03-09 for sample data)
- Row 2: blank spacer
- Row 3: 12 column headers — Employee Name, Mon-Sun, Weekly Total, Overtime Hrs, Regular Hrs, Status (styled with FILL_CALC_HDR + FONT_HEADER)
- Rows 4+: 10 employees from PAYROLL_SAMPLE_EMPLOYEES

**SUMIFS formula pattern (MATCH-based, PAY-04 compliant):**
```
=SUMIFS(
  INDEX('Labor-Import'!A:Z,0,MATCH("Total Hours",'Labor-Import'!2:2,0)),
  INDEX('Labor-Import'!A:Z,0,MATCH("Employee Name",'Labor-Import'!2:2,0)),
  A{row},
  INDEX('Labor-Import'!A:Z,0,MATCH("Date",'Labor-Import'!2:2,0)),
  B$1+{day_offset}
)
```

No Location criterion — aggregates ALL shifts for each employee across ALL locations on each date. Marcus Johnson's 46-hour week (40 hrs MML + 6 hrs MMA) triggers correctly.

**Derived formulas per row:**
- Col I: `=SUM(B{row}:H{row})` — Weekly Total
- Col J: `=MAX(I{row}-40,0)` — Overtime Hrs
- Col K: `=MIN(I{row},40)` — Regular Hrs
- Col L: `=IF(I{row}>=38,"HIGH",IF(I{row}>=32,"WARN","OK"))` — Status

**Conditional formatting:**
- I4:I100 (Weekly Total): CellIsRule >=38 → red, FormulaRule AND(>=32,<38) → amber, CellIsRule <32 → green
- L4:L100 (Status): FormulaRule "HIGH" → red, "WARN" → amber, "OK" → green

Freeze at A4. Column widths: A=20, B-H=8, I-K=12, L=10.

**`build_payroll_output(ws)`** creates the Payroll-Output tab:

- Row 1: "Pay Period Ending:" label + B1 manual entry cell (pre-populated 2026-03-15)
- Row 3: 6 headers — Employee Name, Regular Hours, Overtime Hours, Current Pay Rate, Estimated Gross Pay, Pay Period
- Disclaimer comment on E3 (Estimated Gross Pay header cell)
- Rows 4+: 10 employee rows referencing Overtime-Tracker directly

**Column formulas:**
- Col A: `='Overtime-Tracker'!A{row}` (employee name pass-through)
- Col B: `='Overtime-Tracker'!K{row}` (Regular Hrs)
- Col C: `='Overtime-Tracker'!J{row}` (Overtime Hrs)
- Col D: `=IFERROR(VLOOKUP(A{row},'Employee-Roster'!B:D,3,FALSE),"RATE NOT FOUND")`
- Col E: `=IFERROR((B{row}*D{row})+(C{row}*D{row}*1.5),"")` (handles RATE NOT FOUND gracefully)
- Col F: `=$B$1` (pay period ending date)

Currency format on D4:D100 and E4:E100. Date format on F4:F100. Freeze at A4.

**`build_instructions(ws)` updated** — new "PAYROLL PREP (Phase 2)" section added at end of content list with 5 numbered steps and a PLACEHOLDER note for Labor-Import headers.

**`tab_defs` in `build_workbook()` updated** — 3 new entries appended after Summary (index 14 = Labor-Import, 15 = Overtime-Tracker, 16 = Payroll-Output). Total: 17 tabs.

## Checkpoint Status

Stopped at Task 2 (checkpoint:human-verify). Task 1 is fully committed. The workbook is ready for visual verification in Google Sheets or Excel.

## Verification Results

```
python3 scripts/build_weekly_report.py → 17 tabs, all build without errors
All 17 tabs present in correct order.

Automated checks:
- 17 tabs confirmed
- Labor-Import at index 14
- Overtime-Tracker A3 header = "Employee Name"
- Weekly Total (I4) has SUM formula
- Overtime Hrs (J4) has MAX formula
- Payroll-Output D4 has VLOOKUP
- Monday SUMIFS has NO Location filter (PAY-04 confirmed)
- SUMIFS present in Monday formula

OK: 17 tabs, formulas correct, no Location filter in OT aggregation
```

## Deviations from Plan

### Auto-applied improvements

**1. [Rule 1 - Pattern] MATCH-based SUMIFS instead of hardcoded column letters**
- **Found during:** Task 1 (pre-empted by important_context warning)
- **Issue:** Plan template used hardcoded `'Labor-Import'!H:H` references. Labor-Import uses row 2 for headers (row 1 is PLACEHOLDER notice), and real exports may have different column order.
- **Fix:** All three SUMIFS criteria use `INDEX('Labor-Import'!A:Z,0,MATCH("column_name",'Labor-Import'!2:2,0))` pattern. MATCH targets row 2 (not row 1) matching the Labor-Import layout.
- **Files modified:** scripts/build_weekly_report.py
- **Commit:** 48b8e1e

## Self-Check: PASSED

- `/Users/josi/crash-course-intake/scripts/build_weekly_report.py` — FOUND (modified)
- `/Users/josi/crash-course-intake/Rez-Weekly-Report.xlsx` — FOUND (regenerated)
- Commit `48b8e1e` (Task 1) — FOUND
