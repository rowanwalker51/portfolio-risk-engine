"""Core market-risk measures used by portfolio-risk teams."""

import numpy as np
import pandas as pd

from .portfolio import align_weights


def value_at_risk(returns, confidence=0.95):
    """Positive historical Value at Risk for a one-day loss."""
    return float(-returns.quantile(1 - confidence))


def expected_shortfall(returns, confidence=0.95):
    """Positive historical Expected Shortfall, conditional on a VaR breach."""
    cutoff = returns.quantile(1 - confidence)
    tail = returns[returns <= cutoff]
    return float(-tail.mean())


def annualised_volatility(returns, periods_per_year=252):
    return float(returns.std(ddof=1) * np.sqrt(periods_per_year))


def maximum_drawdown(returns):
    wealth = (1 + returns).cumprod()
    drawdown = wealth / wealth.cummax() - 1
    return float(-drawdown.min())


def rolling_risk_metrics(returns, window=63, confidence=0.95, periods_per_year=252):
    """Rolling volatility, historical VaR and ES for monitoring dashboards."""
    result = pd.DataFrame(index=returns.index)
    result["annualised_volatility"] = returns.rolling(window).std() * np.sqrt(periods_per_year)
    result["var_95"] = -returns.rolling(window).quantile(1 - confidence)
    result["es_95"] = returns.rolling(window).apply(
        lambda sample: expected_shortfall(pd.Series(sample), confidence), raw=False
    )
    return result


def component_var(returns, weights):
    """Euler component VaR under a covariance-normal approximation.

    Components sum to portfolio parametric VaR and make diversification and
    concentration immediately visible to a risk reviewer.
    """
    weights = align_weights(returns, weights)
    covariance = returns.cov()
    portfolio_vol = np.sqrt(weights @ covariance @ weights)
    if portfolio_vol == 0:
        return pd.Series(0.0, index=weights.index, name="component_var")
    z_95 = 1.6448536269514722
    marginal = covariance @ weights / portfolio_vol
    return (z_95 * weights * marginal).rename("component_var")
