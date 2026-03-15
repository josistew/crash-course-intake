---
phase: 03-daily-checklist-app
plan: "01"
subsystem: scaffold-and-data-layer
tags: [next-js, tailwind-v4, google-sheets, server-action, session-context, typescript]
dependency_graph:
  requires: [03-00]
  provides: [next-js-project, sheets-auth, checklist-config, append-completion, session-context]
  affects: [03-02, 03-03]
tech_stack:
  added:
    - googleapis@^171
    - Barlow Condensed (Google Font — display/headings)
    - Barlow (Google Font — body)
  patterns:
    - Google Sheets read-write service account auth (adapted from LeaseJenny pattern)
    - Next.js Server Action with 'use server' directive for Sheets writes
    - React context with in-memory state only (no localStorage) for shared-tablet use case
    - Exponential backoff (2^attempt * 500ms) for Sheets API rate limit handling
    - Tailwind v4 with CSS custom properties for design system tokens
key_files:
  created:
    - /Users/josi/rez-checklist/src/lib/types.ts
    - /Users/josi/rez-checklist/src/lib/sheets.ts
    - /Users/josi/rez-checklist/src/lib/checklist-config.ts
    - /Users/josi/rez-checklist/src/actions/completions.ts
    - /Users/josi/rez-checklist/src/context/SessionContext.tsx
    - /Users/josi/rez-checklist/.env.local
  modified:
    - /Users/josi/rez-checklist/src/app/layout.tsx
    - /Users/josi/rez-checklist/src/app/globals.css
    - /Users/josi/rez-checklist/src/app/page.tsx
    - /Users/josi/rez-checklist/package.json
    - /Users/josi/rez-checklist/src/__tests__/checklist-config.test.ts
    - /Users/josi/rez-checklist/src/__tests__/actions.completions.test.ts
    - /Users/josi/rez-checklist/src/__tests__/layout.test.tsx
decisions:
  - "Used read-write spreadsheets scope (not readonly) — completions Server Action requires append access"
  - "INSERT_ROWS (not OVERWRITE) for concurrent tablet safety — multiple tablets may write simultaneously"
  - "In-memory React context only for session state — prevents ghost sessions on shared tablets if page reloads"
  - "Barlow Condensed chosen for display: bold, industrial, legible on tablets at large sizes; avoids generic AI defaults"
  - "Warm industrial color theme (deep charcoal #1a1714 + copper #c8702a) — references kitchen/ops environment"
  - "Exponential backoff capped at 3 retries (500/1000/2000ms) — balances resilience vs user-perceived delay on tablet"
  - "Checklist items hardcoded as placeholders — Rez to confirm actual SOPs; getItemsForSession filter already supports locationOverride for future customization"
metrics:
  duration_seconds: 900
  completed_date: "2026-03-15"
  tasks_completed: 2
  files_created: 5
  files_modified: 7
---

# Phase 3 Plan 1: Scaffold and Data Layer Summary

**One-liner:** Next.js project scaffolded with Tailwind v4, Barlow Condensed font, warm industrial theme; full data layer (Sheets auth, checklist config, appendCompletion Server Action with retry backoff, in-memory session context) ready for Plan 02 UI consumption.

## What Was Built

### Task 1: Scaffold — Layout, Theme, Fonts

**Layout (`src/app/layout.tsx`):**
- `Barlow_Condensed` (display, 400/600/700/800) + `Barlow` (body, 400/500/600) via `next/font/google`
- `viewport` export: `maximumScale: 1`, `userScalable: false` — prevents pinch-zoom on shared tablets
- Metadata title: "Rez Checklist"
- Wraps children in `SessionProvider` from context module

