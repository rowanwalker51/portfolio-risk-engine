"""Small helpers for combining asset returns into a portfolio."""

import pandas as pd


def align_weights(returns, weights):
    """Check weights and line them up with the return columns."""
    weights = pd.Series(weights, dtype=float)
    missing = weights.index.difference(returns.columns)
    if len(missing):
        raise ValueError(f"Returns are missing: {list(missing)}")
    if round(weights.sum(), 10) != 1.0:
        raise ValueError("Weights must add up to 1.0")
    return weights.reindex(returns.columns).fillna(0.0)


def portfolio_returns(returns, weights):
    """Calculate the daily return of the portfolio."""
    return returns.mul(align_weights(returns, weights), axis=1).sum(axis=1).rename("Portfolio")


def asset_class_exposure(weights, asset_classes):
    """Group portfolio weights into broad asset classes."""
    weights = pd.Series(weights, dtype=float)
    classes = pd.Series(asset_classes).reindex(weights.index)
    return weights.groupby(classes).sum().sort_values(ascending=False).rename("weight")
