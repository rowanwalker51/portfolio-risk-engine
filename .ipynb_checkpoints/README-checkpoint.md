# Multi-Asset Portfolio Risk Analytics Platform

A self-contained Python portfolio project demonstrating core market-risk, portfolio-risk and quantitative-risk workflows: multi-asset market data, risk metrics, factor exposure, stress testing and risk-limit monitoring.

## Run

```bash
python -m pip install -r requirements.txt
jupyter notebook notebooks/portfolio_risk_showcase.ipynb
```

The notebook adds `src/` to its import path and runs without external market-data access. All synthetic data is deterministic, making the results reproducible.

## CV description

Built a Python-based multi-asset portfolio risk analytics platform covering historical VaR/Expected Shortfall, factor and contribution-to-risk analysis, stress testing, and automated risk-limit monitoring; communicated findings through a reproducible risk-reporting notebook.
