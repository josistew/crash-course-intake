# Feature Landscape

**Domain:** Restaurant operations automation — multi-location fast casual (5 locations, 2 brands)
**Researched:** 2026-03-14
**Confidence:** MEDIUM-HIGH (core features well-established; Rez-specific workflows inferred from context)

---

## Table Stakes

Features that restaurant operators expect from any modern ops tool. Missing these and the tool feels like a downgrade from manual spreadsheets.

### Weekly Reporting System

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Net revenue per location per week | Operators need a single number to judge performance | Low | Square CSV + delivery platform CSVs combined |
| Food cost % (actual) | Industry standard KPI — 28–35% target; operators track weekly | Medium | Requires purchase data (BEK Entree) + sales data |
| Labor cost % | Standard alongside food cost; most restaurants track weekly | Medium | Square clock-in hours + payroll wage data |
| Order volume per platform | Operators want to see DoorDash vs UberEats vs in-store trends | Low | Count of orders from each CSV export |
| Average ticket size | Quick signal for upsell health and order mix shifts | Low | Revenue / order count per platform |
| Week-over-week comparison | Operators can't judge a number without context | Low | Calculated from stored prior week |
| Variance flags on significant changes | Alerts when something shifts >5% — prevents buried problems | Low | Conditional formatting, color-coded thresholds |
| Consolidated summary across all locations | The core value prop — one view instead of 5 dashboards | Medium | Rollup tab from location-specific sheets |

### Payroll Prep

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Daily hours summary per employee per location | Foundation for every downstream payroll calculation | Low | Parsed from Square clock-in CSV |
| Weekly total hours per employee | Required input for any payroll processor | Low | Sum of daily hours |
| Overtime flag and calculation | Federal law (40+ hrs/week), some states have daily overtime rules | Medium | Running weekly total with threshold alert |
| Gusto-ready export format | Rez uses Gusto — output must match what Gusto expects to import | Medium | Column mapping to Gusto's CSV import format |
| Pay rate per employee | Required for any payroll calculation | Low | Static lookup table maintained in Sheet |

### Daily Operational Checklist

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Opening and closing checklists | Core use case for any restaurant checklist app | Low | Static task lists, location-specific |
| Cleaning and equipment checklists | Food safety compliance; health inspections require records | Low | Categorized task lists |
| Shift and location selector | Multi-location app; staff need to see their store's tasks | Low | Simple dropdown/button UI |
| Tap-to-complete task items | Mobile/tablet-first interaction model — typing is friction | Low | Toggle state, no forms |
| Completion timestamps | Accountability trail; "when was the fryer cleaned?" | Low | Auto-capture on tap |
| Who completed each item | Manager accountability visibility | Low | Associated with login/name at shift start |
| Optional notes per item | Exception logging — "ice machine not working" | Low | Freetext field, optional |
| Manager dashboard — all locations | Multi-location owners need a status board, not per-location views | Medium | Aggregate view of today's checklists |

---

## Differentiators

Features that go beyond what any checklist or reporting app offers. Not expected, but create clear competitive distance when done well.

### Reporting Differentiators

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Multi-platform delivery aggregation (Square + DoorDash + UberEats + Grubhub) | Most tools require API integrations or paid middleware; CSV-first approach is instantly deployable | Medium | Paste-in workflow; maps platform-specific CSV formats to unified schema |
| BEK Entree food distributor integration | Purpose-built for this supply chain relationship — not generic | Medium | BEK CSV column mapping to COGS calculation |
| Actual vs. theoretical food cost | Shows where food is disappearing vs. what should have been used | High | Requires recipe-level data; Phase 2 candidate |
| Cross-brand comparison (Moto Medi vs. Tikka Shack) | Two-brand operator can see which concept outperforms | Low | Tag locations by brand in summary tab |
| Graduated pay tier tracker | Milestone-based raises (90-day, certifications) — unique to Rez's compensation model | Medium | Tracks hire date, certification events, auto-flags raise eligibility |
| Quarterly KPI bonus report | Connects weekly data to manager bonus structure — closes the loop | High | Depends on stable weekly reporting baseline; Phase 2+ |

### Checklist Differentiators

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Tablet-optimized UI (not mobile-responsive afterthought) | Shared store tablet is the actual device — most checklist apps are phone-first | Low | Large tap targets, no pinch-zoom required |
| Completion trend over time per location | "Location 3 consistently misses closing tasks on Sundays" — not visible without history | Medium | Requires stored data; Google Sheets as log |
| Shift handoff context | Notes from closing shift visible to opening crew | Medium | Phase 2; requires read-on-open pattern |

---

## Anti-Features

Features to explicitly NOT build in v1 — either because they add complexity without delivering value at this stage, or because they've been confirmed out-of-scope.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| API-based auto-pull from Square, DoorDash, UberEats, Grubhub | Requires OAuth setup from Rez, platform developer accounts, maintenance of API changes — high setup cost, brittle | CSV paste-in; upgrade path exists in Phase 2 |
| Real-time clock-in monitoring | Rez explicitly stated end-of-day summaries are sufficient | End-of-day summary from Square export |
| In-app scheduling | Adds a separate product category (Homebase, 7Shifts own this space); Rez doesn't need it | Out of scope entirely |
| Inventory management | Requires physical counts, unit-of-measure logic, recipe integration — separate product | BEK Entree tracks purchases; COGS% is sufficient for v1 |
| Customer-facing features (online ordering, reviews) | Not an ops tool; completely different product | Separate project (Rez mentioned feedback automation as separate) |
| User accounts / authentication for checklist app | Adds friction for shared-tablet use case; overhead doesn't match value | Location + name entry at shift start; no passwords |
| Push notifications / alerts | Complex to implement; requires notification infrastructure | Color-coded Sheet flags are sufficient for this operator's workflow |
| Recipe costing / menu engineering | Requires significant data entry (every ingredient per dish); value only after food cost% is stable | Phase 3+ extension if food cost% shows problems |
| Multi-tenant / white-label version | Rez is one client right now; premature abstraction kills shipping speed | Build for Rez specifically; extract patterns later |

