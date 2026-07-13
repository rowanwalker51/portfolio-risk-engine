"""A compact, reproducible multi-asset portfolio risk analytics toolkit."""

from .config import ASSET_CLASSES, RISK_LIMITS, WEIGHTS
from .market_data import generate_market_data
from .portfolio import portfolio_returns

__all__ = ["ASSET_CLASSES", "RISK_LIMITS", "WEIGHTS", "generate_market_data", "portfolio_returns"]
