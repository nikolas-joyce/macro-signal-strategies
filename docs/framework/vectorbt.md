---
layout: default
title: VectorBT Configuration Guide
---

# VectorBT Configuration Guide

Every strategy repo uses the same backtesting conventions. This keeps Sharpe, Sortino, Max DD, and turnover comparable across signals.

## Standard Install
```python
!pip install -q vectorbt yfinance fredapi pandas-ta matplotlib seaborn
```

## Standard Portfolio Construction
```python
import vectorbt as vbt

portfolio = vbt.Portfolio.from_signals(
    close=prices,
    entries=signal_long,
    exits=signal_short,
    freq='M',
    init_cash=100_000,
    fees=0.0005,       # 5 bps
    slippage=0.001,    # 10 bps round-trip
)
```

## Vol Targeting
```python
def vol_target_returns(returns: pd.Series, target_vol: float = 0.10) -> pd.Series:
    \"\"\"Scale position sizes to target annualised volatility.\"\"\"
    realised_vol = returns.rolling(63).std() * np.sqrt(252)
    scalar = (target_vol / realised_vol).shift(1).clip(0.1, 3.0)
    return returns * scalar
```

## Strategy Variants
Every repo backtests at least three variants:
1. **Pure directional** - long when signal > 0, short when < 0
2. **Long-only overlay** - hold when signal > threshold, else flat
3. **Continuous sizing** - position = f(signal z-score), capped at +/- 1

## Performance Metrics Table
Standard metrics per repo:
- Sharpe
- Sortino
- Max drawdown
- Calmar
- Win rate
- Benchmark correlation

## Robustness Checks
Every repo includes:
- Walk-forward validation
- Parameter sensitivity heatmap (Sharpe vs. lookback x threshold)
- Sub-period tables (pre-2000, 2000-2010, 2010-2020, 2020+)
- Transaction-cost sensitivity (0, 5 bps, 20 bps round-trip)
