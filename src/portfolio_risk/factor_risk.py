"""Simple factor-risk model and decomposition, deliberately easy to audit."""

import pandas as pd



def default_factor_exposures(assets):
    """Return illustrative asset-by-factor loadings for a multi-asset book."""
    exposures = pd.DataFrame(
        {
            "Equity Market": [1.00, 0.90, -0.15, 0.35, -0.10, 0.05],
            "Rates": [-0.15, -0.10, 1.00, 0.25, 0.15, 0.05],
            "Credit": [0.10, 0.08, 0.20, 1.00, -0.05, 0.03],
            "USD": [-0.05, -0.08, 0.05, -0.02, 1.00, -0.15],
            "Commodity": [0.03, 0.02, 0.00, 0.05, -0.02, 1.00],
        },
        index=["US_Equity", "Europe_Equity", "US_10Y_Rates", "Investment_Grade_Credit", "EURUSD", "Gold"],
    )
    return exposures.reindex(assets).fillna(0.0)


def portfolio_factor_exposure(weights, exposures):
    """Aggregate factor exposure from asset weights and factor loadings."""
    weights = pd.Series(weights).reindex(exposures.index).fillna(0.0)
    return (exposures.T @ weights).rename("portfolio_exposure")


def factor_pnl_attribution(weights, exposures, factor_returns):
    """Approximate portfolio factor P&L contributions over time."""
    factor_exposure = portfolio_factor_exposure(weights, exposures)
    return factor_returns.mul(factor_exposure.reindex(factor_returns.columns), axis=1)