---

## Feature Dependencies

```
Square CSV export
  → Daily hours summary
      → Weekly total hours
          → Overtime flag + calculation
              → Gusto-ready export
              → Graduated pay tier tracker (also needs hire dates, cert dates)

Square CSV export + Delivery CSVs (DoorDash, UberEats, Grubhub) + BEK Entree CSV
  → Unified revenue row per location per week
      → Net revenue calculation
      → Order volume per platform
      → Average ticket size
      → Food cost % (needs BEK purchase data)
      → Labor cost % (needs hours + wages)
          → Week-over-week comparison (needs prior week stored)
              → Variance flags
                  → Consolidated summary tab
                      → Cross-brand comparison (Moto Medi vs Tikka Shack)

Checklist app (location + name entry at shift start)
  → Tap-to-complete items
      → Completion timestamp + who
      → Optional notes
          → Manager dashboard (reads from Google Sheets log)
              → Completion trend over time (Phase 2)
```

---

## MVP Recommendation

Build these in order — each unlocks the next:

**Phase 1 — Weekly Reporting Sheet**
Consolidates the manual work that takes the most time. Immediate ROI. Proves the system before adding complexity.

Priority features:
1. Net revenue per location (Square + delivery CSV paste-in)
2. Food cost % (BEK Entree CSV)
3. Labor cost % (Square clock-in hours)
4. Week-over-week comparison with variance flags
5. Consolidated summary tab (cross-location + cross-brand view)

**Phase 2 — Payroll Prep Sheet**
Depends on having Square clock-in data pipeline working from Phase 1. Direct labor hours → Gusto workflow.

Priority features:
1. Daily hours summary from Square clock-in data
2. Weekly overtime tracker with alerts
3. Graduated pay tier tracker (milestone-based raise flags)
4. Gusto-ready export format

**Phase 3 — Daily Checklist App**
Standalone; no hard dependency on Phases 1-2 but benefits from brand trust built in earlier phases. Most visible to frontline staff.

Priority features:
1. Tablet-friendly UI, location + shift selector
2. Opening / closing / cleaning / equipment checklists
3. Tap-to-complete with timestamps and name
4. Manager dashboard (all-location completion view)

**Defer:**
- API integrations (Phase 4 — once CSV-first is stable and patterns are known)
- Actual vs. theoretical food cost (Phase 4 — requires recipe data layer)
- Shift handoff notes (Phase 4 — nice-to-have, not blocking)
- Quarterly KPI bonus report (Phase 4 — depends on weekly reporting being stable)

---

## Industry Context

The 2025-2026 restaurant tech landscape is experiencing a correction after post-COVID feature bloat. Operators are actively cutting tools that create complexity without delivering ROI. The winning pattern is:

- **Fewer tools, tighter integration** — operators want one place, not a jigsaw of dashboards
- **Adoption is the real challenge** — not features; tools that require training get abandoned
- **CSV-first is not embarrassing** — it's pragmatic; API integrations add brittleness that small operators don't need
- **Simplicity beats completeness** — a tool used 100% beats a comprehensive tool used 30%

This validates the CSV paste-in approach for v1. The bar for success here is not matching Restaurant365 — it's being 10x easier to use than Rez's current manual process.

---

## Sources

- [13 Best Features of Restaurant Management Software — BEP Back Office](https://bepbackoffice.com/blog/restaurant-management-software-features/)
- [6 Best Digital Restaurant Checklist Apps & Software In 2026 — Operandio](https://operandio.com/restaurant-checklist-app/)
- [Restaurants Reach a Technology Turning Point Rooted in Simplicity — FSR Magazine](https://www.fsrmagazine.com/feature/restaurants-reach-a-technology-turning-point-rooted-in-simplicity/)
- [How to Calculate Restaurant Food Cost Percentage — Restaurant365](https://www.restaurant365.com/blog/how-to-calculate-food-cost-percentage-and-margins/)
- [Beyond the Checklist: Restaurant Task Management Across Locations — Blanket](https://www.blanket.app/blog/beyond-the-checklist-how-restaurant-task-management-software-gives-you-visibility-across-locations/)
- [7 Best Restaurant Payroll Software — Gusto](https://gusto.com/resources/guides/best-restaurant-payroll-software)
- [How to Consolidate Delivery Apps — ChowNow](https://get.chownow.com/blog/how-to-consolidate-delivery-apps/)
- [5 Restaurant Operations Software & Tools Of 2026 — Operandio](https://operandio.com/best-restaurant-operations-software/)
- [Digital Checklists for Restaurants: The Complete Guide — StaffedUp](https://staffedup.com/digital-checklists-for-restaurants/)
- [Restaurant Task Management Software — Xenia](https://www.xenia.team/articles/restaurant-checklist-app)
