# DEGO Project - Team 8


## Team Members

| Role | Name | Student ID |
|---|---|---|
| Data Engineer | Michael Schneider | 71871 |
| Data Scientist | Matteo De Francesco | 71734 |
| Governance Officer | Ruben Vetter | 70844 |
| Product Lead | Malin Busch | 70145 |

---

## Executive Summary

NovaCred, a fintech company using machine learning to automate loan approval decisions, received a regulatory inquiry regarding potential discrimination in its lending practices. As an external Data Governance Task Force, we were commissioned to audit NovaCred's raw credit application dataset and evaluate whether its credit decision system is **fair**, **legally compliant**, and **built on reliable data**.

Our audit confirmed all three risk areas identified at the outset. The raw dataset contained significant data quality issues that would corrupt model outputs if left uncleaned. A confirmed gender bias was found in loan approval outcomes, with female applicants approved at a rate 15 percentage points below males, a Disparate Impact ratio of 0.77, falling below the legally required 80% threshold. The dataset also held six categories of personally identifiable information (PII) with no consent tracking, no retention policy, and no audit trail, representing violations across GDPR Articles 5, 6, 17, 22, and 30.

**Bottom line: the current model must not be deployed as-is.** This repository documents the full audit, all identified issues, and the governance controls we implemented to bring NovaCred toward compliance.

---

## Project Description

NovaCred is a fintech startup using a machine learning model to make credit approval decisions. Following a regulatory inquiry about possible discrimination, the company must demonstrate that its system is fair, legally compliant, and grounded in high-quality data.

Our task force was assigned to:
- Audit the raw credit application dataset for data quality issues
- Test the loan approval model for evidence of algorithmic bias
- Identify privacy and governance gaps relative to GDPR and the EU AI Act
- Implement concrete controls to remediate the issues found

This project connects to three core governance dimensions:

| Dimension | Question We Answer |
|---|---|
| Data Quality | Is the data reliable enough to base decisions on? |
| Algorithmic Fairness | Does the model treat all applicants equitably? |
| Privacy & Compliance | Is sensitive data handled in accordance with the law? |

---

## Presentation Video

