---
phase: 03-daily-checklist-app
plan: "03"
subsystem: manager-dashboard
tags: [nextjs, react, google-sheets, dashboard, vercel, tablets]
dependency_graph:
  requires: [03-01, 03-02]
  provides: [manager-dashboard, dashboard-api, vercel-deploy-ready]
  affects: []
tech_stack:
  added: []
  patterns:
    - sheets-query-aggregation
    - no-store-cache-control
    - auto-refresh-setinterval
    - brand-grouped-card-grid
    - next-server-mock-in-jest
key_files:
  created:
    - /Users/josi/rez-checklist/src/app/api/dashboard/route.ts
    - /Users/josi/rez-checklist/src/app/dashboard/page.tsx
    - /Users/josi/rez-checklist/src/components/ManagerDashboard.tsx
    - /Users/josi/rez-checklist/vercel.json
    - /Users/josi/rez-checklist/DEPLOY.md
  modified:
    - /Users/josi/rez-checklist/src/__tests__/api.dashboard.test.ts
decisions:
  - "next/server mock in Jest: NextResponse requires Request global unavailable in jsdom — replaced with a minimal MockResponse class in jest.mock('next/server') so route handler is testable without a full server environment"
  - "Deployment deferred: Vercel deploy not executed — no Google service account credentials configured yet. vercel.json prepared, DEPLOY.md documents all steps including Sheet setup, base64 key encoding, and tablet bookmark setup"
  - "Brand-grouped dashboard: Moto Medi (copper accent) and Tikka Shack (teal accent) separated into visual sections matching the ops reporting workbook; distinct brand colors without relying on location-card color changes"
metrics:
  duration_seconds: 1050
  completed_date: "2026-03-14"
  tasks_completed: 2
  tasks_at_checkpoint: 1
  files_created: 5
  files_modified: 1
  tests_added: 4
---

# Phase 3 Plan 03: Manager Dashboard Summary

**One-liner:** Manager dashboard at /dashboard reads pre-computed Manager-View QUERY tab from Google Sheets, computes complete/in-progress/not-started status for all 5 locations × 2 shifts using getItemsForSession(), auto-refreshes every 60s, with brand-grouped card grid and Vercel deploy guide prepared.

## Tasks Completed

| # | Name | Commit | Key Files |
|---|------|--------|-----------|
| 1 | Build manager dashboard API route and UI | a8aaeeb | api/dashboard/route.ts, dashboard/page.tsx, ManagerDashboard.tsx, api.dashboard.test.ts |
| 2 | Prepare git, Google Sheet instructions, and Vercel deploy config | 8eaac6a | vercel.json, DEPLOY.md |

## Checkpoint Reached

**Task 3: Human verification checkpoint**
- Status: Awaiting deployment credentials and human verification
- Blocked by: Google service account credentials + Vercel deploy not yet executed
- Resume signal: User types "approved" or describes issues after verifying the deployed app

## Verification Results

- `npm run build` exits 0 — /api/dashboard (Dynamic), /dashboard (Static) compiled clean
- 39/39 tests passing (4 new dashboard tests + 35 prior)
- `grep Manager-View src/app/api/dashboard/route.ts` — confirmed pre-computed tab read
- `grep no-store src/app/api/dashboard/route.ts` — confirmed Cache-Control header
- `grep getItemsForSession src/app/api/dashboard/route.ts` — confirmed total item count lookup
- Empty Manager-View handled: all 10 location/shift combos return not-started
- DEPLOY.md documents: Sheet tab setup, QUERY formula with date-filter fallback note, base64 key encoding, Vercel CLI steps, tablet bookmark setup

## Architecture Summary

**API Route (/api/dashboard GET):**
- Reads `Manager-View` tab via `readTab('Manager-View', 'A1:Z100')`
- Parses QUERY output (headers in row 1: Location, Shift, StaffName, ItemsCompleted)
- Loops all 5 LOCATIONS × 2 ShiftTypes, calls `getItemsForSession(location, shift).length` for totalItems
- Status logic: 0 items → not-started; items >= total → complete; else in-progress
- Returns `{ date, locations: LocationShiftStatus[] }` with `Cache-Control: no-store`
- try/catch returns 500 with `{ error: 'Failed to load dashboard data' }` on Sheets API failure

**ManagerDashboard component:**
- `useEffect` fetch on mount + `setInterval(fetchDashboard, 60_000)` auto-refresh
- Loading: skeleton card grid with staggered pulse animation
- Error: "Unable to load dashboard. Try refreshing." with Retry button
- Empty: "No activity yet today" with current date, shown when all shifts are not-started
- Main view: two brand sections (Moto Medi copper / Tikka Shack teal), responsive grid (1→2→3 cols)
- Location cards: name header + done mark when all complete, Opening and Closing shift rows
- Status badges: filled color dot + text (green "Complete", amber "3/8", gray "Not Started")
- Incomplete shifts get subtle warm tint background — draws eye to what needs attention

**Dashboard Page (/dashboard):**
- Static route (no session context needed — managers visit directly)
- Sticky header: "Operations / Shift Status" with today's date
- Back-to-staff link ("← Staff") for accidental navigation from tablet

## Aesthetics Applied

- Command center feel: dense, readable, no wasted space
- Barlow Condensed uppercase labels throughout; brand grouping mirrors reporting workbook
- Moto Medi: copper accent (`var(--accent)`) for brand title and card accents
- Tikka Shack: teal `#5bbfb5` — meaningfully distinct from copper without clashing with the dark base
- Location cards: green glow/border when all-done, amber border when in-progress — satisfaction in the complete state
- Skeleton loading with staggered pulse so the UI feels alive while fetching
- Status badges use filled dot + text at 70% opacity labels — color-first scanning

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] next/server mock required for Jest route testing**
- **Found during:** Task 1 verification
- **Issue:** Importing `GET` from the route handler triggered `next/server` → `Request is not defined` in jsdom. The existing test stub used `jest.mock` for sheets and checklist-config but didn't account for the Next.js server environment requirement.
- **Fix:** Added `jest.mock('next/server', ...)` with a minimal `MockResponse` class (stores body/status in memory, exposes `.json()` and `.headers` Map). Test file imports the route after the mock is established. Headers test asserts against the Map directly.
- **Files modified:** `src/__tests__/api.dashboard.test.ts`
- **Commit:** a8aaeeb

**2. [Deviation from plan note] Vercel deploy not executed**
- **Why:** Important context specified "DO NOT actually deploy yet — we don't have Google service account credentials configured"
- **What was done instead:** Created `vercel.json` (framework config, build command, env var references) and `DEPLOY.md` (full step-by-step guide for Sheet setup, key encoding, CLI deploy, tablet bookmark)
- **Impact:** App is deploy-ready; human checkpoint will confirm credentials and execute deploy

## Self-Check

### Files exist:
- /Users/josi/rez-checklist/src/app/api/dashboard/route.ts — FOUND
- /Users/josi/rez-checklist/src/app/dashboard/page.tsx — FOUND
- /Users/josi/rez-checklist/src/components/ManagerDashboard.tsx — FOUND
- /Users/josi/rez-checklist/vercel.json — FOUND
- /Users/josi/rez-checklist/DEPLOY.md — FOUND

### Commits exist:
- a8aaeeb (Task 1: dashboard API + UI) — FOUND
- 8eaac6a (Task 2: vercel.json + DEPLOY.md) — FOUND

## Self-Check: PASSED
