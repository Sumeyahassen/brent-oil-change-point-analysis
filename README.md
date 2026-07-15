# brent-oil-change-point-analysis
# Brent Oil Change Point Analysis

Bayesian change point analysis of Brent crude oil prices (May 1987 – Sept 2022), linking
detected structural breaks in the price series to major geopolitical, economic, and OPEC
policy events. Built for **Birhan Energies** to support investors, policymakers, and energy
companies with data-driven insight into oil market volatility.

## Project Structure
brent-oil-change-point-analysis/
├── .vscode/                  # editor settings
├── .github/workflows/        # CI/CD (unittests.yml)
├── docs/                     # Task 1 planning document, events dataset
│   ├── Task1_Analysis_Plan.docx
│   └── events.csv
├── notebooks/                # Jupyter notebooks (EDA, change point modeling)
│   └── eda_analysis.ipynb
├── scripts/                  # standalone analysis scripts
│   └── analyze_events.py
├── src/                      # shared/reusable source code
├── backend/                  # Flask API + PyMC change point model
│   ├── app.py
│   ├── routes/
│   ├── services/
│   ├── analysis/
│   │   ├── analyze_prices.py
│   │   └── changepoint_model.py
│   ├── data/
│   └── outputs/
├── frontend/                 # React dashboard (Task 3)
├── tests/                    # unit tests
├── requirements.txt
└── README.md
## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Data

Place the instructor-provided `BrentOilPrices.csv` at `backend/data/BrentOilPrices.csv`.
It is intentionally excluded from version control (see `.gitignore`) due to its size.
The compiled events dataset (`docs/events.csv`) IS tracked, since it is a required
Task 1 deliverable.

## Running the Analysis

**Exploratory Data Analysis (Task 1):**
```bash
cd backend
python3 analysis/analyze_prices.py
```
Outputs (trend, log returns, volatility, stationarity report) save to `backend/outputs/`.

**Bayesian Change Point Model (Task 2):**
```bash
cd backend
python3 analysis/changepoint_model.py
```
Outputs (posterior plots, convergence diagnostics, `change_points.json`) save to `backend/outputs/` and `backend/data/`.

**Notebook version:** open `notebooks/eda_analysis.ipynb` for an interactive walkthrough.

## Backend API (Task 3)

```bash
cd backend
python3 app.py
```
Serves:
- `GET /api/prices` — historical Brent prices (supports `?start_date` & `?end_date`)
- `GET /api/events` — compiled key events dataset
- `GET /api/changepoints` — detected change points from the Bayesian model
## Task 2: Bayesian Change Point Analysis

### Methodology

A Bayesian change point model was built in PyMC to detect structural
breaks in Brent oil log returns:

- **tau**: discrete uniform prior over all day indices in the series
- **mu1, mu2**: "before" and "after" mean log-return parameters
- **pm.math.switch**: selects mu1 or mu2 depending on whether the day
  index is before or after tau
- **Likelihood**: Normal distribution connecting the switch function to
  observed log returns
- **Sampling**: MCMC via `pm.sample()` (NUTS for mu1/mu2/sigma, Metropolis
  for the discrete tau), with convergence checked via `r_hat` and trace
  plots

### Two analysis approaches

**1. Full 35-year series (1987–2022).** Produced a technically convergent
but highly diffuse posterior for tau (std ≈ 3,000 days), reflecting the
presence of multiple real structural breaks across the full history that
a single-change-point model cannot individually resolve. Documented as a
limitation rather than a standalone finding.

**2. Focused event windows.** The same model applied to shorter windows
bracketing specific researched events produced sharp, high-confidence
change points:

| Event Window | Detected Change Point | Nearest Event | Days from Event | Price Shift | % Change |
|---|---|---|---|---|---|
| COVID-19 (2019–2020) | 2020-04-22 | COVID-19 Demand Collapse (2020-04-20) | 2 | $23.90 → $27.35 | +14.44% |
| OPEC decision (2014–2015) | 2015-01-16 | OPEC Refuses Production Cut (2014-11-27) | 50 | $57.25 → $54.30 | -5.16% |

### How to run

```bash
cd backend
python3 analysis/changepoint_model.py
```

