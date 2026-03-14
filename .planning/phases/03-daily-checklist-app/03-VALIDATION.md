---
phase: 3
slug: daily-checklist-app
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-14
---

# Phase 3 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Next.js dev server + manual tablet testing |
| **Config file** | next.config.js |
| **Quick run command** | `npm run build` |
| **Full suite command** | `npm run build && npm run start` + manual checklist flow |
| **Estimated runtime** | ~15 seconds build, manual testing as needed |

---

## Sampling Rate

- **After every task commit:** `npm run build` succeeds, no TypeScript errors
- **After every plan wave:** Full build + dev server + walk through checklist flow
- **Before `/gsd:verify-work`:** Full flow test on tablet viewport, verify Sheets write
- **Max feedback latency:** ~15 seconds (build)

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Verification Method | Status |
|---------|------|------|-------------|-----------|---------------------|--------|
| 03-01-01 | 01 | 1 | CHK-01 | automated | Build succeeds, location/shift selector renders | ⬜ pending |
| 03-01-02 | 01 | 1 | CHK-02 | automated | Name entry component renders | ⬜ pending |
| 03-01-03 | 01 | 1 | CHK-03 | manual | Checklist categories display correctly | ⬜ pending |
| 03-01-04 | 01 | 1 | CHK-04 | manual | Tap-to-complete with timestamp | ⬜ pending |
| 03-01-05 | 01 | 1 | CHK-05 | manual | Notes field works on any item | ⬜ pending |
| 03-01-06 | 01 | 1 | CHK-06 | automated | Sheets API write succeeds (check log tab) | ⬜ pending |
| 03-01-07 | 01 | 1 | CHK-07 | manual | Manager dashboard shows all locations | ⬜ pending |
| 03-01-08 | 01 | 1 | CHK-08 | automated | Vercel deploy succeeds | ⬜ pending |
| 03-01-09 | 01 | 1 | CHK-09 | manual | Tablet viewport renders without pinch-zoom | ⬜ pending |

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Tap-to-complete UX | CHK-04 | Touch interaction | Tap items on tablet viewport, verify timestamp appears |
| Notes field | CHK-05 | Text input UX | Add note to item, verify it saves |
| Manager dashboard | CHK-07 | Visual layout | Check all 5 locations show status |
| Tablet rendering | CHK-09 | Device-specific | Use Chrome DevTools tablet viewport or real tablet |

---

## Validation Sign-Off

- [ ] Build succeeds with no TypeScript errors
- [ ] Checklist flow works end-to-end (select → name → complete → Sheets write)
- [ ] Manager dashboard reads from Sheets completions
- [ ] Deployed to Vercel successfully
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