**Theme (`src/app/globals.css`):**
- CSS variables: `--bg` (#1a1714 deep charcoal), `--fg` (#f5f0e8 warm white), `--accent` (#c8702a copper), `--card`, `--card-border`, `--success`, `--warning`, `--danger`, all with secondary variants
- Layered background: diagonal 41px line texture over radial amber gradient — creates warm kitchen atmosphere without being flat
- Touch target utilities: `min-height: 48px` on button/input (tablet-optimized)
- Keyframe animations: `check-pop`, `fade-in-up` — ready for Plan 02's checklist interactions

### Task 2: Data Layer

**`src/lib/types.ts`** — Shared TypeScript contracts:
- `ShiftType = 'Opening' | 'Closing'`
- `Category` union (4 values)
- `LOCATIONS` const array (5 locations)
- `SessionState` and `CompletionEvent` interfaces

**`src/lib/sheets.ts`** — Google Sheets auth helpers:
- `getAuth()`: decodes base64 service account key, returns `GoogleAuth` with read-write scope
- `getSheets()`: returns authenticated sheets client
- `readTab(tabName, range)`: general-purpose tab reader for Plan 03 dashboard

**`src/lib/checklist-config.ts`** — Checklist data:
- `ChecklistItem` interface with `locationOverride` support
- 18 placeholder items across all 4 categories (Opening/Closing/Both shifts)
- `getItemsForSession(location, shift)`: filters by shift match and location override

**`src/actions/completions.ts`** — Server Action:
- `'use server'` directive
- 8-column row: `[timestamp, location, shift, staffName, itemId, itemText, category, notes]`
- `sheets.spreadsheets.values.append` with `INSERT_ROWS` + `USER_ENTERED`
- Exponential backoff: up to 3 attempts, delays 500ms → 1000ms → 2000ms on HTTP 429

**`src/context/SessionContext.tsx`** — Session state:
- `SessionProvider` and `useSession()` hook
- In-memory state: `location`, `shift`, `staffName` (all nullable)
- `isReady: boolean` computed (all three fields set)
- `reset()` clears all fields — for "New Session" after shift completion
- No `localStorage` or `sessionStorage` — prevents stale state on shared tablets

### Tests Implemented (19 passing)

| File | Tests | Requirement |
|------|-------|-------------|
| checklist-config.test.ts | 10 | CHK-03 |
| actions.completions.test.ts | 5 | CHK-06 |
| layout.test.tsx | 4 | CHK-09 |

## Deviations from Plan

**1. [Rule 3 - Blocking] Directory already existed from 03-00 parallel execution**
- **Found during:** Task 1 start
- **Issue:** `/Users/josi/rez-checklist/` already existed with Next.js project scaffolded by 03-00 (create-next-app had already run); `npx create-next-app` would have failed on non-empty directory
- **Fix:** Skipped create-next-app; added googleapis and testing deps via `npm install` directly; manually wrote all configuration files on top of existing scaffold
- **Impact:** None — all required files created/updated successfully

**2. [Rule 1 - Bug] package.json `jest` key conflict with jest.config.ts from 03-00**
- **Found during:** Task 2 setup
- **Issue:** Added `jest` config key to package.json, but 03-00 had already created `jest.config.ts` using `next/jest` wrapper — Jest would error on multiple configs
- **Fix:** Removed `jest` key from package.json; tests run via jest.config.ts (next/jest wrapper handles transforms correctly)
- **Files modified:** package.json

**3. [Rule 1 - Bug] Exponential backoff test with fake timers caused unhandled rejection**
- **Found during:** Task 2 test run
- **Issue:** Test "throws after 3 retries on persistent 429" used `await expect(promise).rejects.toThrow()` after fake timer advancement, but the promise rejection surfaced before the async assertion, triggering an `UnhandledPromiseRejection`
- **Fix:** Wrapped the promise in `.catch()` to capture the error, then advanced timers, then asserted on the captured error and call count
- **Files modified:** src/__tests__/actions.completions.test.ts

## Commits

| Hash | Message |
|------|---------|
| 446cf64 | feat(03-01): scaffold Next.js project with Tailwind v4, distinctive font, restaurant-ops theme |
| d162e05 | feat(03-01): add full data layer — types, sheets auth, checklist config, Server Action, session context |

## Self-Check: PASSED

Files verified to exist:
- /Users/josi/rez-checklist/src/lib/types.ts — FOUND
- /Users/josi/rez-checklist/src/lib/sheets.ts — FOUND
- /Users/josi/rez-checklist/src/lib/checklist-config.ts — FOUND
- /Users/josi/rez-checklist/src/actions/completions.ts — FOUND
- /Users/josi/rez-checklist/src/context/SessionContext.tsx — FOUND
- /Users/josi/rez-checklist/src/app/layout.tsx — FOUND
- /Users/josi/rez-checklist/src/app/globals.css — FOUND

Commits verified: 446cf64, d162e05 in rez-checklist git log.
Build: passes (Next.js 16.1.6 Turbopack, 0 errors).
Tests: 19/19 passing (CHK-03, CHK-06, CHK-09).
Verification: INSERT_ROWS used, no readonly scope, no localStorage in production code.