Or interactively via the notebook:
```bash
cd notebooks
jupyter notebook changepoint_analysis.ipynb
```

### Outputs

Saved to `backend/outputs/`:
- `trace_plot_covid_window.png` / `posterior_means_covid_window.png`
- `posterior_tau*.png` — change point posterior distributions
- `model_summary*.txt` — convergence diagnostics (r_hat, ESS)

Saved to `backend/data/`:
- `change_points.json` — machine-readable results consumed by the Task 3
  dashboard API (`GET /api/changepoints`)

### Key limitation

Change point detection identifies **statistical association in time**,
not proven causation. See `docs/Task1_Analysis_Plan.docx` (Section 4.3)
for a full discussion of the distinction, and the notebook's "Future Work"
section for how multi-change-point or Markov-Switching models could
address the full-series limitation.

## Frontend Dashboard (Task 3)

```bash
cd frontend
npm install
npm run dev
```
## Task 3: Interactive Dashboard

### Overview

A full-stack dashboard (Flask backend + React frontend) that lets stakeholders
explore how major geopolitical, economic, and OPEC policy events correlate
with Brent oil price movements, and view the Bayesian change points detected
in Task 2.

### Architecture
### Backend API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API info and list of available endpoints |
| GET | `/api/prices` | Historical Brent prices. Optional `?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` |
| GET | `/api/events` | Compiled dataset of 15 key oil market events |
| GET | `/api/changepoints` | Bayesian-detected change points with quantified impact |
| GET | `/api/events/correlation` | Per-event price shift and volatility. Optional `?window=N` (days, default 30) |
| GET | `/api/stats` | Overall dataset performance metrics (avg/min/max price, volatility, etc.) |

### Frontend Features

- **Interactive price chart** (Recharts) spanning the full 1987–2022 series
- **Event highlight lines** color-coded by category (Conflict, Economic, OPEC
  Policy, Sanctions, Geopolitical), overlaid directly on the price chart
- **Change point markers** showing the Bayesian model's detected structural
  breaks (COVID-19, OPEC 2014)
- **Date range filters**, including one-click presets for key crisis periods
  (COVID-19, 2014 OPEC decision, 2008 Financial Crisis)
- **Sortable event correlation table** — click any column header to sort by
  date, event, category, % change, or volatility
- **Drill-down detail modal** — click any event (on the chart or in the
  table) to see full details: price before/after, % change, volatility
- **Summary stat cards** — average price, min/max, highest volatility period
- **Responsive layout** — works on desktop, tablet, and mobile

### Setup

**1. Start the backend:**
```bash
cd backend
source venv/bin/activate
pip install flask flask-cors pandas numpy
python3 app.py
```
Runs on `http://127.0.0.1:5000`.

**2. Start the frontend** (in a separate terminal):
```bash
cd frontend
npm install
npm run dev
```
Runs on `http://localhost:5173` (or the port Vite reports).

**3. Open the frontend URL in your browser.** The dashboard automatically
fetches all data from the Flask backend on load.

### Tech Stack

- **Backend:** Flask, Flask-CORS, pandas, NumPy
- **Frontend:** React, Vite, Tailwind CSS v3, Recharts, Axios

### Screenshots


## Testing

```bash
pytest tests/ --verbose
```

Tests run automatically on every push via GitHub Actions (`.github/workflows/unittests.yml`)
on the `main`, `task-1`, `task-2`, and `task-3` branches.

## Methodology Summary

1. Load and clean daily Brent price data; compute log returns for stationarity.
2. Test stationarity (Augmented Dickey-Fuller), trend, and volatility clustering.
3. Compile 15 major oil market events (conflicts, sanctions, OPEC decisions, economic shocks).
4. Fit a Bayesian change point model in PyMC (discrete uniform prior on the switch point,
   before/after mean parameters, Normal likelihood).
5. Interpret the posterior distribution of the change point and quantify the price/return
   shift, cross-referencing against the compiled events dataset.
6. Present results via an interactive Flask/React dashboard.

See `docs/Task1_Analysis_Plan.docx` for the full analysis plan, assumptions, limitations,
and discussion of correlation vs. causal impact.

## Author

Sumeya — Birhan Energies Data Science Challenge, Week 10.