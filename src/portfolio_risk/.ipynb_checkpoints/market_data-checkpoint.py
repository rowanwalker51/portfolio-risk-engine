"""Synthetic but realistic market data with validation utilities."""

import numpy as np
import pandas as pd

from .config import PERIODS, RANDOM_SEED, WEIGHTS


def generate_market_data(periods=PERIODS, seed=RANDOM_SEED, assets=None):
    """Generate correlated daily returns with a small stressed period.

    The deterministic seed makes the demonstration reproducible.  In production,
    this function can be replaced by a market-data adapter without changing the
    downstream risk analytics.
    """
    rng = np.random.default_rng(seed)
    assets = list(WEIGHTS) if assets is None else assets
    daily_vol = np.array([0.012, 0.013, 0.005, 0.006, 0.007, 0.010])
    daily_mean = np.array([0.00035, 0.00025, 0.00010, 0.00016, 0.00005, 0.00012])
    correlation = np.array(
        [
            [1.00, 0.78, -0.25, 0.42, -0.18, 0.08],
            [0.78, 1.00, -0.20, 0.38, -0.12, 0.10],
            [-0.25, -0.20, 1.00, 0.30, 0.22, 0.05],
            [0.42, 0.38, 0.30, 1.00, -0.08, 0.14],
            [-0.18, -0.12, 0.22, -0.08, 1.00, -0.12],
            [0.08, 0.10, 0.05, 0.14, -0.12, 1.00],
        ]
    )
    covariance = np.outer(daily_vol, daily_vol) * correlation
    returns = rng.multivariate_normal(daily_mean, covariance, size=periods)

    # A concise, reproducible risk-off episode makes stress and monitoring useful.
    stress_start = periods // 2
    stress = np.array([-0.025, -0.022, 0.004, -0.011, 0.009, 0.006])
    returns[stress_start : stress_start + 4] += stress

    index = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=periods)
    return validate_returns(pd.DataFrame(returns, index=index, columns=assets))


def validate_returns(returns):
    """Return a clean copy of a return matrix or raise a useful error."""
    if returns.empty:
        raise ValueError("Returns data must contain at least one row.")
    if returns.isna().any().any():
        raise ValueError("Returns data contains missing values.")
    if not np.isfinite(returns.to_numpy()).all():
        raise ValueError("Returns data contains non-finite values.")
    if not isinstance(returns.index, pd.DatetimeIndex):
        raise TypeError("Returns data must use a DatetimeIndex.")
    return returns.sort_index().copy()
