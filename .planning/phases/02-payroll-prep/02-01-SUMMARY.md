---
phase: 02-payroll-prep
plan: 01
subsystem: payroll-data-foundation
tags: [labor-import, employee-roster, milestone-tracking, square-labor, cross-location-ot]
completed: 2026-03-14

dependency-graph:
  requires: []
  provides:
    - build_labor_import (Labor-Import tab builder, ready for Plan 02-02 to wire into tab_defs)
    - PAYROLL_SAMPLE_EMPLOYEES (unique employee list for Overtime-Tracker and Payroll-Output)
    - EMPLOYEE_ROSTER extended to 11 columns with milestone fields
    - SQUARE_LABOR_SAMPLE_ROWS expanded to 48 rows with cross-location OT test case
  affects:
    - scripts/build_weekly_report.py (build_employee_roster extended in place)
    - scripts/sample_data.py (EMPLOYEE_ROSTER schema change — callers must unpack 11 cols)

tech-stack:
  added: []
  patterns:
    - MATCH-based ISNUMBER/ISTEXT validation in row 3 (same pattern as other import tabs)
    - Excel formula cells (J, K) written as string formulas via openpyxl cell.value
    - FormulaRule conditional formatting with stopIfTrue for milestone priority ordering
    - Cross-location labor data: one employee, multiple location rows, SUMIFS must aggregate

key-files:
  created: []
  modified:
    - scripts/sample_data.py
    - scripts/build_weekly_report.py

decisions:
  - "build_labor_import row layout: row1=PLACEHOLDER notice, row2=headers, row3=validation, row4+=data (freeze at A4, not A3) — one extra row vs other import tabs because notice is row 1, headers are row 2"
  - "EMPLOYEE_ROSTER tuple extended to 11 elements; indices 9 and 10 are None (formula placeholders, not static data)"
  - "ISTEXT validation added for Employee Name and Location columns in Labor-Import validation row — not just ISNUMBER, because text paste errors are equally common for string columns"
  - "Conditional formatting stopIfTrue=True on red/overdue rule so amber rule does not fire for overdue cells"

metrics:
  duration: 4 minutes
  completed: 2026-03-14T20:15:10Z
  tasks: 2
  files_modified: 2
---

# Phase 2 Plan 01: Labor-Import Tab and Employee Roster Milestone Tracking Summary

**One-liner:** Square Labor CSV import tab with MATCH-based validation plus Employee Roster extended with formula-driven milestone flag columns (SOON/OVERDUE/OK).

## Tasks Completed

| Task | Name | Commit | Key Output |
|------|------|--------|------------|
| 1 | Extend sample data with multi-location labor rows and milestone fields | 79f2f04 | 48 labor rows, 11-col roster, PAYROLL_SAMPLE_EMPLOYEES |
| 2 | Build Labor-Import tab and extend Employee-Roster with milestone columns | c68ecc6 | build_labor_import(), extended build_employee_roster() |

## What Was Built

### Task 1 — sample_data.py

**SQUARE_LABOR_SAMPLE_ROWS** expanded from 14 to 48 rows covering the full Mon-Fri sample week (2026-03-09 to 2026-03-13) for all 10 employees across all 5 locations.

Cross-location OT test case (PAY-04): Marcus Johnson works 8 hrs/day Mon-Fri at Moto Medi Lubbock (40 hrs) plus two 3-hr afternoon shifts at Moto Medi Amarillo on Tue and Thu (6 hrs) — total 46 hrs across two locations. Split-shift pattern (two rows for same employee/day) is present on Tue and Thu for Marcus to exercise SUMIFS multi-row aggregation.

**EMPLOYEE_ROSTER** extended from 7 to 11 columns per row. Indices 7 and 8 added for `Next Milestone Date` and `Milestone Type` (static strings). Indices 9 and 10 are `None` — these are formula placeholders written in Excel by `build_employee_roster()`. Milestone test cases:
- Marcus Johnson: `2026-04-01` / `90-Day Review` → SOON (18 days from sample week)
- Jake Hernandez: `2026-03-10` / `Food Handler Cert` → OVERDUE (3 days before end of sample week)
- Ashley Torres, Devon Scott, Jasmine Lee: empty milestone dates → IFERROR returns `""` (blank status)

**PAYROLL_SAMPLE_EMPLOYEES** added: 10 unique employee names in first-appearance order for Plan 02-02 consumers.

### Task 2 — build_weekly_report.py

**`build_labor_import(ws)`** creates a Labor-Import tab following the same import tab pattern used by Square/DoorDash/UberEats/Grubhub/BEK:
- Row 1: merged PLACEHOLDER notice with A1 cell comment explaining update requirement
- Row 2: column headers from SQUARE_LABOR_HEADERS; B2 comment flags Employee Name as the SUMIFS key
- Row 3: validation row — ISNUMBER formulas for hours columns, ISTEXT formulas for Employee Name/Location, type labels for date/time columns. All validation uses MATCH-based references (not hardcoded column letters)
- Rows 4+: 48 sample data rows from SQUARE_LABOR_SAMPLE_ROWS
- Freeze pane at A4; "Last Updated" marker cell below data
- Conditional formatting on row 3: cells returning "OK" turn green

**`build_employee_roster(ws)` extended in place** (no new function):
- Header list extended from 7 to 11 columns (A-K)
- H (col 8): Next Milestone Date — static from EMPLOYEE_ROSTER index 7, formatted YYYY-MM-DD
- I (col 9): Milestone Type — static from EMPLOYEE_ROSTER index 8
- J (col 10): formula `=IFERROR(H{row}-TODAY(),"")` — integer days until milestone; blank when no date set
- K (col 11): formula `=IF(J{row}="","",IF(J{row}<=0,"OVERDUE",IF(J{row}<=30,"SOON","OK")))`
- Conditional formatting on J2:J100: red (FILL_CF_RED + bold) for `AND(J<>"",J<=0)`, amber (FILL_CF_AMBER + bold) for `AND(J>0,J<=30)`
- Note row merge extended from A:G (7 cols) to A:K (11 cols)

**`FILL_CF_AMBER`** constant added: `PatternFill(start_color="FFE0B2", ...)`.

**Import** updated to include `PAYROLL_SAMPLE_EMPLOYEES` from sample_data.

Neither `build_labor_import` nor any related changes are wired into `tab_defs` yet — that is deferred to Plan 02-02 per the plan spec.

## Deviations from Plan

None - plan executed exactly as written.

## Verification Results

```
1. Constants importable: OK
2. Functions exist: OK
3. Labor-Import: ISNUMBER validation OK, 53 rows (48 data + overhead)
4. Employee-Roster: 11 cols, J formula: =IFERROR(H2-TODAY(),""), K formula: =IF(J2="","",...)
5. Marcus cross-location: 46.0hrs at {'Moto Medi Amarillo', 'Moto Medi Lubbock'}

All plan verification criteria: PASSED
```

Full workbook build (`python3 scripts/build_weekly_report.py`) also passes — all 14 existing tabs build correctly with no regressions.

## Self-Check: PASSED

- `/Users/josi/crash-course-intake/scripts/sample_data.py` — FOUND (modified)
- `/Users/josi/crash-course-intake/scripts/build_weekly_report.py` — FOUND (modified)
- Commit `79f2f04` (Task 1) — FOUND
- Commit `c68ecc6` (Task 2) — FOUND
