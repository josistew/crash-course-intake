# Roadmap: Rez Operations Suite

## Overview

Three systems that replace Rez's manual number-pulling workflow: a formula-driven Google Sheets reporting engine that consolidates Square, delivery platform, and BEK Entree CSV exports into a single weekly view; a payroll prep layer within that same Sheet that handles hours, overtime, pay tiers, and Gusto output; and a tablet-friendly Next.js checklist app that captures daily shift completion data into Google Sheets. Built in natural dependency order — reporting first (highest ROI, most dangerous pitfalls), payroll second (shares Square import infrastructure), checklist third (fully independent, the only phase requiring code).

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Weekly Reporting** - Operators paste CSVs into import tabs and get a consolidated, formula-driven weekly report across all 5 locations
- [ ] **Phase 2: Payroll Prep** - Operators paste Square labor CSV and get overtime tracking, pay tier milestones, and a Gusto-ready output tab
- [ ] **Phase 3: Daily Checklist App** - Staff complete shift checklists on a shared tablet; managers see completion status across all locations

## Phase Details

### Phase 1: Weekly Reporting
**Goal**: Operators can paste CSV exports from all platforms and get an accurate, consolidated weekly view of revenue, food cost, labor cost, and order volume across all 5 locations — with week-over-week variance flags.
**Depends on**: Nothing (first phase)
**Requirements**: RPT-01, RPT-02, RPT-03, RPT-04, RPT-05, RPT-06, RPT-07, RPT-08, RPT-09, RPT-10
**Success Criteria** (what must be TRUE):
  1. Operator can paste Square, DoorDash, UberEats, Grubhub, and BEK Entree CSVs into named import tabs and all metrics auto-populate without manual formula editing
  2. Each location tab shows net revenue, food purchases %, labor cost %, order volume by platform, and avg ticket — all drawn from pasted data, not hardcoded
  3. The consolidated summary tab shows all 5 locations side-by-side with Moto Medi and Tikka Shack grouped separately
  4. Week-over-week comparison highlights any metric that moved more than 5% in red (decline) or green (gain) — correct even when prior week had different column ordering in the paste
  5. Formulas survive CSV column reordering from any platform (MATCH-based, not fixed column index)
**Plans**: 2 plans

Plans:
- [ ] 01-01-PLAN.md — Workbook scaffold: 14 tabs, import tab layouts with placeholder headers and validation rows, Instructions tab, Employee Roster, sample data
- [ ] 01-02-PLAN.md — Formula engine: MATCH-based SUMIFS on calc tabs, Summary tab with cross-tab KPIs and WoW variance formatting

### Phase 2: Payroll Prep
**Goal**: Operators can paste Square labor CSV and immediately see daily/weekly hours per employee, overtime flags, pay tier milestones, and a Gusto-ready output tab — all cross-location before overtime threshold is applied.
**Depends on**: Phase 1
**Requirements**: PAY-01, PAY-02, PAY-03, PAY-04, PAY-05, PAY-06, PAY-07
**Success Criteria** (what must be TRUE):
  1. Operator pastes one Square labor CSV and sees daily hours breakdown plus weekly total per employee across all locations combined (not per-location)
  2. Overtime tracker color-codes every employee: green under 32 hrs, yellow 32-38 hrs, red 38+ hrs — with cross-location aggregation applied before threshold
  3. Employee roster shows hire date, current pay rate, pay tier, next milestone date, and days until milestone — auto-flagging anyone approaching a raise
  4. Gusto-ready output tab contains employee name, total hours, overtime hours, and current pay rate in Gusto's exact import column format
**Plans**: TBD

Plans:
- [ ] 02-01: TBD

### Phase 3: Daily Checklist App
**Goal**: Staff at any location can complete a shift checklist on a shared tablet without logging in; managers can see today's completion status across all locations from a single dashboard view.
**Depends on**: Phase 2
**Requirements**: CHK-01, CHK-02, CHK-03, CHK-04, CHK-05, CHK-06, CHK-07, CHK-08, CHK-09
**Success Criteria** (what must be TRUE):
  1. Staff can tap their location and shift (Opening/Closing), enter their name, and see the correct categorized checklist in under 10 seconds — no login required
  2. Staff can tap any item to mark it complete with an automatic timestamp; they can add a note to any item before or after completing it
  3. Every completion writes to Google Sheets (staff name, location, shift, item, timestamp) — verified by checking the Completions-Log tab directly
  4. Manager dashboard shows today's checklist status across all locations — which shifts are complete, in progress, or not started — with no data entry required from managers
  5. App is deployed to Vercel, accessible via URL on store tablet bookmark, renders correctly on tablet screen without pinch-zoom
**Plans**: TBD

Plans:
- [ ] 03-01: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Weekly Reporting | 0/2 | Planning complete | - |
| 2. Payroll Prep | 0/TBD | Not started | - |
| 3. Daily Checklist App | 0/TBD | Not started | - |
