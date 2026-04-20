"""Excess Inflation signal wrappers.

Imports the framework normalisation + reference implementation, and exposes
the strategy-specific defaults (6-month annualised, 2% target floor, 60-month
z-score window).
"""

import sys
from pathlib import Path

import pandas as pd

_FRAMEWORK = Path(__file__).resolve().parents[2] / "00-framework"
if str(_FRAMEWORK) not in sys.path:
    sys.path.insert(0, str(_FRAMEWORK))

from src.signal_builder import (  # type: ignore  # noqa: F401,E402
    normalise_signal,
    excess_inflation_signal,
    excess_signal,
)


def build_strategy_signal(
    cpi_pit: pd.Series,
    inflation_target: float = 2.0,
) -> pd.Series:
    """Canonical Excess Inflation signal for this repo."""
    return excess_inflation_signal(
        cpi_pit,
        inflation_target=inflation_target,
        lookback_months=6,
        zscore_window=60,
    )
