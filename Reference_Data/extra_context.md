# Project Context: PSEO Market Analysis Dashboard
**Principal Investigator:** Anubhav Dhungana (CS & Economics, Texas State University)
**Project Goal:** Academic research for the McCoy College of Business Symposium analyzing market failure and wage stagnation in the U.S. teacher labor market compared to STEM fields.

---

## 1. Technical Environment & UI/UX Standards
* **Platform:** Streamlit (Web Dashboard), Plotly (Visualizations), Statsmodels (Econometrics).
* **IDE Context:** Developed in Antigravity IDE.
* **Design Philosophy:** * **Dark Theme:** Background `#0e0e0e`, Text `#e8e8e8`, Accent Cyan `#00d4ff`.
    * **Layout:** Wide mode, initial sidebar collapsed.
    * **Filtering:** **NO GLOBAL SIDEBAR.** Each visualization must have its own "Local Filter Bar" (using `st.columns`).
    * **Typography:** High-fidelity, clean, professional (IBM Plex Sans).

---

## 2. Repository Architecture & Token Management
**CRITICAL: TOKEN SAFETY PROTOCOL**
To avoid immediate token exhaustion, the following folders contain high-volume CSVs. **DO NOT** read or load full files from these directories unless a specific subset is requested:
* `Foundational_Data/` (Raw Census dumps)
* `Usage_Data/` (Large processed datasets)
* `Intermediary_Cleaned/` (Middle-state cleanup files)

**Safe Directories for Context:**
* `Cleaning_Notebooks/`: Contains the logic for data extraction and transformation.
* `Labels/`: Small CSVs for mapping codes (CIP, FIPS, Geography) to human-readable names.
* `Regression/`: Contains exported coefficients and HTML appendix tables.

---

## 3. Data Domain Knowledge (PSEO)
* **Dataset:** Post-Secondary Employment Outcomes (PSEO) from the U.S. Census Bureau.
* **Aggregation Levels:**
    * **Level 34:** Degree x CIP-2 x Cohort x State (Used for Earnings Regressions).
    * **Level 178:** Degree x CIP-2 x Cohort x State x Industry x Census Division (Used for Flow/Sankey).
* **Key Variables:**
    * `cipcode`: 2-digit major codes. (01: Agriculture, 11: CS, 13: Education, 51: Nursing).
    * **Baseline:** All regression models use **CIP 01 (Agriculture)** as the reference group.
    * `y1/y5/y10_p50_earnings`: Median earnings 1, 5, and 10 years after graduation.
    * `y1/y5/y10_grads_emp_instate`: Count of graduates working in their home state.

---

## 4. Current Progress & Engineering Roadmap

### A. Econometrics (Completed)
* Executed 9 OLS regressions (3 years x 3 percentiles).
* Implemented **Fixed Effects (areg logic)** by "absorbing" variation through a combined `state_year` (Vortex) variable.
* Confirmed statistically significant stagnation in Education ($p > 0.05$ for premiums) vs. significant growth in CS/Nursing.

### B. Dashboard State
* **Tab 1 (Flow):** Double Sankey visualization. *Current Goal:* Implement 3-way toggle (Industry, Division, Both) and unmask "In-State" graduates.
* **Tab 2 (Geographic):** Heatmaps and state-level comparisons.
* **Tab 3 (Economic Returns):** Regression visualizer showing the "Scissors Effect" (Divergence of premiums over time).

---

## 5. Specific Implementation Style
* **Pandas:** Prefer vectorized operations over loops. Use `.copy()` on slices to avoid `SettingWithCopy` warnings.
* **Plotly:** Use `plotly_dark` template. Transparent backgrounds (`paper_bgcolor='rgba(0,0,0,0)'`).
* **Cleanliness:** Always include docstrings or brief comments explaining the "Econ Logic" behind the code (e.g., why we are controlling for a specific variable).
* **Sankey Logic:** When visualizing flows, the "In-State" node must be explicitly labeled as `{State Name} (In-State)` to distinguish it from the rest of the Census Division.

---

## 6. Goal Alignment
The agent must focus on **academic rigor**. Every visualization or piece of code should be designed to support the thesis that the teacher shortage is a rational economic response to structural wage stagnation. The dashboard is not just a tool; it is a proof-of-concept for a future PhD research agenda.

***

**Instruction to Agent:** Use this context to inform all code generation and analysis. If a task violates the token safety protocol in Section 2, alert the user before proceeding.