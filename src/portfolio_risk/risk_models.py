"""Comparable one-day VaR and Expected Shortfall models."""

from statistics import NormalDist

import numpy as np
import pandas as pd


NORMAL = NormalDist()


def historical_risk(returns, confidence=0.95):
    """Historical simulation VaR and ES."""
    cutoff = returns.quantile(1 - confidence)
    return -cutoff, -returns[returns <= cutoff].mean()


def normal_risk(returns, confidence=0.95):
    """Normal VaR and ES using the sample mean and volatility."""
    mean = returns.mean()
    volatility = returns.std(ddof=1)
    z_score = NORMAL.inv_cdf(1 - confidence)
    tail_density = NORMAL.pdf(z_score)
    var = -(mean + z_score * volatility)
    es = -mean + volatility * tail_density / (1 - confidence)
    return var, es


def ewma_risk(returns, confidence=0.95, decay=0.94):
    """Normal VaR and ES with RiskMetrics-style EWMA volatility."""
    squared_returns = returns.to_numpy() ** 2
    weights = (1 - decay) * decay ** np.arange(len(returns) - 1, -1, -1)
    volatility = np.sqrt(np.dot(weights, squared_returns))
    z_score = NORMAL.inv_cdf(1 - confidence)
    tail_density = NORMAL.pdf(z_score)
    return -z_score * volatility, volatility * tail_density / (1 - confidence)


def monte_carlo_risk(returns, confidence=0.95, simulations=20_000, seed=7):
    """Normal Monte Carlo VaR and ES fitted to the return history."""
    rng = np.random.default_rng(seed)
    simulated_returns = rng.normal(returns.mean(), returns.std(ddof=1), simulations)
    return historical_risk(pd.Series(simulated_returns), confidence)


def compare_risk_models(returns, confidence=0.95):
    """Place four VaR/ES estimates in one readable comparison table."""
    models = {
        "Historical": historical_risk(returns, confidence),
        "Normal": normal_risk(returns, confidence),
        "EWMA": ewma_risk(returns, confidence),
        "Monte Carlo": monte_carlo_risk(returns, confidence),
    }
    return pd.DataFrame(models, index=["VaR", "Expected shortfall"]).T.rename_axis("model")
