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

## Frontend Dashboard (Task 3)

```bash
cd frontend
npm install
npm run dev
```

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