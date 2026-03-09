# Project Tracking

## Workflow Overview
The project followed a sequential pipeline built on a single shared feature branch (`RubenVet9938/feature/data-quality-notebook`), with changes merged into `main` via four pull requests. Notebooks were developed iteratively, with each depending on the stable output of the previous one.
---

## Milestone Checklist

### Setup
- [x] GitHub repo created and public
- [x] All 4 members added and onboarded
- [x] Folder structure created (`data/`, `notebooks/`, `src/`, `presentation/`, `docs/`)
- [x] Dataset added to `data/`
- [x] Team members filled in README.md (all 4 names + student IDs)

### Analysis

**01-data-quality.ipynb**
- [x] Load and parse nested JSON into flat DataFrame
- [x] Identify and count duplicate records
- [x] Identify inconsistent data types (e.g. income stored as string)
- [x] Identify missing / null values — per-column % missing
- [x] Identify inconsistent categorical coding (e.g. gender as `M` / `Male` / `male`)
- [x] Identify invalid / impossible values (e.g. negative credit history months)
- [x] Identify inconsistent date formats
- [x] Quantify every issue: count + % of affected records
- [x] Demonstrate remediation steps in code
- [x] Notebook runs clean (restart kernel → run all)

**02-bias-analysis.ipynb**
- [x] Calculate gender approval rates (female vs. male)
- [x] Calculate Disparate Impact ratio — `DI = approval_rate(female) / approval_rate(male)`
- [x] Interpret DI against four-fifths rule (threshold: 0.8)
- [x] Analyse age-based approval patterns
- [x] Proxy discrimination analysis — ZIP code and spending_behavior correlated with protected attributes
- [x] Investigate interaction effects (age × gender)
- [x] Visualisations for all bias patterns
- [x] Statistical test — logistic regression to back up DI findings (p = 0.001)
- [x] Notebook runs clean (restart kernel → run all)

**03-privacy-demo.ipynb**
- [x] Identify all PII fields: `full_name`, `email`, `ssn`, `ip_address`, `date_of_birth`, `zip_code`
- [x] Demonstrate pseudonymization of PII fields (SHA-256 hash with secret salt)
- [x] Map findings to GDPR: Art. 5, 6, 7, 9, 17, 22, 25, 30
- [x] Reference EU AI Act — credit scoring as high-risk (Annex III)
- [x] Propose and implement concrete governance controls (audit trail, human oversight, consent tracking, retention policy, erasure pipeline)
- [x] Notebook runs clean (restart kernel → run all)

**README**
- [x] Executive summary written
- [x] Data quality table filled in with real numbers
- [x] Bias section filled in (DI ratio value + interpretation)
- [x] Privacy table filled in (controls implemented)
- [x] Governance recommendations written
- [x] Individual contributions filled in

### Video
- [x] All 4 members recorded and speaking
- [x] Duration checked (target: 5:45, max: 6:00)
- [x] Key visualizations shown
- [x] Specific numbers cited (DI ratio, duplicate count, etc.)
- [x] Uploaded and link added to README

### Final Submission
- [x] All notebooks run clean (restart kernel → run all)
- [x] All 4 members have commits
- [x] Repo is public
- [ ] Moodle submission done (GitHub URL)
- [ ] Deadline: 23:59 day before Session 6

### After Session 6
- [ ] Peer evaluation submitted on Moodle (within 48h)

---

## Milestone Log

| Milestone | Commit Message | Contributor |
|---|---|---|
| Repository initialised | Initial commit | Ruben Vetter |
| README first update | ReadMe first Update: Name added Ruben Vetter | RubenVet9938 |
| README second update | ReadMe second Update: Name added Malin Busch | Malin Busch |
| Folder structure created | Add project folders | RubenVet9938 |
| Team onboarding completed | Add Michael Schneider to team members | Michael Schneider |
| Raw dataset added | Add raw credit applications dataset | Michael Schneider |
| Data quality pipeline developed | Update data quality analysis with cleaning and remediation steps | Michael Schneider |
| Bias notebook added | Add bias analysis notebook | Michael Schneider |
| Privacy notebook added | Add privacy demo notebook | Michael Schneider |
| Cleaned CSV added to repository | Add cleaned credit applications CSV | Michael Schneider |
| PR #1 merged into main | Merge pull request #1 from RubenVet9938/feature/data-quality-notebook | Michael Schneider |
| PR #2 merged into main | Merge pull request #2 from RubenVet9938/feature/data-quality-notebook | Michael Schneider |
| Bias analysis started | Started discrimination analysis | Matteo De Francesco |
| Logistic regression added | Added logistic regression for gender bias (stat. significant) | Matteo De Francesco |
| Uncleaned columns removed, data types fixed | Remove uncleaned columns from cleaned CSV, fix data types | Michael Schneider |
| ZIP code proxy analysis added | ZIP code analysis | Matteo De Francesco |
| Merge conflict resolved | Resolve merge conflict in bias-analysis notebook | Michael Schneider |
| Date parsing fixed, 161 records recovered | Fixed date parsing, recovered 161 records | Matteo De Francesco |
| Spending pattern analysis completed | Finished spending pattern analysis | Matteo De Francesco |
| Gambling sanity check added | Added sanity check to spending by gender | Matteo De Francesco |
| Recap and conclusion added | Added recap | Matteo De Francesco |
| PR #3 merged into main | Merge pull request #3 from RubenVet9938/feature/data-quality-notebook | Ruben Vetter |
| Privacy analysis finalised | Added Privacy Analysis | RubenVet9938 |
| PR #4 merged into main | Merge pull request #4 from RubenVet9938/feature/data-quality-notebook | Matteo De Francesco |
| Plot labels and typos fixed | Fixed plot labels and typos | Matteo De Francesco |
| README finalised | Modified README file | Malin Busch |

---

## Pull Request Summary

| PR | Branch | Description | Merged by |
|---|---|---|---|
| #1 | RubenVet9938/feature/data-quality-notebook | Privacy demo notebook added to repository | Michael Schneider |
| #2 | RubenVet9938/feature/data-quality-notebook | Cleaned CSV added to `data/` | Michael Schneider |
| #3 | RubenVet9938/feature/data-quality-notebook | Bias notebook integrated; uncleaned columns removed; data types fixed | Ruben Vetter |
| #4 | RubenVet9938/feature/data-quality-notebook | Privacy analysis finalised and integrated | Matteo De Francesco |

---

## Notes

- Commit counts do not reflect the full distribution of project work. Commit frequency is influenced by workflow style and does not capture research, analysis, writing, or coordination efforts.
- All four team members contributed equally to the overall project.