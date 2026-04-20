![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](COLAB_LINK)
[![Pages](https://img.shields.io/badge/GitHub-Pages-orange)](PAGES_LINK)

# 00-framework

Shared utilities imported by every strategy repo in the **macro-signal-strategies** org.

## What lives here

| Module | Purpose |
|---|---|
| `src/alfred_client.py` | ALFRED vintage pull + information-state (point-in-time) builder |
| `src/signal_builder.py` | Standard signal normalisation + reference implementations (excess inflation, yield curve, real yield, credit excess, real M2) |
| `src/composite.py` | Multi-signal aggregation + Investment Clock regime logic |
| `src/reporting.py` | Publication-ready chart templates and performance-metrics tables |

## Design principles

1. **No lookahead bias** - use ALFRED vintages everywhere, lag signals by 1 period.
2. **Point-in-time format** - signals reflect what was published and known at each date.
3. **Regime awareness** - note when a signal should not apply (ZLB regimes, Japan exception).
4. **Reproducibility** - cache every ALFRED pull to parquet; pin versions.
5. **Modularity** - this repo is the single source of truth for shared logic.

## Install

```bash
pip install -r requirements.txt
```

## Quick test

```python
import os
from src import get_alfred_vintages, build_information_state, excess_inflation_signal

vintages = get_alfred_vintages("CPIAUCSL", os.environ["FRED_API_KEY"])
cpi_pit  = build_information_state(vintages)["value"]
signal   = excess_inflation_signal(cpi_pit, inflation_target=2.0)
print(signal.tail())
```

## Strategy repos that consume this framework

1. [01-excess-inflation](../01-excess-inflation)
2. [02-yield-curve](../02-yield-curve)
3. [03-real-yield](../03-real-yield)
4. [04-credit-cycle](../04-credit-cycle)
5. [05-labor-market](../05-labor-market)
6. [06-money-supply](../06-money-supply)
7. [07-financial-conditions](../07-financial-conditions)
8. [08-investment-clock](../08-investment-clock)
