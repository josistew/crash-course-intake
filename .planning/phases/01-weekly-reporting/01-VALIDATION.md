---
phase: 1
slug: weekly-reporting
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-14
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Manual — Google Sheets (no code, no test framework) |
| **Config file** | none |
| **Quick run command** | Manual inspection of Sheet formulas and sample data |
| **Full suite command** | Paste sample CSVs into all 5 import tabs, verify all metrics populate |
| **Estimated runtime** | ~5 minutes manual |

---

## Sampling Rate

- **After every task commit:** Visual inspection of affected Sheet tabs
- **After every plan wave:** Full paste-and-verify with sample data
- **Before `/gsd:verify-work`:** All import tabs tested with sample CSVs, all metrics verified
- **Max feedback latency:** N/A — manual verification

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Verification Method | Status |
|---------|------|------|-------------|-----------|---------------------|--------|
| 01-01-01 | 01 | 1 | RPT-01 | manual | Paste Square CSV → verify metrics populate | ⬜ pending |
| 01-01-02 | 01 | 1 | RPT-02 | manual | Paste DoorDash CSV → verify revenue/orders | ⬜ pending |
| 01-01-03 | 01 | 1 | RPT-03 | manual | Paste UberEats CSV → verify revenue/orders | ⬜ pending |
| 01-01-04 | 01 | 1 | RPT-04 | manual | Paste Grubhub CSV → verify revenue/orders | ⬜ pending |
| 01-01-05 | 01 | 1 | RPT-05 | manual | Paste BEK CSV → verify purchase data | ⬜ pending |
| 01-01-06 | 01 | 1 | RPT-06 | manual | Each location tab shows all 5 metrics | ⬜ pending |
| 01-01-07 | 01 | 1 | RPT-07 | manual | Summary tab shows all locations with brand grouping | ⬜ pending |
| 01-01-08 | 01 | 1 | RPT-08 | manual | WoW comparison shows prior values and % change | ⬜ pending |
| 01-01-09 | 01 | 1 | RPT-09 | manual | >5% changes highlighted red/green | ⬜ pending |
| 01-01-10 | 01 | 1 | RPT-10 | manual | Reorder CSV columns → formulas still work | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] Sample CSV data for each platform (placeholder data until Rez provides real exports)
- [ ] Location names defined (Moto Medi Lubbock 1, Moto Medi Lubbock 2, Moto Medi Amarillo, Tikka Shack locations)

*No test framework needed — this is a pure Google Sheets build.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| CSV paste populates metrics | RPT-01 through RPT-05 | Google Sheets — no programmatic test | Paste sample CSV into each import tab, verify data flows to location tabs |
| Location tabs show correct metrics | RPT-06 | Visual inspection | Check each location tab for net revenue, purchase cost %, labor cost %, order volume, avg ticket |
| Summary tab consolidation | RPT-07 | Visual inspection | Verify all 5 locations appear with Moto Medi / Tikka Shack grouping |
| WoW comparison | RPT-08, RPT-09 | Requires two weeks of data | Paste week 1, store as prior, paste week 2, verify comparison and color coding |
| MATCH resilience | RPT-10 | Requires column reorder test | Reorder columns in a sample CSV, re-paste, verify formulas still resolve |

---

## Validation Sign-Off

- [ ] All tasks have manual verification steps defined
- [ ] Sample data created for testing
- [ ] All 10 requirements verifiable through paste-and-inspect
- [ ] MATCH resilience tested with reordered columns
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
