---
phase: 01-weekly-reporting
plan: 01
subsystem: reporting-workbook
tags: [openpyxl, excel, weekly-report, scaffold, import-tabs, validation]
requires: []
provides: [Rez-Weekly-Report.xlsx, scripts/build_weekly_report.py, scripts/sample_data.py]
affects: [01-02-PLAN.md]
tech-stack:
  added: [openpyxl 3.1.5]
  patterns: [MATCH-based column lookup, ISNUMBER validation row, date-keyed Prior-Week snapshot]
key-files:
  created:
    - scripts/build_weekly_report.py
    - scripts/sample_data.py
    - Rez-Weekly-Report.xlsx
  modified: []
decisions:
  - "Placeholder headers in all import tabs with ISNUMBER validation on numeric columns — survives CSV re-paste without formula changes"
  - "Prior-Week tab uses 26-column date-keyed structure (date + 5 KPIs x 5 locations) for WoW comparison; row-offset pattern explicitly avoided"
  - "Employee-Roster Square Name column is the VLOOKUP key — separate from display name to handle nickname mismatches (per RESEARCH.md Pitfall 7)"
  - "Tab colors distinguish tab groups: import=blue, calc=gray, summary/prior=amber, reference=green"
  - "Summary and Location Calc tabs have structure-only (no formulas) — deferred to Plan 02 pending Rez's real CSV export column names"
metrics:
  duration: 5 minutes
  completed: 2026-03-14
  tasks_completed: 1
  tasks_total: 1
  files_created: 3
  files_modified: 0
---

# Phase 1 Plan 1: Weekly Report Workbook Scaffold Summary

**One-liner:** openpyxl script generating 14-tab Excel workbook with MATCH-based import tab layouts, ISNUMBER validation rows, placeholder column headers, and sample data across 5 locations for 5 platforms.

## What Was Built

### scripts/sample_data.py (266 lines)
Module containing all reference data for the workbook:
- Placeholder column headers for each platform (Square, DoorDash, UberEats, Grubhub, BEK, Square Labor)
- Location and brand dictionaries: 5 locations mapped to 2 brands (Moto Medi, Tikka Shack)
- 25 sample rows per import platform covering week of 2026-03-09 to 2026-03-15 across all 5 locations
- 10 sample employees with Square Name / Display Name separation for VLOOKUP accuracy
- Prior-Week snapshot row (week ending 2026-03-09) with realistic KPIs per location
- 15 sample BEK invoice rows including both Food and Supplies categories (to test category filter)

### scripts/build_weekly_report.py (695 lines)
Main openpyxl script that produces `Rez-Weekly-Report.xlsx`. Builds:

**Import tabs** (Square, DoorDash, UberEats, Grubhub, BEK):
- Row 1: Placeholder notice (yellow background warning to update headers)
- Row 2: Bold column headers with steel blue background
- Row 3: ISNUMBER validation row using MATCH-based formula: `=IF(ISNUMBER(INDEX(Tab!A:Z,4,MATCH("Column",Tab!2:2,0))),"OK","PASTE ERROR...")`
- Row 4+: Sample data rows with alternating row colors
- Last Updated date cell with comment prompt

**Reference tabs** (Instructions, Employee-Roster):
- Instructions: Step-by-step export paths for all 5 platforms, Grubhub lag warning, troubleshooting guide, placeholder header notice
- Employee-Roster: Square Name as VLOOKUP key, data validation dropdown for location, currency/date formatting on rate/hire date columns

**Prior-Week tab** (amber): 26-column date-keyed structure (Week Ending + 5 KPIs x 5 locations). Sample row for 2026-03-09 populated with realistic values.

**Location Calc tabs** (MML, MMA, MM3, TS1, TS2) — structure only:
- Merged title row with location full name
- Week Ending date cell
- Section headers: Revenue Breakdown, Cost Metrics, Labor, Volume
- Metric label rows with currency/percentage number formats applied
- Formulas deferred to Plan 02

