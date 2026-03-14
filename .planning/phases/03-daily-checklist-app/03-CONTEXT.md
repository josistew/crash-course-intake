# Phase 3: Daily Checklist App - Context

**Gathered:** 2026-03-14
**Status:** Ready for planning

<domain>
## Phase Boundary

Tablet-friendly Next.js web app deployed to Vercel. Staff select location + shift, enter name, complete categorized checklist items with tap-to-complete and optional notes. Completions write to Google Sheets. Manager dashboard shows all-location status. No login/authentication — shared tablet use case.

</domain>

<decisions>
## Implementation Decisions

### Checklist Content
- Categories: opening procedures, closing procedures, cleaning/sanitation, equipment checks (confirmed by Rez)
- Location-specific items may vary — structure should support per-location customization
- Shift types: Opening and Closing

### User Flow
- Staff tap location → tap shift (Opening/Closing) → enter name → see checklist → tap items to complete
- No login/password required — name entry only (shared tablet, minimal friction)
- Optional notes field on any item (e.g., "ice machine not working")
- Automatic timestamp on completion

### Data Storage
- Google Sheets as data store (keeps everything in Google ecosystem, familiar for Rez)
- Completions log: staff name, location, shift, item, timestamp
- googleapis service account for Sheets API (same pattern as LeaseJenny dashboard)

### Device & Display
- Shared tablet at each store (confirmed by Rez)
- Tablet-optimized: large tap targets, no pinch-zoom
- Bookmarked URL on each store's tablet

### Manager Dashboard
- All-location completion view for today
- No data entry from managers — reads from Sheets completions log
- Shows: which shifts complete, in progress, not started

### Claude's Discretion
- Specific UI design, color scheme, animations
- Checklist item organization within categories
- How manager dashboard aggregates/displays data
- Whether checklist items are hardcoded or configurable via Sheet

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- LeaseJenny dashboard pattern: Next.js + Google Sheets API + Vercel deploy (at /Users/josi/leasejenny-dashboard/)
- googleapis service account auth pattern already proven

### Established Patterns
- CLAUDE.md aesthetics guide: distinctive fonts, no AI slop, cohesive theme
- Vercel free tier deployment
- Google Sheets as lightweight database

### Integration Points
- New standalone project directory (not in crash-course-intake repo)
- Google Sheets completions log — separate Sheet from the reporting workbook
- Vercel deployment — separate from any existing projects

</code_context>

<specifics>
## Specific Ideas

- Rez checks things on his phone between locations — manager dashboard should be mobile-scannable too
- Ops partner will also check the dashboard
- 5 locations: Moto Medi Lubbock 1, Moto Medi Lubbock 2, Moto Medi Amarillo, Tikka Shack 1, Tikka Shack 2

</specifics>

<deferred>
## Deferred Ideas

- Completion trend analysis over time per location (v2)
- Shift handoff notes visible to next shift (v2)
- Photo attachment for equipment issues (v2)

</deferred>

---

*Phase: 03-daily-checklist-app*
*Context gathered: 2026-03-14*
