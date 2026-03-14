# Phase 1: Weekly Reporting - Context

**Gathered:** 2026-03-14
**Status:** Ready for planning

<domain>
## Phase Boundary

Operator pastes CSVs from 5 platforms (Square, DoorDash, UberEats, Grubhub, BEK Entree) into dedicated import tabs. The Sheet auto-calculates net revenue, purchase cost %, labor cost %, order volume, and average ticket size per location. A consolidated summary tab shows all 5 locations with week-over-week variance flags. This is a pure Google Sheets build — no code.

</domain>

<decisions>
## Implementation Decisions

### Import Workflow
- One import tab per platform (5 tabs: Square, DoorDash, UberEats, Grubhub, BEK)
- Clear-and-paste: operator clears last week's data, pastes new CSV. Prior week stored in a separate "Prior Week" tab for comparison
- Instructions tab as the first tab: step-by-step guide for each platform ("Go to Square > Reports > Sales Summary > Export CSV > Paste into Square tab")
- Weekly batch cadence: all 5 CSVs pasted in one sitting, Monday morning ritual
- MATCH-based column headers in all formulas — survive CSV column reordering

### Metric Definitions
- Net revenue = after all delivery fees/commissions (what hits Rez's bank account)
- Purchase cost % = BEK purchases / total revenue. Labeled "Purchase Cost %" (not "Food Cost %") to be honest about no inventory counts
- Labor cost uses employee roster tab with static pay rates (hours × rate = estimated labor cost)
- Timing: match by order/transaction date, not payout date — aligns revenue with the week it was earned

### Visual Presentation
- Summary tab: locations as columns, metrics as rows. KPIs only (5-6 key numbers per location), drill into location tab for full breakdown
- Week-over-week: arrow + percentage next to each metric (↑ +3.2% or ↓ -7.1%). Red/green color coding for >5% swings
- Brand separation: color-coded sections — Moto Medi locations in one color band, Tikka Shack in another

### Claude's Discretion
- Sheet structure: Claude decides tab count, naming, and organization beyond the import/summary/location pattern
- Specific conditional formatting thresholds beyond the 5% variance flag
- How prior week data is stored and referenced

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- No existing Google Sheets templates in the repo — this is a greenfield Sheets build
- web3forms integration pattern (from intake quiz) is not relevant here

### Established Patterns
- Humanity branding aesthetic (warm paper tones, Fraunces/Outfit fonts) — not applicable to Google Sheets but could influence any web-facing dashboard in Phase 3

### Integration Points
- Employee roster tab created here will also be used by Phase 2 (Payroll) for pay rates
- Square import tab pattern established here will be reused for Square Labor import in Phase 2

</code_context>

<specifics>
## Specific Ideas

- Rez checks the summary on his phone between locations — keep KPI summary scannable at mobile viewport
- Ops partner also uses the Sheet — everything needs to be clear without explanation beyond the Instructions tab
- Rez currently has a "loose template" — this replaces it entirely, not adds to it

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 01-weekly-reporting*
*Context gathered: 2026-03-14*
