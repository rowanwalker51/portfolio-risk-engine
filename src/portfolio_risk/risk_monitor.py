"""Daily risk monitoring and clear exception reporting."""

import pandas as pd

from .risk_metrics import annualised_volatility, expected_shortfall, maximum_drawdown, value_at_risk


def risk_summary(returns, limits):
    """Create a risk-committee-ready summary with explicit limit status."""
    metrics = {
        "1-day historical VaR (95%)": (value_at_risk(returns), limits["var_95"]),
        "1-day historical ES (95%)": (expected_shortfall(returns), limits["es_95"]),
        "Annualised volatility": (annualised_volatility(returns), limits["annualised_volatility"]),
        "Maximum drawdown": (maximum_drawdown(returns), limits["max_drawdown"]),
    }
    summary = pd.DataFrame.from_dict(metrics, orient="index", columns=["value", "limit"])
    summary["utilisation"] = summary["value"] / summary["limit"]
    summary["status"] = summary["utilisation"].map(lambda x: "BREACH" if x > 1 else "OK")
    return summary.round(4)


def latest_alerts(rolling_metrics, limits):
    """Return latest rolling-metric exceptions; empty means no active exception."""
    latest = rolling_metrics.iloc[-1].dropna()
    thresholds = pd.Series(
        {
            "annualised_volatility": limits["annualised_volatility"],
            "var_95": limits["var_95"],
            "es_95": limits["es_95"],
        }
    )
    report = pd.DataFrame({"value": latest, "limit": thresholds}).dropna()
    report["status"] = report.apply(lambda row: "BREACH" if row["value"] > row["limit"] else "OK", axis=1)
    return report
