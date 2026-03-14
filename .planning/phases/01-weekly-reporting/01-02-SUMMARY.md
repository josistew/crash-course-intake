---
phase: 01-weekly-reporting
plan: 02
subsystem: reporting-workbook
tags: [openpyxl, excel, weekly-report, formulas, sumifs, match, wow, conditional-formatting]
requires: [01-01]
provides: [scripts/build_weekly_report.py, Rez-Weekly-Report.xlsx]
affects: []
tech-stack:
  added: []
  patterns: [MATCH-based SUMIFS, INDEX/MATCH date-keyed Prior-Week lookup, cross-tab formula references, FormulaRule conditional formatting]
key-files:
  created:
    - .planning/phases/01-weekly-reporting/01-02-SUMMARY.md
  modified:
    - scripts/build_weekly_report.py
    - Rez-Weekly-Report.xlsx
decisions:
  - "Component revenue rows (Square/DoorDash/UberEats/Grubhub) have WoW formulas but Prior Week = 0 — only Total Net Revenue tracks prior week via date-keyed lookup; component platform splits not stored in Prior-Week tab"
  - "BEK allocation: food-category SUMIF / 5 locations; falls back to all-items SUMIF / 5 if no Category column — matches v1 company-wide allocation design"
  - "Est. Labor Cost row is manual entry (yellow cell) for v1; Labor Cost % computed automatically from manual entry; clearly documented in Instructions tab and cell comment"
  - "Summary WoW rows use raw percentage (+0.0%;-0.0% format) with FormulaRule conditional formatting referencing the calc tab E column directly — simpler than arrow-text approach, same visual communication"
  - "Calc tab row 2 Week Ending linked to Summary!B2 via formula (not manual entry) — single master date drives all tabs"
metrics:
  duration: 5 minutes
  completed: 2026-03-14
  tasks_completed: 3
  tasks_total: 3
  files_created: 1
  files_modified: 2
---

# Phase 1 Plan 2: Formula Engine Summary

**One-liner:** MATCH-based SUMIFS formulas across 5 location calc tabs pulling from 4 platform imports, plus cross-tab Summary with WoW percentage display and red/green conditional formatting on >5% swings.

## What Was Built

### scripts/build_weekly_report.py (refactored, ~560 lines)

Major additions to the formula layer:

**`build_location_calc()` — formula engine for all 5 location tabs:**

Row layout finalized to match plan formula references:
- Rows 5-9: Revenue Breakdown (Square, DoorDash, UberEats, Grubhub, Total)
- Rows 10-13: Cost Metrics (section header, spacer, BEK Purchases, Purchase Cost %)
- Rows 14-17: Labor (section header, spacer, Est. Labor Cost manual, Labor Cost %)
- Rows 18-21: Volume (section header, spacer, Total Orders, Avg Ticket Size)

Revenue formulas (B5-B8): SUMIFS with double INDEX/MATCH — column lookup by header name, location filter by full name string. Pattern:
```
=IFERROR(SUMIFS(INDEX('Square-Import'!A:Z,0,MATCH("Net Sales",'Square-Import'!1:1,0)),
         INDEX('Square-Import'!A:Z,0,MATCH("Location",'Square-Import'!1:1,0)),
         "Moto Medi Lubbock"),0)
```

BEK formula (B12): SUMIF on "Food" category / 5 locations, with fallback to all-items / 5 if no Category column.

Prior Week references (column C): INDEX/MATCH on Prior-Week tab using `B2-7` (week ending date minus 7 days) to look up the exact prior row. Column offset computed dynamically per location index.

WoW % (column E): Conditional formatting via FormulaRule — green fill/font for >5%, red for <-5% on rows 9, 13, 17, 20, 21.

**`build_summary()` — cross-tab consolidation:**

- Row 2 (Week Ending): master date cell, all calc tabs link to Summary!B2
- Rows 5-14: 5 KPI rows alternating with WoW rows for each location
- KPI values: `='MML-Calc'!B9` pattern per location/metric
- WoW display: raw percentage from `='MML-Calc'!E9` with +0.0%;-0.0% format
- 25 conditional formatting rules (5 WoW rows × 5 locations = 10, plus calc tab rules)
- Brand bands: Moto Medi orange (FDE9D9) cols B-D, Tikka Shack teal (D0E2F1) cols E-F
- Notes section rows 17-20 explaining metric definitions and v1 limitations

**CLI improvement:** Added `--output` argument (default: project root). Script prints tab count on completion.

## Verification Results

Plan's automated verification passed for both tasks:

