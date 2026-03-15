---
phase: 03-daily-checklist-app
plan: "00"
subsystem: test-infrastructure
tags: [jest, react-testing-library, test-stubs, wave-0]
dependency_graph:
  requires: []
  provides: [jest-config, test-stubs-all-8]
  affects: [03-01, 03-02, 03-03]
tech_stack:
  added:
    - jest@^30
    - "@testing-library/react@^16"
    - "@testing-library/jest-dom@^6"
    - jest-environment-jsdom@^30
    - ts-jest@^29
    - "@types/jest@^30"
  patterns:
    - next/jest wrapper for Next.js-aware Jest config
    - setupFilesAfterEnv with jest.setup.ts for RTL matchers
key_files:
  created:
    - /Users/josi/rez-checklist/jest.config.ts
    - /Users/josi/rez-checklist/jest.setup.ts
    - /Users/josi/rez-checklist/src/__tests__/LocationShiftSelector.test.tsx
    - /Users/josi/rez-checklist/src/__tests__/NameEntry.test.tsx
    - /Users/josi/rez-checklist/src/__tests__/checklist-config.test.ts
    - /Users/josi/rez-checklist/src/__tests__/ChecklistItem.test.tsx
    - /Users/josi/rez-checklist/src/__tests__/ChecklistItem.notes.test.tsx
    - /Users/josi/rez-checklist/src/__tests__/actions.completions.test.ts
    - /Users/josi/rez-checklist/src/__tests__/api.dashboard.test.ts
    - /Users/josi/rez-checklist/src/__tests__/layout.test.tsx
  modified:
    - /Users/josi/rez-checklist/package.json
decisions:
  - "Used next/jest wrapper (not raw ts-jest) so Next.js CSS/image transforms are handled automatically"
  - "Removed conflicting jest key from package.json to avoid multiple-config-files error with jest.config.ts"
  - "Fixed deprecated testPathPattern to testMatch glob pattern for Jest 30 compatibility"
  - "scaffolded full Next.js project first (create-next-app) then layered jest deps — 03-01 extends the same project"
metrics:
  duration_seconds: 261
  completed_date: "2026-03-15"
  tasks_completed: 2
  files_created: 10
---

# Phase 3 Plan 0: Jest Test Infrastructure Summary

**One-liner:** Jest 30 + React Testing Library installed with next/jest wrapper; 8 test stub files (32 todo tests) covering CHK-01 through CHK-09 ready for Wave 1 implementation.

## What Was Built

Wave 0 prerequisite: test framework setup so all subsequent implementation plans have automated verification targets.

### Jest Configuration

`jest.config.ts` uses the `next/jest` wrapper which automatically handles Next.js-specific transforms (CSS modules, image imports, server/client component boundaries) without manual configuration. The config sets:
- `testEnvironment: jest-environment-jsdom` — browser-like environment for React component tests
- `setupFilesAfterEnv: ['<rootDir>/jest.setup.ts']` — loads RTL matchers globally
- `testMatch: ['**/__tests__/**/*.{ts,tsx}']` — scoped to the test directory

`jest.setup.ts` imports `@testing-library/jest-dom` which adds matchers like `toBeInTheDocument()`, `toBeDisabled()`, etc. to all test files.

### Test Stub Files

All 8 files under `src/__tests__/` have `describe` blocks with `test.todo` placeholders matching the Validation Architecture in 03-RESEARCH.md:

| File | Requirement | Todos |
|------|-------------|-------|
| LocationShiftSelector.test.tsx | CHK-01 | 4 |
| NameEntry.test.tsx | CHK-02 | 3 |
| checklist-config.test.ts | CHK-03 | 5 |
| ChecklistItem.test.tsx | CHK-04 | 5 |
| ChecklistItem.notes.test.tsx | CHK-05 | 4 |
| actions.completions.test.ts | CHK-06 | 5 |
| api.dashboard.test.ts | CHK-07 | 4 |
| layout.test.tsx | CHK-09 | 2 |

### Verify Commands

```bash
cd /Users/josi/rez-checklist && npx jest --passWithNoTests
# Result: 8 suites, 32 todo, 0 failed — exits 0
```

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] create-next-app scaffolded project before jest install**
- **Found during:** Task 1
- **Issue:** Directory `/Users/josi/rez-checklist/` did not exist; plan notes to scaffold first if needed
- **Fix:** Ran `npx create-next-app@latest rez-checklist --typescript --tailwind --app --src-dir --no-import-alias --yes` in `/Users/josi/` first, then layered jest deps
- **Impact:** package.json also gained `googleapis` dependency (from create-next-app invocation) — no issue for 03-01 which extends the same package.json

**2. [Rule 1 - Bug] Conflicting jest config: package.json `jest` key + jest.config.ts**
- **Found during:** Task 1 verify run
- **Issue:** Jest error "Multiple configurations found" — create-next-app had generated a `jest` key in package.json alongside jest.config.ts
- **Fix:** Removed the `jest` key from package.json entirely; jest.config.ts is the single source of truth
- **Files modified:** package.json

**3. [Rule 1 - Bug] Deprecated `testPathPattern` config key**
- **Found during:** Task 1 verify run
- **Issue:** Jest 30 emits deprecation warning: "Option testPathPattern was replaced by --testPathPatterns"
- **Fix:** Replaced with `testMatch: ['**/__tests__/**/*.{ts,tsx}']` which is the idiomatic config-file approach
- **Files modified:** jest.config.ts

## Commits

| Hash | Message |
|------|---------|
| b41cede | chore(03-00): install Jest + React Testing Library and configure test framework |
| a4526f6 | test(03-00): create 8 test stub files with describe blocks and test.todo placeholders |

## Self-Check: PASSED

All 10 files exist. Both commits found in rez-checklist git log (b41cede, a4526f6).
