---
layout: default
title: Signal Normalisation Standard
---

# Signal Normalisation Standard

Every strategy in this org applies the same normalisation recipe so cross-strategy comparisons (and the Investment Clock composite) are apples-to-apples.

## The Recipe
1. Compute the raw economic quantity (e.g. CPI 6m/6m annualised minus target).
2. Apply a rolling z-score with a 60-month window.
3. Clip at +/- 3 sigma.
4. Lag by 1 period (guarantees no same-period lookahead).

## Code
```python
def normalise_signal(raw: pd.Series, window: int = 60) -> pd.Series:
    mu    = raw.rolling(window).mean()
    sigma = raw.rolling(window).std()
    return ((raw - mu) / sigma).clip(-3, 3).shift(1)
```

## Reference Implementations
- `excess_inflation_signal` - Strategy 1 (6m annualised CPI minus target, target-scaled)
- `yield_curve_slope` - Strategy 2
- `real_yield` - Strategy 3
- `credit_excess` - Strategy 4
- `real_m2_growth` - Strategy 6

## Composites
For Strategy 8, the Investment Clock builds two orthogonal composites:
- **Growth axis:** average of payroll, credit excess, and real-M2 signals
- **Inflation axis:** average of excess-CPI and real-yield signals

Each date is then classified into Recovery / Expansion / Stagflation / Deflation.

## Why 60 Months?
Five years is long enough to span at least one half of a typical business cycle, so the rolling mean does not chase short-term trends. It is short enough to adapt to regime changes within a single career.
