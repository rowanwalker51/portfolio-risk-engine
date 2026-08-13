"""Transparent hypothetical stress testing for a multi-asset portfolio."""

import pandas as pd



def default_scenarios() -> pd.DataFrame:
    """Market moves expressed as one-period returns, by asset."""
    return pd.DataFrame(
        {
            "Equity risk-off": [-0.12, -0.10, 0.015, -0.035, 0.025, 0.04],
            "Rates shock": [-0.04, -0.03, -0.06, -0.025, 0.01, -0.02],
            "Credit widening": [-0.06, -0.05, 0.01, -0.08, 0.005, 0.01],
            "USD spike": [-0.02, -0.03, 0.005, -0.01, 0.07, -0.015],
        },
        index=["US_Equity", "Europe_Equity", "US_10Y_Rates", "Investment_Grade_Credit", "EURUSD", "Gold"],
    )


def run_stress_tests(weights, scenarios):
    """Calculate asset-level and total P&L for every stress scenario."""
    weights = pd.Series(weights)
    shocks = scenarios.reindex(weights.index).fillna(0.0)
    contributions = shocks.mul(weights, axis=0)
    result = contributions.T
    result["Total"] = result.sum(axis=1)
    return result.sort_values("Total")
