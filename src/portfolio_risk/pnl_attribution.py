"""Simple P&L and risk attribution tables."""

import pandas as pd

from .factor_risk import factor_pnl_attribution
from .portfolio import portfolio_returns
from .risk_metrics import component_var


def asset_pnl_attribution(returns, weights):
    """Daily portfolio P&L split into the six asset contributions."""
    return returns.mul(pd.Series(weights), axis=1)


def factor_pnl_explain(asset_returns, weights, exposures, factor_returns):
    """Explain portfolio P&L as factor P&L plus an unexplained residual."""
    factor_contributions = factor_pnl_attribution(weights, exposures, factor_returns)
    explained = factor_contributions.sum(axis=1).rename("factor_pnl")
    actual = portfolio_returns(asset_returns, weights).rename("actual_pnl")
    result = pd.concat([actual, explained], axis=1)
    result["residual_pnl"] = result["actual_pnl"] - result["factor_pnl"]
    return result, factor_contributions


def risk_attribution(returns, weights):
    """Show each position's weight, component VaR, and share of total VaR."""
    components = component_var(returns, weights)
    result = pd.DataFrame({"weight": pd.Series(weights), "component_var": components})
    result["risk_share"] = result["component_var"] / result["component_var"].sum()
    return result.sort_values("component_var", ascending=False)
