"""
signal_builder.py
=================
Signal construction primitives shared by every strategy repo.

Includes:
- excess_inflation_signal : flagship reference implementation for Strategy 1
- normalise_signal        : the standard rolling z-score / clip / lag recipe
- excess_signal           : generic (series - target) / target excess function
- yield_curve_slope       : helper for Strategy 2
- real_yield              : helper for Strategy 3

The goal is that every strategy repo uses the same normalisation and lagging
conventions, so cross-strategy comparisons and the composite in Strategy 8
are apples-to-apples.
"""

from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Standard signal normalisation
# ---------------------------------------------------------------------------
def normalise_signal(raw: pd.Series, window: int = 60) -> pd.Series:
    """
    Rolling z-score, clipped at +/- 3 sigma, lagged 1 period.

    Parameters
    ----------
    raw : pd.Series
        Untransformed signal series.
    window : int, default 60
        Rolling window length in periods (60 months = 5Y for monthly data).

    Returns
    -------
    pd.Series
        Normalised, clipped, lagged signal suitable for backtesting.
    """
    mu = raw.rolling(window).mean()
    sigma = raw.rolling(window).std()
    return ((raw - mu) / sigma).clip(-3, 3).shift(1)


# ---------------------------------------------------------------------------
# Excess Inflation (Strategy 1) -- reference implementation
# ---------------------------------------------------------------------------
def excess_inflation_signal(
    cpi: pd.Series,
    inflation_target: float = 2.0,
    lookback_months: int = 6,
    zscore_window: int = 60,
) -> pd.Series:
    """
    Build the flagship Excess Inflation signal.

    Formula
    -------
        cpi_6m_change_ann  = (1 + CPI.pct_change(6))**2 - 1
        excess             = cpi_6m_change_ann*100 - target
        excess_scaled      = excess / max(target, 2.0)
        signal             = rolling-z(excess_scaled, 60).clip(+/-3).shift(1)

    Parameters
    ----------
    cpi : pd.Series
        Point-in-time CPI index level (monthly).
    inflation_target : float, default 2.0
        Central bank's effective inflation target in percent.
        Use 2.0 for USD/EUR/GBP/AUD/CAD/NZD, 1.0 for JPY/CHF (post-ZLB).
    lookback_months : int, default 6
        Horizon for the CPI change calculation.
    zscore_window : int, default 60
        Rolling z-score window in months.

    Returns
    -------
    pd.Series
        Final, lagged excess-inflation signal.
    """
    # Step 1: 6-month-over-6-month annualised CPI change
    cpi_change = cpi.pct_change(lookback_months).apply(
        lambda x: (1 + x) ** (12 / lookback_months) - 1
    ) * 100

    # Step 2: Raw excess
    excess = cpi_change - inflation_target

    # Step 3: Scale by target (floor 2% for cross-country comparability)
    scaled = excess / max(inflation_target, 2.0)

    # Steps 4-6: z-score, clip, lag
    return normalise_signal(scaled, window=zscore_window)


# ---------------------------------------------------------------------------
# Generic "excess-vs-target" signal
# ---------------------------------------------------------------------------
def excess_signal(
    series: pd.Series,
    target: float | pd.Series,
    floor: Optional[float] = None,
    zscore_window: int = 60,
) -> pd.Series:
    """
    Generic excess-vs-target signal: (series - target) scaled + normalised.

    Parameters
    ----------
    series : pd.Series
        Observed series (already in percent or rate terms).
    target : float or pd.Series
        Target value. Scalar broadcast or time-varying target.
    floor : float, optional
        Minimum divisor when scaling (avoids blow-up when target near 0).
    zscore_window : int, default 60
        Rolling z-score window.

    Returns
    -------
    pd.Series
        Normalised, clipped, lagged signal.
    """
    diff = series - target
    if floor is not None:
        if isinstance(target, pd.Series):
            divisor = np.maximum(target, floor)
        else:
            divisor = max(target, floor)
        scaled = diff / divisor
    else:
        scaled = diff
    return normalise_signal(scaled, window=zscore_window)


# ---------------------------------------------------------------------------
# Yield-curve slope (Strategy 2)
# ---------------------------------------------------------------------------
def yield_curve_slope(
    long_rate: pd.Series,
    short_rate: pd.Series,
    zscore_window: int = 60,
) -> pd.Series:
    """Long rate minus short rate, normalised & lagged."""
    slope = long_rate - short_rate
    return normalise_signal(slope, window=zscore_window)


# ---------------------------------------------------------------------------
# Real yield (Strategy 3)
# ---------------------------------------------------------------------------
def real_yield(
    nominal: pd.Series,
    breakeven: pd.Series,
    zscore_window: int = 60,
) -> pd.Series:
    """Real yield = nominal - breakeven inflation, normalised & lagged."""
    ry = nominal - breakeven
    return normalise_signal(ry, window=zscore_window)


# ---------------------------------------------------------------------------
# Credit growth vs GDP growth (Strategy 4)
# ---------------------------------------------------------------------------
def credit_excess(
    credit: pd.Series,
    gdp: pd.Series,
    lookback: int = 4,
    zscore_window: int = 20,
) -> pd.Series:
    """
    Excess credit growth: credit growth minus GDP growth.
    Default lookback=4 (qtr) assumes quarterly data.
    """
    credit_g = credit.pct_change(lookback) * 100
    gdp_g = gdp.pct_change(lookback) * 100
    return normalise_signal(credit_g - gdp_g, window=zscore_window)


# ---------------------------------------------------------------------------
# Real M2 growth (Strategy 6)
# ---------------------------------------------------------------------------
def real_m2_growth(
    m2: pd.Series,
    cpi: pd.Series,
    lookback: int = 12,
    zscore_window: int = 60,
) -> pd.Series:
    """Real money-supply growth = nominal M2 growth minus CPI growth."""
    nominal_g = m2.pct_change(lookback) * 100
    cpi_g = cpi.pct_change(lookback) * 100
    return normalise_signal(nominal_g - cpi_g, window=zscore_window)