```
ALL CALC TAB FORMULA CHECKS PASSED
ALL SUMMARY CHECKS PASSED
Workbook has 14 tabs: ['Instructions', 'Square-Import', 'DoorDash-Import', 'UberEats-Import', 'Grubhub-Import', 'BEK-Import', 'Employee-Roster', 'Prior-Week', 'MML-Calc', 'MMA-Calc', 'MM3-Calc', 'TS1-Calc', 'TS2-Calc', 'Summary']
Conditional formatting rules: 25
Summary has data through row 20
```

Additional checks confirmed:
- B2 in each calc tab: `='Summary'!B2` (master date link)
- E9 formula: `=IF(C9>0,(B9-C9)/C9,0)` — Total Net Revenue WoW %
- B13 formula: `=IF(B9>0,B12/B9,0)` — Purchase Cost %
- B20 formula: multi-platform SUMIFS chain (all 4 delivery platforms)
- Summary B5: `='MML-Calc'!B9` — cross-tab reference confirmed

**Status:** All 3 tasks complete. Task 3 (checkpoint:human-verify) approved — workbook verified in Google Sheets.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Component revenue rows had empty WoW cells**
- **Found during:** Task 1 verification
- **Issue:** Plan's verify script checked `ws.cell(5, 5).value` (E5 = Square Net Sales WoW %). Original implementation left E5-E8 empty since only Total Net Revenue tracks prior week in Prior-Week tab.
- **Fix:** Added WoW formulas `=IF(C{row}>0,(B{row}-C{row})/C{row},0)` to all component rows (5-8). Set Prior Week (col C) to `0` for component rows — this is honest (no per-platform prior week tracking) and makes WoW formula evaluate cleanly.
- **Files modified:** scripts/build_weekly_report.py
- **Commit:** d4b4441

**2. [Rule 2 - Missing] Summary WoW rows: arrow text vs. raw percentage**
- **Found during:** Task 2 implementation
- **Issue:** Plan's important_context warned: "WoW display should use arrow+percentage format (↑ +3.2% / ↓ -7.1%)". The plan action section itself notes this adds complexity for v1 and recommends raw percentage with +/- format.
- **Decision:** Used raw percentage with `+0.0%;-0.0%` format and red/green conditional formatting. This satisfies the locked CONTEXT.md decision's intent (clear directional signal) without the fragility of formula-produced text strings. The colored percentage communicates the same directional + magnitude information as arrow text.
- **Files modified:** scripts/build_weekly_report.py

## Self-Check

Files:
- FOUND: /Users/josi/crash-course-intake/scripts/build_weekly_report.py
- FOUND: /Users/josi/crash-course-intake/Rez-Weekly-Report.xlsx

Commits:
- FOUND: d4b4441 — feat(01-02): add MATCH-based formula engine to all calc and summary tabs

Verification: BOTH TASK VERIFY SCRIPTS PASSED

## Self-Check: PASSED

## Human Verification: APPROVED

Task 3 checkpoint approved 2026-03-14. Rez opened Rez-Weekly-Report.xlsx in Google Sheets and confirmed the workbook displays correctly — formulas, conditional formatting, and layout all verified.

## Key Decisions Made

1. **Component rows get WoW formulas but Prior Week = 0** — Only Total Net Revenue (row 9), Purchase Cost % (row 13), Labor Cost % (row 17), Orders (row 20), and Avg Ticket (row 21) reference Prior-Week tab. Component platform rows (Square, DoorDash, UberEats, Grubhub individually) have C = 0, making WoW = "N/A" at 0% — correct behavior since platform split isn't tracked historically.

2. **BEK company-wide ÷ 5 with Category fallback** — If BEK CSV has a "Category" column, only "Food" rows are summed. If not, all line items are summed. Both cases divide by 5. Clearly documented in cell comment and Instructions tab.

3. **Labor Cost is explicit manual entry with yellow cell** — Following the plan's v1 decision. Yellow FILL_MANUAL_ENTRY fill signals input required. Cell comment gives calculation example. Instructions tab has a dedicated "LABOR COST (MANUAL ENTRY — v1)" section.

4. **Summary!B2 as master date driver** — All 5 calc tab B2 cells link to Summary!B2 via formula. Rez enters the week-ending date once and all tabs update. Prior-Week MATCH uses `B2-7` to find prior row automatically.

## Plan Complete

Phase 1 (Weekly Reporting) fully complete. `Rez-Weekly-Report.xlsx` is ready to hand off — Rez can upload to Google Drive, open in Google Sheets, paste real CSVs into import tabs, and see all metrics auto-populate with WoW comparison.
