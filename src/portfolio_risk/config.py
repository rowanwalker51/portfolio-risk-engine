"""Project assumptions kept in one easy-to-edit place."""

PERIODS = 756
RANDOM_SEED = 42
TRADING_DAYS = 252
CONFIDENCE_LEVEL = 0.95

WEIGHTS = {
    "US_Equity": 0.28,
    "Europe_Equity": 0.17,
    "US_10Y_Rates": 0.20,
    "Investment_Grade_Credit": 0.15,
    "EURUSD": 0.08,
    "Gold": 0.12,
}

ASSET_CLASSES = {
    "US_Equity": "Equity",
    "Europe_Equity": "Equity",
    "US_10Y_Rates": "Rates",
    "Investment_Grade_Credit": "Credit",
    "EURUSD": "FX",
    "Gold": "Commodity",
}

RISK_LIMITS = {
    "var_95": 0.018,
    "es_95": 0.024,
    "annualised_volatility": 0.16,
    "max_drawdown": 0.12,
}
