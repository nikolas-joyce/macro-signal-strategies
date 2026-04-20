"""
composite.py
============
Multi-signal aggregation for Strategy 8 (Investment Clock) and other
composite constructs.
"""

from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd


def build_composite(
    signals: dict[str, pd.Series],
    weights: Optional[dict[str, float]] = None,
) -> pd.Series:
    """
    Equal risk-weight composite (conceptual parity) unless weights specified.

    Parameters
    ----------
    signals : dict[str, pd.Series]
        Mapping of signal name -> already-normalised signal series.
    weights : dict[str, float], optional
        Desired weights. If None, equal-weight across signals.

    Returns
    -------
    pd.Series
        Composite signal (sum of weight*signal across columns).
    """
    df = pd.DataFrame(signals)
    if weights is None:
        weights = {k: 1 / len(signals) for k in signals}
    weight_series = pd.Series(weights)
    return df.multiply(weight_series).sum(axis=1)


def investment_clock_regime(
    growth_signal: pd.Series,
    inflation_signal: pd.Series,
) -> pd.Series:
    """
    Classify each date into one of four Investment Clock regimes:

        Recovery     : growth up,   inflation down
        Expansion    : growth up,   inflation up
        Stagflation  : growth down, inflation up
        Deflation    : growth down, inflation down

    Parameters
    ----------
    growth_signal : pd.Series
        Already-normalised growth direction signal (sign-driven).
    inflation_signal : pd.Series
        Already-normalised inflation direction signal.

    Returns
    -------
    pd.Series
        Categorical series of regime labels.
    """
    growth_up = growth_signal > 0
    inflation_up = inflation_signal > 0

    regime = pd.Series(index=growth_signal.index, dtype="object")
    regime[growth_up & ~inflation_up] = "Recovery"
    regime[growth_up & inflation_up] = "Expansion"
    regime[~growth_up & inflation_up] = "Stagflation"
    regime[~growth_up & ~inflation_up] = "Deflation"
    return regime


REGIME_ASSET_MAP = {
    "Recovery": "Equity",
    "Expansion": "Commodity",
    "Stagflation": "Cash",
    "Deflation": "Bond",
}


def regime_to_asset(regime: pd.Series) -> pd.Series:
    """Translate regime labels into preferred asset per the Investment Clock."""
    return regime.map(REGIME_ASSET_MAP)


def risk_parity_weights(
    returns: pd.DataFrame,
    window: int = 63,
) -> pd.DataFrame:
    """
    Simple inverse-volatility risk parity weighting.

    Parameters
    ----------
    returns : pd.DataFrame
        Per-signal or per-asset return series.
    window : int, default 63
        Rolling window for vol estimate (~3 months at daily freq).
    """
    vol = returns.rolling(window).std() * np.sqrt(252)
    inv_vol = 1.0 / vol
    weights = inv_vol.div(inv_vol.sum(axis=1), axis=0)
    return weights
