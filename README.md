# DEGO Project - Team 8
## Team Members
- Ruben Vetter 70844
- Malin Busch 70145
- Michael Schneider 71871
- Matteo De Francesco 71734
## Project Description
Credit scoring bias analysis for DEGO course.
## Structure
- ‘data/‘ - Dataset files
- ‘notebooks/‘ - Jupyter analysis notebooks
- ‘src/‘ - Python source code
- ‘reports/‘ - Final deliverables

## Executive Summary

NovaCred, a fintech company using machine learning to automate loan approval decisions, received a regulatory inquiry regarding potential discrimination in its lending practices. As an external Data Governance Task Force, we were commissioned to audit NovaCred's raw credit application dataset and evaluate whether its credit decision system is **fair**, **legally compliant**, and **built on reliable data**.

Our audit confirmed all three risk areas identified at the outset. The raw dataset contained significant data quality issues that would corrupt model outputs if left uncleaned. A confirmed gender bias was found in loan approval outcomes, with female applicants approved at a rate 15 percentage points below males — a Disparate Impact ratio of 0.77, falling below the legally required 80% threshold. The dataset also held six categories of personally identifiable information (PII) with no consent tracking, no retention policy, and no audit trail — representing violations across GDPR Articles 5, 6, 17, 22, and 30.

**Bottom line: the current model must not be deployed as-is.** This repository documents the full audit, all identified issues, and the governance controls we implemented to bring NovaCred toward compliance.

---

## Table of Contents