**Summary tab** (amber) — structure only:
- 18pt title, Week Ending cell
- Location columns with brand color bands (Moto Medi = orange FDE9D9, Tikka Shack = teal D0E2F1)
- KPI row labels with WoW indented rows
- Frozen at B5 for mobile scrolling; print area set
- Formulas deferred to Plan 02

## Verification Results

Plan's automated verification passed:
```
ALL CHECKS PASSED
```
- All 14 tabs present in correct order
- Each import tab has header row (row 2) and content in validation row (row 3)
- Employee-Roster has sample data (10 employees)
- Prior-Week has header row

Additional sanity checks:
- All tab colors match spec (import=4A86C8, calc=999999, amber=F4A442, green=6AA84F)
- Instructions A1: "Rez Weekly Report — Instructions"
- Employee count: 10 with Square Name column populated
- Prior-Week: 26 columns (Week Ending + 5 KPIs x 5 locations)
- Location Calc: title and Revenue Breakdown section confirmed
- Summary: title, brand color column headers confirmed

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] FormulaRule API incompatibility with openpyxl 3.1.5**
- **Found during:** Task 1 — first run
- **Issue:** Plan specified using `DifferentialStyle` with `dxf=` argument to `FormulaRule`, but openpyxl 3.1.5 `FormulaRule` takes `fill=` and `font=` directly, not a `dxf` argument
- **Fix:** Removed `DifferentialStyle` import, changed `FormulaRule(dxf=...)` to `FormulaRule(fill=ok_fill, font=ok_font)` — same visual result
- **Files modified:** scripts/build_weekly_report.py
- **Commit:** 8fcbec9

**2. [Rule 1 - Bug] DataValidation sqref API mismatch**
- **Found during:** Task 1 — second run
- **Issue:** `loc_dv.sqref.append()` not available; `MultiCellRange` object has no `append` method in this openpyxl version
- **Fix:** Changed to `loc_dv.add(ws.cell(row=r_idx, column=3))` — the correct API call
- **Files modified:** scripts/build_weekly_report.py
- **Commit:** 8fcbec9

## Self-Check: PASSED

Files created:
- FOUND: /Users/josi/crash-course-intake/scripts/build_weekly_report.py (695 lines, min 200 required)
- FOUND: /Users/josi/crash-course-intake/scripts/sample_data.py (266 lines, min 50 required)
- FOUND: /Users/josi/crash-course-intake/Rez-Weekly-Report.xlsx

Commits:
- FOUND: 8fcbec9 — feat(01-01): generate Rez Weekly Report workbook scaffold

Verification: ALL CHECKS PASSED (automated plan verification script)

## Key Decisions Made

1. **ISNUMBER validation uses MATCH-based formula** — validation row references column by name via `MATCH("Column Name", Tab!2:2, 0)` not hardcoded column letter, so it still works after CSV column reorder
2. **Placeholder headers prominently marked** — Row 1 of every import tab has a yellow-background notice about placeholder status; repeated in Instructions tab with bold warning
3. **Square Name as separate column** — Following RESEARCH.md Pitfall 7; allows nickname mismatches between Square clock-in names and display names
4. **Location Calc and Summary tabs: structure-only** — Explicitly deferred formula writing until Rez provides real CSV exports; wrong MATCH("Column") strings silently return 0 revenue

## Next Steps for Plan 02

Plan 02 should:
1. Get Rez's actual CSV exports from each platform to validate column names
2. Update `MATCH("Column Name")` strings in `sample_data.py` header lists to match real names
3. Write SUMIFS formulas on Location Calc tabs (revenue, purchase cost %, labor cost %)
4. Write WoW formulas on Summary tab referencing Prior-Week tab via date-keyed MATCH
5. Add conditional formatting for >5% variance flags (red/green) on Summary WoW rows
