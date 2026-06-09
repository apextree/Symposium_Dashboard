# PSEO Earnings Dashboard

An interactive Streamlit dashboard exploring **post-graduation earnings** for **Computer Science, Education, and Health Professions** majors, built on the U.S. Census Bureau's [Post-Secondary Employment Outcomes (PSEO)](https://lehd.ces.census.gov/data/pseo_experimental.html) data.

> **Research question:** What are the 1-, 5-, and 10-year post-graduation average salaries for Computer Science, Education, and Healthcare majors?

## Features

- **Earnings** — Earnings distributions, trajectories across post-graduation years, and breakdowns by graduation cohort, filterable by state and CIP code.
- **Employment Flows** — Sankey diagrams tracing graduates from *Major → Industry → Census Division*.
- **Economic Returns** — OLS regression of earnings premiums relative to a baseline major.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch the dashboard
streamlit run dashboard.py
```

The app opens in your browser at `http://localhost:8501`.

## Project Structure

| Path | Description |
| --- | --- |
| `dashboard.py` | Main Streamlit application |
| `Usage_Data/` | Cleaned datasets consumed by the dashboard |
| `Cleaning_Notebooks/` | Notebooks that extract and clean the raw PSEO data |
| `Regression/` | Regression inputs, coefficients, and output tables |
| `Labels/`, `Reference_Data/` | Lookup tables (FIPS, CIP, industry codes) |

## Data

Source: U.S. Census Bureau PSEO (aggregation levels 34 / 178, degree level 5, CIP 11 / 13 / 51). Data is aggregated and de-identified at the source; some cells may be suppressed for privacy.

## Tech Stack

Python · Streamlit · pandas · Plotly
