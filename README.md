# Multi-Asset Portfolio Risk Analytics Platform

A self-contained Python project demonstrating a multi-asset market-risk workflow: risk measurement, model comparison, P&L explain, risk attribution, stress testing and limit monitoring.

## Run

```bash
python -m pip install -r requirements.txt
jupyter notebook notebooks/portfolio_risk_showcase.ipynb
```

Start with `notebooks/portfolio_risk_showcase.ipynb` for the complete workflow, then use `notebooks/risk_methods_testing.ipynb` for focused examples of the new analytical methods. Both use deterministic synthetic returns, so they run without external market-data access. Assumptions, weights and limits are simple dictionaries in `src/portfolio_risk/config.py`.
