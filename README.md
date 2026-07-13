# Multi-Asset Portfolio Risk Analytics Platform

A self-contained Python portfolio project demonstrating core market-risk, portfolio-risk and quantitative-risk workflows: multi-asset market data, risk metrics, factor exposure, stress testing and risk-limit monitoring.

## Run

```bash
python -m pip install -r requirements.txt
jupyter notebook notebooks/portfolio_risk_showcase.ipynb
```

The notebook adds `src/` to its import path and runs without external market-data access. Assumptions, weights and limits are simple dictionaries in `src/portfolio_risk/config.py`, so they are straightforward to change.