---
phase: 2
slug: payroll-prep
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-14
---

# Phase 2 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Manual — Google Sheets via openpyxl (no test framework) |
| **Config file** | none |
| **Quick run command** | `python3 scripts/build_weekly_report.py && python3 -c "import openpyxl; wb=openpyxl.load_workbook('Rez-Weekly-Report.xlsx'); print([s for s in wb.sheetnames])"` |
| **Full suite command** | Run build script, verify all payroll tabs exist with correct structure |
| **Estimated runtime** | ~5 seconds build + manual inspection |

---

## Sampling Rate

- **After every task commit:** Run build script, verify new tabs appear
- **After every plan wave:** Full build + paste sample labor data + verify formulas
- **Before `/gsd:verify-work`:** All payroll tabs tested with sample data
- **Max feedback latency:** ~5 seconds automated, manual inspection as needed

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Verification Method | Status |
|---------|------|------|-------------|-----------|---------------------|--------|
| 02-01-01 | 01 | 1 | PAY-01 | manual | Paste Square Labor CSV → daily hours populate | ⬜ pending |
| 02-01-02 | 01 | 1 | PAY-02 | manual | Weekly totals calculated from daily breakdown | ⬜ pending |
| 02-01-03 | 01 | 1 | PAY-03 | manual | Color coding: green/yellow/red at correct thresholds | ⬜ pending |
| 02-01-04 | 01 | 1 | PAY-04 | manual | Multi-location employee hours aggregated before OT check | ⬜ pending |
| 02-01-05 | 01 | 1 | PAY-05 | manual | Roster shows hire date, rate, tier, milestone, days-until | ⬜ pending |
| 02-01-06 | 01 | 1 | PAY-06 | manual | Approaching-milestone employees flagged | ⬜ pending |
| 02-01-07 | 01 | 1 | PAY-07 | manual | Gusto output tab has name, hours, OT hours, rate | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] Square Labor sample data added to `scripts/sample_data.py`
- [ ] Cross-location employee included in sample data (same name, two locations)

*No test framework needed — pure Sheets build extending Phase 1 pattern.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Labor CSV paste populates hours | PAY-01, PAY-02 | Sheets formula execution | Paste sample data, verify daily+weekly hours |
| OT color coding | PAY-03 | Visual inspection | Check green/yellow/red at 32/38/40 thresholds |
| Cross-location aggregation | PAY-04 | Logic verification | Verify multi-location employee shows combined hours |
| Milestone flagging | PAY-06 | Date-based formula | Set sample hire date to 85 days ago, verify flag |
| Gusto format | PAY-07 | Column inspection | Compare output tab to Gusto Smart Import expectations |

---

## Validation Sign-Off

- [ ] All tasks have manual verification steps defined
- [ ] Cross-location OT aggregation tested with multi-location employee
- [ ] All 7 requirements verifiable
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
