# macro-signal-strategies

> Macroeconomic signal strategies applied to ETFs — each strategy is a self-contained Colab notebook pulling live data from FRED and yfinance.

## Strategies

| # | Strategy | Signal | Notebook |
|---|----------|--------|----------|
| 01 | Excess Inflation | CPI deviation from 2% Fed target (z-scored) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nikolas-joyce/macro-signal-strategies/blob/main/01-excess-inflation/notebooks/excess_inflation_strategy.ipynb) |

## How to run

Each notebook is fully self-contained — no CSV uploads, no Drive mounts. Just open in Colab and run all cells.

**Required Colab Secrets:**
- `FRED_API_KEY` — free key at https://fred.stlouisfed.org/docs/api/api_key.html
