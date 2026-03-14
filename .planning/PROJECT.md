# Rez Operations Suite — Moto Medi / Tikka Shack

## What This Is

A suite of automation tools for Rez, a restaurant operator running 5 locations across 2 brands (Moto Medi — 3 Mediterranean fast casual in Lubbock/Amarillo, Tikka Shack — multi-location Indian fast casual franchise). Three systems: a consolidated weekly reporting Google Sheet, a payroll automation Sheet, and a tablet-friendly daily checklist web app. All designed to replace manual number-pulling, spreadsheet assembly, and paper checklists.

## Core Value

Eliminate hours of manual weekly reporting across 5 locations by consolidating Square, delivery platforms, and BEK Entree data into a single automated view.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Weekly reporting Sheet that consolidates data from Square, DoorDash, UberEats, Grubhub, and BEK Entree
- [ ] Auto-calculated metrics: net revenue, food cost %, labor cost %, order volume, avg ticket per location
- [ ] Week-over-week comparison with variance flags (>5% change)
- [ ] Consolidated summary tab across all 5 locations
- [ ] Daily hours summary from Square clock-in data by location
- [ ] Running weekly overtime tracker with color-coded alerts
- [ ] Graduated pay tier tracker (milestone-based raises: 90 days, certifications)
- [ ] Gusto-ready payroll prep output
- [ ] Tablet-friendly daily checklist web app (opening, closing, cleaning, equipment)
- [ ] Location and shift selector
- [ ] Tap-to-complete checklist items with optional notes
- [ ] Completion timestamps (who, when, which location)
- [ ] Manager dashboard showing checklist completion across all locations

### Out of Scope

- API-based auto-pull from delivery platforms — Phase 2 (start with CSV paste-in)
- Square API integration — Phase 2 (start with CSV export)
- Quarterly KPI bonus report — depends on weekly reporting being stable first
- Feedback automation (review monitoring/responses) — separate project after core builds
- Ingredient price tracker — extension of weekly reporting Sheet, add after v1
- Real-time clock-in monitoring — Rez only needs end-of-day summaries

## Context

- **Client:** Rez — zero coding background, heavy ChatGPT user, uses Zapier for some automations
- **Ops partner** also uses systems — outputs must be clear for non-technical users
- **Stack:** Square POS (all locations, also clock-in), Gusto (payroll), Google Workspace (Sheets/Drive), DoorDash/UberEats/Grubhub, BEK Entree (food distributor, CSV export available), Meta Business Suite
- **Current state:** Logs into each dashboard manually, copies numbers by hand, pieces together a loose weekly template. Payroll prep is manual from Square exports into Gusto.
- **Engagement:** Josiah builds, presents gameplan Monday 3/16. Rez reviews and provides sample data exports to plug in.
- **Existing code:** Static HTML intake quiz and follow-up quiz (web3forms), crash course content. New builds are additive.

## Constraints

- **Data format:** Must work with CSV exports initially — no API keys or OAuth setup required from Rez
- **Hosting:** Vercel free tier for checklist app (same as LeaseJenny dashboard pattern)
- **Sheets:** Google Sheets for reporting/payroll (Rez already lives in Google Workspace)
- **Checklist device:** Shared tablet at each store, accessed via bookmarked URL
- **No GHL:** Don't use GoHighLevel for this — it's shared and we can't edit existing items
- **Design:** Follow CLAUDE.md aesthetics guide — distinctive, no AI slop

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| CSV paste-in over API integration for v1 | Fastest to ship, no auth setup needed from Rez, reduces complexity | — Pending |
| Google Sheets over custom dashboard for reporting | Rez already uses Sheets, familiar interface, easy to share with ops partner | — Pending |
| Next.js + Vercel for checklist app | Proven pattern (LeaseJenny dashboard), free hosting, mobile-friendly | — Pending |
| Google Sheets as checklist data store | Keeps everything in Google ecosystem, familiar for Rez to inspect | — Pending |

---
*Last updated: 2026-03-14 after initialization*
