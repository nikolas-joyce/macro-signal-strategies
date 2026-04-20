"""Smoke tests for signal_builder primitives."""

import numpy as np
import pandas as pd

from src.signal_builder import normalise_signal, excess_inflation_signal


def test_normalise_signal_basic():
    rng = pd.date_range("2000-01-01", periods=120, freq="ME")
    raw = pd.Series(np.random.default_rng(0).standard_normal(120), index=rng)
    out = normalise_signal(raw, window=24)
    assert out.isna().sum() >= 24
    assert out.dropna().between(-3, 3).all()


def test_excess_inflation_signal_shape():
    rng = pd.date_range("1990-01-01", periods=240, freq="ME")
    cpi = pd.Series(np.linspace(130, 310, 240), index=rng)
    sig = excess_inflation_signal(cpi, inflation_target=2.0)
    assert sig.shape == cpi.shape
