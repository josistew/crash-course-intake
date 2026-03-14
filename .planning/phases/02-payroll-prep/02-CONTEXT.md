# Phase 2: Payroll Prep - Context

**Gathered:** 2026-03-14
**Status:** Ready for planning

<domain>
## Phase Boundary

Operator pastes Square Labor CSV into an import tab. The Sheet auto-calculates daily hours per employee per location, aggregates cross-location before overtime threshold, color-codes overtime status, tracks graduated pay tier milestones, and produces a Gusto-ready output tab. This is a pure Google Sheets build extending the Phase 1 workbook pattern.

</domain>

<decisions>
## Implementation Decisions

### Hours Aggregation
- Square POS is the clock-in system (confirmed by Rez)
- Cross-location hours must be aggregated per employee BEFORE overtime threshold is applied (PAY-04)
- Daily breakdown showing hours per day, rolling into weekly total
- One Square Labor CSV paste per pay period

### Overtime Tracking
- Color-coded: green (<32 hrs), yellow (32-38 hrs), red (38+ hrs)
- Running tracker through the week — flags approaching overtime by mid-week
- Federal 40-hour weekly threshold

### Pay Tier Tracking
- "Graduated" = pay tiers with milestone-based raises (90 days, certifications — confirmed by Rez)
- Employee roster with hire date, current rate, tier, next milestone date, days-until
- Auto-flag when approaching a milestone
- Exact tier rules and raise amounts TBD — need from Rez on Monday

### Gusto Integration
- Gusto is the payroll system (confirmed by Rez)
- Output tab formatted for Gusto Smart Import (flexible column mapping)
- Columns needed: employee name, total hours, overtime hours, current pay rate
- Rez reviews the prep tab then submits to Gusto manually

### Claude's Discretion
- Whether payroll lives in the same workbook as weekly reporting or a separate file
- Tab naming and organization within the payroll section
- How the Employee Roster from Phase 1 is reused or extended
- Specific conditional formatting details beyond the green/yellow/red scheme

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `scripts/build_weekly_report.py` — Phase 1 openpyxl generator pattern (MATCH-based formulas, conditional formatting, tab structure)
- `scripts/sample_data.py` — Can extend with Square Labor sample data
- Employee-Roster tab already built in Phase 1 workbook with hire date, pay rate, pay tier columns

### Established Patterns
- MATCH-based column headers (survive CSV reordering)
- ISNUMBER validation row for import tabs
- Clear-and-paste workflow with Instructions tab
- openpyxl for .xlsx generation

### Integration Points
- Employee Roster tab connects Phase 1 (labor cost manual entry) to Phase 2 (automated hours × rate)
- Square Labor import can feed back into Phase 1 location calc tabs for automated labor cost %

</code_context>

<specifics>
## Specific Ideas

- Rez said "daily clock-ins" means end-of-day summary + running overtime tracker (from follow-up quiz)
- Pay period: need to confirm weekly vs biweekly with Rez on Monday
- Gusto Smart Import is flexible — auto-maps columns, no rigid template required (from research)

</specifics>

<deferred>
## Deferred Ideas

- Square API integration for automated labor data pull (v2)
- Direct Gusto API submission (v2)
- Daily automated clock-in summary push (v2)

</deferred>

---

*Phase: 02-payroll-prep*
*Context gathered: 2026-03-14*