Watch the project video presentation: [https://youtu.be/Q6UyGMLu2bE](https://youtu.be/Q6UyGMLu2bE)

---

## Repository Structure
```
dego-project-team8/
│
├── README.md
│
├── data/
│   ├── raw_credit_applications.json        # Original dataset (502 records)
│   └── cleaned_credit_applications.csv     # Cleaned dataset (500 records)
│
├── notebooks/
│   ├── 01-data-quality.ipynb               # Data quality audit & remediation
│   ├── 02-bias-analysis.ipynb              # Bias detection & fairness analysis
│   └── 03-privacy-demo.ipynb               # PII identification & GDPR controls
│
├── src/
│   ├── __init__.py
│   └── data_loading.py                     # Reusable raw-data loading helper
│
├── presentation/
│   ├── DEGO-project-team8.pdf              # Presentation slides
│   └── DEGO-project-team8-presentationlink.pdf
│
├── docs/
│   └── project_tracking.md                 # Workflow tracking and milestone log
│
└── secrets/
    └── salt.txt                            # ⚠️ Local only — excluded from GitHub

```
---
## Methodology

The audit followed a sequential three-notebook pipeline, where each notebook builds on the output of the previous one.
```
raw_credit_applications.json
        │
        ▼
01-data-quality.ipynb  ──►  cleaned_credit_applications.csv
        │
        ▼
02-bias-analysis.ipynb  ──►  Fairness metrics & statistical tests
        │
        ▼
03-privacy-demo.ipynb  ──►  GDPR-compliant dataset + governance controls
```

Each notebook follows the same internal logic: identify the risk, quantify affected records, apply the remediation, and verify the fix.

---

## Dataset Overview

**Source:** Raw credit application records from NovaCred's MongoDB collection  
**Format:** Nested JSON, flattened to tabular form for analysis  
**Size:** 502 records (500 after deduplication)  
**Sensitive fields:** SSN flagged as PII from the outset

The dataset is structured across four categories:

| Category | Fields |
|---|---|
| Applicant Info | Full Name, Email, SSN, Gender, Date of Birth, ZIP Code, IP Address |
| Financial Data | Annual Income, Debt-to-Income Ratio, Credit History (months), Savings Balance |
| Spending Behavior | Category + Amount (array of objects per applicant) |
| Loan Decision | Loan Approved, Approved Amount, Interest Rate, Rejection Reason |

> SSN is a direct identifier and the highest-risk PII field in the dataset. `loan_purpose` and `processing_timestamp` are present in only a subset of records.

## Data Quality Findings

**Notebook:** `01-data-quality.ipynb`  
**Input:** `raw_credit_applications.json`  
**Output:** `cleaned_credit_applications.csv`  
**Result:** 502 → 500 records (99.6% retention), 35 columns

We audited nine data quality issue categories across six standard quality dimensions:

| # | Issue | Dimension | Records Affected | Action Taken |
|---|---|---|---|---|
| 1 | Duplicate application IDs | Uniqueness | 4 rows sharing 2 IDs (0.8%) | Removed 2 duplicates, kept first occurrence |
| 2 | Missing values in critical fields | Completeness | 12 records (2.4%) | Flagged; not dropped |
| 3 | Invalid values (negative credit history, malformed emails) | Validity | 2 negative credit history (0.4%), 4 malformed emails (0.8%) | Set to NaN |
| 4 | Inconsistent gender encoding | Consistency | 4 variants (Male/M/Female/F + 2 blanks) | Standardised to Male/Female |
| 5 | Inconsistent date formats | Consistency | 11.2% unrecognised formats, 4 unparseable (0.8%) | Parsed and normalised |
| 6 | Out-of-range numeric values | Validity | 1 DTI > 1, 1 negative savings, 1 zero income, 2 income outliers > 3σ | Impossible values set to NaN; outliers retained |
| 7 | Nested spending_behavior field | Consistency | All 500 records | Exploded to 15 flat spending columns |
| 8 | Redundant income field | Consistency | 5 records used `annual_salary` instead of `annual_income` | Merged into `annual_income` |
| 9 | Wrong data types across columns | Consistency | 34 of 35 columns had wrong dtype | Cast to schema-defined types |

---
## Bias Detection & Fairness

**Notebook:** `02-bias-analysis.ipynb`  
**Input:** `cleaned_credit_applications.csv`

### Gender Bias — Confirmed

| Group | Approval Rate |
|---|---|
| Male | 66% |
| Female | 51% |

- **Disparate Impact Ratio:** 0.77 — below the legally required **80% four-fifths threshold**
- **Demographic parity difference:** -15 percentage points
- **Statistical significance:** logistic regression coefficient = 0.63, p = 0.001
- **Odds ratio:** Male applicants have ~88% higher odds of approval
- **Financial profiles are near-identical:** female mean income $84,010 vs male $81,358; female DTI 0.237 vs male 0.249 — the gap is not explained by financial differences

### Age-Based Approval Patterns

| Age Group | Approval Rate |
|---|---|
| 18–29 | 41% |
| 30–44 | 62% |
| 45–59 | 61% |
| 60+ | 67% |

Applicants under 30 face the lowest approval rate in the dataset. The gender gap persists across all age groups, with women under 30 facing a double disadvantage (30% approval rate).

### Proxy Discrimination — Detected

Two indirect discrimination channels were identified:

- **ZIP code:** Low-approval ZIP codes are **70% female** vs high-approval ZIP codes which are **68% male**, meaning geographic data acts as a gender proxy
- **Gambling spending:** This spending category appears **exclusively in female applicant records** (average $2,449 vs $0 for males) and is likely penalised by the model — a form of indirect discrimination via spending behaviour

### Regulatory Implications

Under the **EU AI Act**, credit scoring is classified as a **High-Risk AI system** (Annex III), requiring bias-free training data, full documentation, and mandatory human oversight. The identified Disparate Impact ratio of 0.77 constitutes a fairness violation that must be remediated before any deployment.

---

## Privacy & Governance Controls

**Notebook:** `03-privacy-demo.ipynb`  
**Input:** `cleaned_credit_applications.csv`

### PII Identified

Seven PII fields were present in the raw dataset:

| Field | PII Type | Risk Level |
|---|---|---|
| `full_name` | Direct identifier | High |
| `email` | Direct identifier | High |
| `ssn` | Sensitive identifier | Critical |
| `ip_address` | Quasi-identifier | Medium |
| `date_of_birth` | Quasi-identifier | Medium |
| `zip_code` | Quasi-identifier | Low |
| `gender` | Quasi-identifier | Medium |

### Controls Implemented

| Control | GDPR Article | EU AI Act Article | Implementation |
|---|---|---|---|
| Pseudonymization of Name, Email, SSN | Art. 5, 25, 32 | — | SHA-256 hashing with secret salt |
| Anonymization of ZIP, DOB, Gender & IP | Art. 5 | — | ZIP → first 3 digits + **, DOB → birth year only, Gender → *, IP → last octet masked |
| Sensitive & proxy spending columns removed | Art. 6, 9 | — | Processed under contractual necessity; Healthcare, Adult Entertainment, Gambling, Gender dropped |
| Retention policy implemented | Art. 5 | — | 7-year retention from request date; 247 overdue records routed to human review queue for deletion |
| Right-to-erasure workflow | Art. 17 | — | PII fields set to NaN on request; anonymized decision data retained for fairness auditing |
| Audit trail logging | Art. 30 | Art. 12 | Automated event log with 9 event codes covering full application lifecycle |
| Human-in-the-Loop architecture | Art. 22 | Art. 14 | AI now advisory only; final decision made by human operator |

### Governance Gaps Found (Pre-Controls)

The raw dataset had **no** consent tracking, **no** retention policy, **no** audit trail, and **no** human oversight — all four represent violations under GDPR and EU AI Act requirements for High-Risk systems.

---
## Remediation Summary

| Area | Issue Found | Remediation Applied | Governance Implication |
|---|---|---|---|
| Data Quality | 9 categories of issues including duplicates, invalid values, inconsistent formats, wrong dtypes | Removed duplicates, standardised encodings, set impossible values to NaN, cast all columns to correct types | Produces a cleaner analytical base and a more auditable pipeline |
| Bias & Fairness | Gender DI = 0.77, strongest harm for women under 30, ZIP and gambling spending act as proxies | Quantified all disparities with statistical tests and logistic regression; proxy variables identified for removal | Supports feature review, subgroup monitoring, and fairness controls before deployment |
| Privacy & GDPR | Direct identifiers present, no consent tracking, no retention policy, no audit trail, no human oversight | Demonstrated SHA-256 pseudonymization, mapped all GDPR gaps, implemented consent, retention, erasure, and HITL architecture | Shows the system is not deployment-ready without legal and procedural safeguards |

---

## Key Findings & Conclusions

| Area | Finding |
|---|---|
| **Data Quality** | Raw dataset had 9 categories of quality issues across 6 dimensions; all remediated in the cleaning pipeline |
| **Gender Bias** | Confirmed — DI ratio of 0.77, below the 80% legal threshold (p = 0.001) |
| **Age Bias** | Applicants under 30 have only 41% approval rate vs 67% for 60+ |
| **Proxy Discrimination** | ZIP code and gambling spending act as indirect gender discrimination channels |
| **GDPR Compliance** | 4 critical gaps found — consent, retention, audit trail, human oversight — all now addressed |
| **EU AI Act** | System classified as High-Risk; obligations require bias-free data, documentation, and HITL oversight |

> **The current model must not be deployed as-is.** Before any production release, NovaCred must resolve the bias in its training data, remove proxy variables, and complete full regulatory documentation.

---

## Recommendations

1. **Remove proxy variables** — Exclude ZIP code and gambling spending from the model's feature set before retraining
2. **Retrain on clean, balanced data** — Use the cleaned dataset from `01-data-quality.ipynb` and apply bias-aware training techniques
3. **Deploy the Human-in-the-Loop architecture** — The AI should function as an advisory tool only; all final credit decisions must be made and logged by a human operator
4. **Complete GDPR documentation** — Implement the retention policy, audit trail, and right-to-erasure pipeline
5. **Conduct a full post-remediation fairness audit** — After retraining, rerun the bias analysis to verify the Disparate Impact ratio has risen above 0.80
6. **Establish ongoing monitoring** — Fairness metrics, data quality checks, and governance controls should be audited regularly, not just at launch

---

## How to Run

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn scipy statsmodels
```

### Execution Order

Run notebooks strictly in sequence, as each depends on the output of the previous:
```bash
# Step 1 – Data Quality
jupyter notebook notebooks/01-data-quality.ipynb

# Step 2 – Bias Analysis
jupyter notebook notebooks/02-bias-analysis.ipynb

# Step 3 – Privacy & Governance
jupyter notebook notebooks/03-privacy-demo.ipynb
```

> The raw dataset must be placed at `data/raw_credit_applications.json` before running notebook 1. All subsequent notebooks load from `data/cleaned_credit_applications.csv`.  
> A `secrets/salt.txt` file is required for notebook 3. Contact the team to obtain it.

---

## Individual Contributions

> Note: Git commit counts do not fully reflect the distribution of project work. Commit frequency is influenced by workflow style and does not capture research, analysis, writing, or coordination efforts. All four team members contributed equally to the overall project.

| Name | Student ID | Role | Key Contributions |
|---|---|---|---|
| Michael Schneider | 71871 | Data Engineer | Data loading, JSON flattening, quality analysis, cleaning pipeline, dataset export |
| Matteo De Francesco | 71734 | Data Scientist | Bias metrics, logistic regression, proxy analysis, age × gender interaction, visualisations |
| Ruben Vetter | 70844 | Governance Officer | PII classification, pseudonymization, GDPR mapping, EU AI Act classification, privacy notebook |
| Malin Busch | 70145 | Product Lead | Presentation, coordination, repository management, README, project tracking, PR reviews |