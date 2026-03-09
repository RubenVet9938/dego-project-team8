# Project Tracking — Group 8

---

## Milestone Checklist

### Setup
- [x] GitHub repo created and public
- [x] All 4 members added and onboarded
- [x] Folder structure created
- [x] Dataset added to `data/`
- [x] All 4 names + student IDs in README

### 01-data-quality.ipynb
- [x] Load and parse nested JSON into flat DataFrame
- [x] Identify duplicates, missing values, invalid values
- [x] Identify inconsistent encoding, date formats, wrong dtypes
- [x] Quantify every issue: count + % of affected records
- [x] Demonstrate remediation in code
- [x] Notebook runs clean

### 02-bias-analysis.ipynb
- [x] Gender approval rates + Disparate Impact ratio
- [x] Age-based approval patterns
- [x] Proxy discrimination (ZIP code + spending behavior)
- [x] Age × gender interaction effects
- [x] Logistic regression (p = 0.001)
- [x] Notebook runs clean

### 03-privacy-demo.ipynb
- [x] Identify all 7 PII fields
- [x] SHA-256 pseudonymization with secret salt
- [x] GDPR mapping (Art. 5, 6, 9, 17, 22, 25, 30, 32)
- [x] EU AI Act — high-risk classification (Annex III)
- [x] Audit trail, HITL, retention policy, erasure pipeline
- [x] Notebook runs clean

### README
- [x] Executive summary, all analysis sections, recommendations
- [x] Individual contributions filled in

### Video
- [x] All 4 members speaking, key numbers cited
- [x] Link added to README

### Final Submission
- [x] All notebooks run clean
- [x] All 4 members have commits, repo is public
- [ ] Moodle submission done
- [ ] Peer evaluation submitted (within 48h of Session 6)

---

## Milestone Log

| Milestone | Commit Message | Contributor |
|---|---|---|
| Repository initialised | Initial commit | Ruben Vetter |
| README updates | Names added | Ruben Vetter, Malin Busch |
| Folder structure created | Add project folders | Ruben Vetter |
| Team onboarding | Add Michael Schneider to team members | Michael Schneider |
| Raw dataset added | Add raw credit applications dataset | Michael Schneider |
| Data quality pipeline | Update data quality analysis | Michael Schneider |
| Notebooks added | Add bias + privacy notebooks | Michael Schneider |
| Cleaned CSV added | Add cleaned credit applications CSV | Michael Schneider |
| PR #1 + #2 merged | Privacy notebook + cleaned CSV | Michael Schneider |
| Bias analysis | Discrimination analysis, logistic regression, ZIP proxy, spending patterns | Matteo De Francesco |
| PR #3 merged | Bias notebook + data type fixes | Ruben Vetter |
| Privacy analysis finalised | Added Privacy Analysis | Ruben Vetter |
| PR #4 merged | Privacy analysis finalised | Matteo De Francesco |
| README finalised | Modified README file | Malin Busch |

> Commit counts do not reflect the full distribution of project work. All four team members contributed equally.