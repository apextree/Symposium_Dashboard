# Symposium Dashboard — agent context

This file was written for **other agents** working in this folder. It summarizes what is known from **repository layout, code, and data files**, plus **git/session metadata** from the conversation that requested this document.

**Important:** There was **no separate, substantive prior chat history** about this project in the available agent transcript for this workspace. Anything not backed by files on disk is labeled as inference or external metadata below.

---

## Where this lives in git

- **Git repository root:** `/Users/anubhavdhungana/Desktop/BSc. Computer Science/PSEO_Research` (parent of this folder).
- **`Symposium_Dashboard/`** was reported as **untracked** (`??`) alongside `PSEO_Raw_Data_old/` at the start of the session. Treat this subtree as **not yet committed** unless that has changed.
- **Workspace path (Cursor):** `/Users/anubhavdhungana/Desktop/BSc. Computer Science/PSEO_Research/Symposium_Dashboard`.

---

## Purpose (inferred from code and filenames)

This project supports **PSEO (Post-Secondary Employment Outcomes)** research for a symposium-style presentation. It combines:

1. **A Streamlit dashboard** for interactive charts (earnings + employment flows).
2. **Jupyter notebooks** that extract and clean subsets of PSEO extracts for specific aggregation levels, degree filters, and CIP families.
3. **Reference tables** (labels, variable lists, institution lists) and **large foundational CSV extracts** from Census PSEO products.

The dashboard’s stated research question (in `dashboard.py`) is: **1-, 5-, and 10-year post-graduation average salaries** for **Computer Science (CIP 11), Education (CIP 13), and Healthcare / health professions (CIP 51)**.

---

## How to run the app

From this directory:

```bash
streamlit run dashboard.py
```

(`dashboard.py` documents this in its module docstring.)

### Python environment

- A **local virtualenv** exists at `.venv/` (Python **3.13** was observed in site-packages paths; Streamlit **1.56.0** is installed there).
- There is **no** `requirements.txt` or `pyproject.toml` in the project root at the time of writing. Runtime imports in `dashboard.py` are **`pandas`**, **`plotly.graph_objects`**, and **`streamlit`**.

---

## Main application: `dashboard.py`

Single-file Streamlit app with custom **dark theme** CSS, **sidebar hidden**, wide layout.

### Data sources (hard-coded paths)

| Role | Path |
|------|------|
| Earnings / cohort trends (agg 34) | `Usage_Data/pseo_state_cohort_trends_agg34_deg5_cip11_13_51_clean.csv` |
| Employment flows (agg 178) | `Usage_Data/pseof_agg178_deg5_cip11_13_51_clean.csv` |
| Optional FIPS → state name join | `Labels/label_fipsnum.csv` (used only if `state_name` is missing from the flow file) |

### Tabs and behavior

1. **Earnings**
   - **Figure 1:** grouped bar chart — mean **P25 / P50 / P75** earnings by major for a chosen **post-grad year** (1, 5, 10), with filters for **state** and **graduation cohort** (including “All … Combined”).
   - **Figure 2:** line chart — **earnings trajectory** across 1 / 5 / 10 years for a chosen **percentile**.
   - **Figure 3:** line chart — **earnings by graduation cohort** for selected year milestones and percentile; optional state filter.
   - Footer copy references PSEO / Census and CIP 11 / 13 / 51.

2. **Employment Flows**
   - **Sankey diagram:** **Major → Industry (NAICS sector labels) → Census Division**, plus **NME** (“Not Observed / Marginal”) nodes per major, using employment count columns `y*_grads_emp` and `y*_grads_nme`.
   - Filters: **source state**, **majors** (labels: Computer Science, Education, Health Professions), **cohort**, **time milestone** (1 / 5 / 10 years). Default cohort selection logic picks the **last** cohort in the sorted list when “All Cohorts” is not used (see `index=len(flow_cohorts)`).
   - Suppression / empty states show in-app warning boxes.

### Implementation notes useful for edits

- **CIP mapping** is centralized in dicts like `CIP_MAP`, `CIP_SHORT`, `CIP_LABEL`.
- **Earnings columns** per year live in `YEAR_COLS`; flow employment columns in `FLOW_EMP_COLS` / `FLOW_NME_COLS`.
- **Sankey:** `build_sankey()` deduplicates NME before summing (see comments around `nme_key_cols`).
- **Plotly** layout helpers use a consistent dark palette (`BG_PLOT`, `BG_PAPER`, etc.).

---

## Data pipeline layout (folders)

| Folder | Contents / role |
|--------|------------------|
| `Foundational_Data/` | Very large raw-ish extracts: `pseof_all.csv` (~3 GB class), `pseoe_all.csv`, duplicate `pseoe_all copy.csv`. **Heavy**; avoid accidental full reads in agents. |
| `Intermediary_Cleaned/` | Intermediate filtered CSVs (e.g. agg 46 slices, `pseo_double_sankey_ready.csv`, and precursors to the `Usage_Data` files). |
| `Usage_Data/` | **Dashboard inputs** — cleaned, dashboard-sized CSVs (`*_clean.csv`). |
| `Labels/` | Dimension label tables: `label_fipsnum.csv`, `label_industry.csv`, `label_cipcode.csv`, geo/agg/degree labels, etc. |
| `Identifiers_and_Variables/` | `lehd_identifiers_pseo.csv`, `variables_pseoe.csv`, `pseo_all_institutions.csv` — schema / reference for analysts. |
| `Information_Description/` | `PSEO Data Information.pdf` (methodology / field documentation from Census). |
| `Cleaning_Notebooks/` | Extraction notebooks, e.g. `extract_state_cohort_trends_agg34_deg5.ipynb`, `extract_flow_agg178_deg5.ipynb`, `Extract For Regression.ipynb`; subdirectory `irr_others/` for ancillary notebooks; exported CSV such as `peoe_agg34_regression.csv`. |

---

## PSEO parameters echoed in the project

Consistent labels in the UI and file names point to:

- **Aggregation level 34** for the state–cohort earnings trends file.
- **Aggregation level 178** for the employment flow / Sankey file.
- **Degree level 5** in earnings naming (`deg5`); flow file uses `degree_level` values like `05` in the sample rows (string dtype enforced on read).
- **CIP families 11, 13, 51** throughout.

Agents changing filters or adding majors should keep **column names**, **CIP codes**, and **file paths** in sync across notebooks, `Usage_Data`, and `dashboard.py`.

---

## Miscellaneous files

- `first_10_rows.csv` — small sample snippet at repo root (likely for quick inspection).
- `.DS_Store` — macOS folder metadata (usually should not be committed).
- `.venv/` — local environment; typically **gitignored** in shared repos (currently present on disk).

---

## Gaps / things to verify before assuming

- Whether `Symposium_Dashboard` has been added to git and what `.gitignore` rules apply (especially for `.venv/` and multi-gigabyte CSVs).
- Exact **provenance** of each notebook output (rerun order, filters) if reproducing `Usage_Data` from `Foundational_Data`.
- Whether a **`requirements.txt`** should be added for reproducibility (not present when this document was written).

---

## Changelog of this document

- **2026-04-14:** Initial `full_context.md` created from filesystem inspection of `Symposium_Dashboard` and reading `dashboard.py` plus headers of primary CSV inputs.