- [DEGO Project - Team 8](#dego-project---team-8)
  - [Team Members](#team-members)
  - [Project Description](#project-description)
  - [Structure](#structure)
  - [Executive Summary](#executive-summary)
  - [Table of Contents](#table-of-contents)
  - [1. Project Context \& Mission](#1-project-context--mission)
  - [2. Dataset Overview](#2-dataset-overview)
  - [3. Repository Structure](#3-repository-structure)
  - [4. Methodology](#4-methodology)
  - [5. Data Quality Analysis](#5-data-quality-analysis)
  - [6. Bias Analysis](#6-bias-analysis)
    - [Gender Bias — Confirmed](#gender-bias--confirmed)
    - [Proxy Discrimination — Detected](#proxy-discrimination--detected)
    - [Regulatory Implications](#regulatory-implications)
  - [7. Privacy \& Governance Controls](#7-privacy--governance-controls)
    - [PII Identified](#pii-identified)
    - [Controls Implemented](#controls-implemented)
    - [Governance Gaps Found (Pre-Controls)](#governance-gaps-found-pre-controls)
  - [8. Key Findings \& Conclusions](#8-key-findings--conclusions)
  - [9. Recommendations](#9-recommendations)
  - [10. How to Run](#10-how-to-run)
    - [Requirements](#requirements)
    - [Execution Order](#execution-order)
  - [11. Team](#11-team)

---

## 1. Project Context & Mission

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

## 2. Dataset Overview

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

> ⚠️ SSN is a direct identifier and the highest-risk PII field in the dataset. `loan_purpose` and `processing_timestamp` are present in only a subset of records.

---

## 3. Repository Structure

```
dego-project-team8/
│
├── data/
│   ├── raw_credit_applications.json          # Original dataset (not modified)
│   └── cleaned_credit_applications.csv       # Output of data quality pipeline
│
├── notebooks/
│   ├── 01-data-quality.ipynb                 # Data cleaning & quality audit
│   ├── 02-bias-analysis.ipynb                # Fairness metrics & bias testing
│   └── 03-privacy-demo.ipynb                 # GDPR controls & EU AI Act mapping
│
├── reports/
│   └── [presentation slides]
│
├── presentation/
│   └── [video presentation]
│
└── README.md
```

---

## 4. Methodology

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

## 5. Data Quality Analysis

**Notebook:** `01-data-quality.ipynb`  
**Input:** `raw_credit_applications.json`  
**Output:** `cleaned_credit_applications.csv`

We audited nine data quality issue categories across six standard quality dimensions (Accuracy, Completeness, Consistency, Timeliness, Validity, Uniqueness):

| # | Issue | Dimension | Records Affected | Action Taken |
|---|---|---|---|---|
| 1 | Duplicate records | Uniqueness | 2 duplicates removed | Kept first occurrence |
| 2 | Missing values in critical fields | Completeness | 5 records (1.0%) | Flagged; not dropped |
| 3 | Invalid values (malformed emails, future DOB, negative credit history) | Validity | 11 malformed emails (2.2%) | Set to NaN |
| 4 | Inconsistent gender encoding | Consistency | 4 variants (Male/M/Female/F + blanks) | Standardised to Male/Female |
| 5 | Inconsistent date formats | Consistency | 12% unrecognised formats | Parsed and normalised |
| 6 | Out-of-range numeric values | Validity | DTI > 1, negative savings, zero income | Impossible values set to NaN |
| 7 | Nested spending_behavior field | Consistency | All records | Exploded to flat spending columns |
| 8 | Redundant income field | Consistency | 5 records used `annual_salary` vs `annual_income` | Consolidated into `annual_income` |
| 9 | Wrong data types | Consistency | 97.1% of columns had wrong dtype | Cast to schema-defined types |

> All fixes are applied sequentially and carried forward in `df_clean`, which is exported to `cleaned_credit_applications.csv` for use in subsequent notebooks.

---

## 6. Bias Analysis

**Notebook:** `02-bias-analysis.ipynb`  
**Input:** `cleaned_credit_applications.csv`

### Gender Bias — Confirmed

| Group | Approval Rate |
|---|---|
| Male | 66% |
| Female | 51% |

- **Disparate Impact Ratio:** 0.77 — below the legally required **80% threshold**
- **Statistical significance:** p < 0.001
- **Odds ratio:** Male applicants have ~88% higher odds of approval

### Proxy Discrimination — Detected

Two indirect discrimination channels were identified:

- **ZIP code:** Low-approval ZIP codes are **70% female**, suggesting geographic data acts as a gender proxy
- **Gambling spending:** This category appears exclusively in female applicant records and is likely penalised by the model — a form of indirect discrimination via spending behaviour

### Regulatory Implications

Under the **EU AI Act**, credit scoring is classified as a **High-Risk AI system**, requiring bias-free training data, full documentation, and mandatory human oversight. The identified Disparate Impact ratio of 0.77 constitutes a fairness violation that must be remediated before any deployment.

---

## 7. Privacy & Governance Controls

**Notebook:** `03-privacy-demo.ipynb`  
**Input:** `cleaned_credit_applications.csv`

### PII Identified

Six PII fields were present in the raw dataset: `full_name`, `email`, `SSN`, `IP address`, `date_of_birth`, `ZIP code`.

### Controls Implemented

| Control | GDPR Article | EU AI Act Article | Implementation |
|---|---|---|---|
| Pseudonymization of Name, Email, SSN | Art. 5, 25 | — | SHA-256 hashing with secret salt |
| Anonymization of ZIP code & DOB | Art. 5 | — | ZIP truncated to 3 digits; DOB reduced to year only |
| IP address removed | Art. 5 (Data Minimization) | — | Column dropped entirely |
| Sensitive spending columns removed | Art. 9 | — | Gambling, Alcohol, Adult Entertainment dropped |
| Proxy variables removed | Art. 5 | Art. 10 | Fitness, Healthcare, Education spending dropped |
| Consent tracking added | Art. 6, 7 | — | `spending_consent` field; 95% opt-in rate |
| Retention policy implemented | Art. 5 | — | 5-year tier (rejected), 10-year tier (approved) |
| Right-to-erasure workflow | Art. 17 | — | Automated purge pipeline demonstrated |
| Audit trail logging | Art. 30 | Art. 12 | Timestamped event log with 9 defined event codes |
| Human-in-the-Loop architecture | Art. 22 | Art. 14 | AI now advisory only; final decision made by human operator |

### Governance Gaps Found (Pre-Controls)

The raw dataset had **no** consent tracking, **no** retention policy, **no** audit trail, and **no** human oversight — all four represent violations under GDPR and EU AI Act requirements for High-Risk systems.

---

## 8. Key Findings & Conclusions

| Area | Finding |
|---|---|
| **Data Quality** | Raw dataset had 9 categories of quality issues; all remediated in the cleaning pipeline |
| **Gender Bias** | Confirmed — DI ratio of 0.77, below the 80% legal threshold (p < 0.001) |
| **Proxy Discrimination** | ZIP code and gambling spending act as indirect gender discrimination channels |
| **GDPR Compliance** | 4 critical gaps found — consent, retention, audit trail, human oversight — all now addressed |
| **EU AI Act** | System classified as High-Risk; obligations require bias-free data, documentation, and HITL oversight |

> **The current model must not be deployed as-is.** Before any production release, NovaCred must resolve the bias in its training data, remove proxy variables, and complete full regulatory documentation.

---

## 9. Recommendations

1. **Remove proxy variables** — Exclude ZIP code, gambling spending, fitness, healthcare, and education spending from the model's feature set before retraining
2. **Retrain on clean, balanced data** — Use the cleaned dataset from `01-data-quality.ipynb` and apply bias-aware training techniques
3. **Deploy the Human-in-the-Loop architecture** — The AI should function as an advisory tool only; all final credit decisions must be made and logged by a human operator
4. **Complete GDPR documentation** — Implement the consent, retention, and audit trail infrastructure designed in `03-privacy-demo.ipynb` in production
5. **Conduct a full post-remediation fairness audit** — After retraining, rerun the bias analysis to verify the Disparate Impact ratio has risen above 0.80
6. **Establish ongoing monitoring** — Fairness metrics, data quality checks, and governance controls should be audited regularly, not just at launch

---

## 10. How to Run

### Requirements

```bash
pip install pandas numpy matplotlib seaborn scipy hashlib uuid
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

---

## 11. Team

| Name | Student ID | Role |
|---|---|---|
| Michael Schneider | 71871 | Data Engineer — data loading, cleaning pipeline, notebook 01 |
| Matteo De Francesco | 71734 | Data Scientist — bias metrics, statistical testing, notebook 02 |
| Ruben Vetter | 70844 | Governance Officer — GDPR mapping, policy recommendations, notebook 03 |
| Malin Busch | 70145 | Product Lead — presentation, coordination, repository documentation |

---

*Nova School of Business & Economics — DEGO Course — Group 8 — 2025/26 T3*
