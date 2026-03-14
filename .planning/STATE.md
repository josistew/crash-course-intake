# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-14)

**Core value:** Eliminate hours of manual weekly reporting across 5 locations by consolidating Square, delivery platforms, and BEK Entree data into a single automated view.
**Current focus:** Phase 1 — Weekly Reporting

## Current Position

Phase: 2 of 3 (Payroll Prep)
Plan: 1 of 2 in current phase (02-01 complete, 02-02 next)
Status: Phase 2 in progress — Plan 02-01 executed and verified
Last activity: 2026-03-14 — Plan 02-01 complete: Labor-Import tab built, Employee Roster extended with milestone columns H-K

Progress: [█████░░░░░] 50%

## Performance Metrics

**Velocity:**
- Total plans completed: 2
- Average duration: 5 minutes
- Total execution time: 0.2 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1. Weekly Reporting | 2 | 10 min | 5 min |
| 2. Payroll Prep | 1 | 4 min | 4 min |

**Recent Trend:**
- Last 5 plans: 01-01 (5 min), 01-02 (5 min), 02-01 (4 min)
- Trend: Stable

*Updated after each plan completion*

## Accumulated Context

### Decisions

Decisions logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- [Init]: CSV paste-in over API integration for v1 — fastest to ship, no auth setup from Rez
- [Init]: Google Sheets for reporting/payroll — Rez already lives in Google Workspace
- [Init]: Next.js + Vercel for checklist — proven LeaseJenny pattern, free hosting
- [Init]: Google Sheets as checklist data store — keeps everything in Google ecosystem
- [01-01]: Placeholder headers in import tabs with ISNUMBER validation on MATCH-based formula — survives CSV column reorder
- [01-01]: Prior-Week tab uses 26-column date-keyed structure; row-offset WoW explicitly avoided
- [01-01]: Employee-Roster Square Name column is the VLOOKUP key to handle nickname mismatches
- [01-01]: Location Calc and Summary tabs structure-only — formulas deferred to Plan 02 pending real CSV exports from Rez
- [01-02]: Component revenue rows (Square/DoorDash/UberEats/Grubhub) have WoW formulas but Prior Week = 0 — only Total Net Revenue/KPIs tracked in Prior-Week tab
- [01-02]: BEK allocation = food-category SUMIF / 5 locations; falls back to all-items / 5 if no Category column
- [01-02]: Est. Labor Cost is manual entry (yellow cell) for v1; Labor Cost % computed automatically; Phase 2 (PAY-01) automates
- [01-02]: Summary WoW rows use raw +/- percentage with FormulaRule conditional formatting (not arrow-text strings)
- [02-01]: build_labor_import freeze at A4 (not A3) — notice row pushes headers to row 2, data starts row 4
- [02-01]: EMPLOYEE_ROSTER tuple extended to 11 elements; indices 9-10 are None (formula placeholders in Excel)
- [02-01]: ISTEXT validation added for Employee Name/Location in Labor-Import row 3 — text paste errors as important as numeric ones
- [02-01]: Conditional formatting stopIfTrue=True on red/overdue rule to prevent amber rule also firing for overdue cells

### Pending Todos

None yet.

### Blockers/Concerns

- [Phase 1]: Must validate actual CSV column names from DoorDash, UberEats, Grubhub, and Square with Rez's real exports before writing any formulas — do NOT assume column names
- [Phase 1]: Confirm BEK Entree CSV has food/non-food category column (affects food purchases % calculation)
- [Phase 2]: Download Gusto Smart Import sample template before designing Payroll-Output tab structure
- [Phase 2]: Confirm whether any employees work across multiple locations (determines overtime architecture urgency)
- [Phase 3]: Confirm expected concurrent tablet usage volume before committing to direct Sheets writes vs. Vercel KV write buffer

## Session Continuity

Last session: 2026-03-14
Stopped at: Completed 02-01-PLAN.md both tasks. Phase 2 Plan 1 (data foundation) fully complete. Next: Plan 02-02 — Overtime-Tracker formula engine, Payroll-Output Gusto tab, wire 17-tab workbook.
Resume file: None
