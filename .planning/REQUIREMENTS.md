# Requirements: Rez Operations Suite

**Defined:** 2026-03-14
**Core Value:** Eliminate hours of manual weekly reporting across 5 locations by consolidating Square, delivery platforms, and BEK Entree data into a single automated view.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Weekly Reporting

- [ ] **RPT-01**: Operator can paste Square Sales Summary CSV into an import tab and data auto-populates location metrics
- [ ] **RPT-02**: Operator can paste DoorDash CSV into an import tab and delivery revenue/orders auto-populate
- [ ] **RPT-03**: Operator can paste UberEats CSV into an import tab and delivery revenue/orders auto-populate
- [ ] **RPT-04**: Operator can paste Grubhub CSV into an import tab and delivery revenue/orders auto-populate
- [ ] **RPT-05**: Operator can paste BEK Entree CSV into an import tab and purchase/COGS data auto-populates
- [x] **RPT-06**: Each location has a dedicated tab showing net revenue, food cost %, labor cost %, order volume (by platform), and avg ticket size
- [x] **RPT-07**: Consolidated summary tab shows all 5 locations side-by-side with brand grouping (Moto Medi vs Tikka Shack)
- [x] **RPT-08**: Week-over-week comparison shows prior week values and percentage change for each metric
- [x] **RPT-09**: Variance flags highlight any metric that changed >5% week-over-week (color-coded: red/green)
- [ ] **RPT-10**: Import tabs use column header matching (MATCH function) so formulas survive CSV column reordering

### Payroll

- [ ] **PAY-01**: Operator can paste Square Labor CSV and daily hours per employee per location auto-populate
- [x] **PAY-02**: Weekly total hours per employee calculated with running daily breakdown
- [x] **PAY-03**: Overtime tracker flags employees approaching 40 hours by mid-week (color-coded: green <32, yellow 32-38, red 38+)
- [x] **PAY-04**: Cross-location hours aggregated per employee before overtime threshold applied (not per-location)
- [ ] **PAY-05**: Employee roster tab with hire date, current pay rate, pay tier, next milestone date, and days-until-milestone
- [ ] **PAY-06**: Pay tier tracker auto-flags employees approaching a graduated raise milestone (90 days, certifications)
- [x] **PAY-07**: Gusto-ready prep output tab with employee name, total hours, overtime hours, and current pay rate

### Daily Checklist

- [x] **CHK-01**: Staff can select their location and shift type (Opening/Closing) on a tablet-friendly interface
- [x] **CHK-02**: Staff can enter their name at shift start (no password/login required)
- [x] **CHK-03**: Checklist displays categorized items: opening procedures, closing procedures, cleaning/sanitation, equipment checks
- [x] **CHK-04**: Staff can tap items to mark complete with automatic timestamp capture
- [x] **CHK-05**: Staff can add optional notes to any checklist item (e.g., "ice machine not working")
- [ ] **CHK-06**: Completion data writes to Google Sheets (who completed, when, which location, which items)
- [ ] **CHK-07**: Manager dashboard shows today's checklist completion status across all locations
- [ ] **CHK-08**: Checklist app deployed to Vercel and accessible via bookmarked URL on store tablets
- [x] **CHK-09**: Tablet-optimized UI with large tap targets, no pinch-zoom required

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Reporting Extensions

- **RPT-11**: Square API integration to auto-pull sales data (replace CSV paste-in)
- **RPT-12**: Delivery platform API integrations where available
- **RPT-13**: Actual vs. theoretical food cost comparison (requires recipe-level data)
- **RPT-14**: Quarterly KPI bonus report generator with customizable manager bonus structure

### Payroll Extensions

- **PAY-08**: Direct Gusto API integration for payroll submission
- **PAY-09**: Scheduled automation to pull Square labor data daily

### Checklist Extensions

- **CHK-10**: Completion trend analysis over time per location (historical patterns)
- **CHK-11**: Shift handoff notes visible to next shift's crew
- **CHK-12**: Photo attachment for equipment issues

### Feedback Automation

- **FEED-01**: Google Business review monitoring with negative alerts
- **FEED-02**: Delivery platform review aggregation
- **FEED-03**: AI-drafted review responses for operator approval

### Ingredient Tracking

- **ING-01**: BEK Entree price change detection and alerts
- **ING-02**: Menu item margin impact calculator
- **ING-03**: Historical ingredient price trend dashboard

## Out of Scope

| Feature | Reason |
|---------|--------|
| Real-time clock-in monitoring | Rez explicitly stated end-of-day summaries are sufficient |
| In-app scheduling | Homebase/7Shifts own this space; separate product category |
| Inventory management with physical counts | Separate product; BEK purchase tracking sufficient for v1 |
| Customer-facing features (ordering, reviews) | Not an ops tool; different product entirely |
| User accounts / authentication for checklist | Adds friction for shared-tablet use; name entry sufficient |
| Push notifications / alerts | Sheets color-coding sufficient for this operator's workflow |
| Recipe costing / menu engineering | Requires significant data entry; only after food cost % is stable |
| Multi-tenant / white-label | Rez is one client; premature abstraction kills shipping speed |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| RPT-01 | Phase 1 | Pending |
| RPT-02 | Phase 1 | Pending |
| RPT-03 | Phase 1 | Pending |
| RPT-04 | Phase 1 | Pending |
| RPT-05 | Phase 1 | Pending |
| RPT-06 | Phase 1 | Complete (01-02) |
| RPT-07 | Phase 1 | Complete (01-02) |
| RPT-08 | Phase 1 | Complete (01-02) |
| RPT-09 | Phase 1 | Complete (01-02) |
| RPT-10 | Phase 1 | Pending |
| PAY-01 | Phase 2 | Pending |
| PAY-02 | Phase 2 | Complete (02-02) |
| PAY-03 | Phase 2 | Complete (02-02) |
| PAY-04 | Phase 2 | Complete (02-02) |
| PAY-05 | Phase 2 | Pending |
| PAY-06 | Phase 2 | Pending |
| PAY-07 | Phase 2 | Complete (02-02) |
| CHK-01 | Phase 3 | Complete (03-02) |
| CHK-02 | Phase 3 | Complete (03-02) |
| CHK-03 | Phase 3 | Complete (03-02) |
| CHK-04 | Phase 3 | Complete (03-02) |
| CHK-05 | Phase 3 | Complete (03-02) |
| CHK-06 | Phase 3 | Pending |
| CHK-07 | Phase 3 | Pending |
| CHK-08 | Phase 3 | Pending |
| CHK-09 | Phase 3 | Complete (03-02) |

**Coverage:**
- v1 requirements: 26 total
- Mapped to phases: 26
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-14*
*Last updated: 2026-03-14 after initial definition*
