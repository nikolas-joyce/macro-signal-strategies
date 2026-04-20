![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](COLAB_LINK)
[![Pages](https://img.shields.io/badge/GitHub-Pages-orange)](PAGES_LINK)

# 01-excess-inflation

**Flagship strategy.** Systematic macro overlay using headline CPI growth relative to each central bank's effective inflation target. Long excess inflation is bearish for equities and bond-receivers, and bullish for the local currency.

## Abstract
Point-in-time CPI data from ALFRED is used to reconstruct the inflation surprise actually observable to traders at each historical date. The resulting signal is z-scored over a 60-month window and traded as (a) a long-short directional, (b) an equity risk overlay, and (c) an FX relative-value construct.

## Signal Formula
```
ExcessInflation  = (CPI_{6m/6m, annualised} - Target) / max(Target, 2%)
Signal_t         = rolling_z(ExcessInflation, 60m).clip(+/-3).shift(1)
```

## Data
| Series | Source | Vintage-Safe |
|---|---|---|
| CPIAUCSL  | ALFRED | YES |
| CPILFESL  | ALFRED | YES |
| PCEPILFE  | ALFRED | YES |
| FEDFUNDS  | ALFRED | YES |
| SPY/TLT/UUP | yfinance | n/a |

## Notebooks
| # | Notebook | Role |
|---|---|---|
| 1 | `notebooks/01_data_acquisition.ipynb`   | Pull ALFRED vintages, build info-state panel |
| 2 | `notebooks/02_signal_construction.ipynb` | Excess-CPI z-score, variants, IC |
| 3 | `notebooks/03_backtest.ipynb`            | VectorBT sims: directional / overlay / sized |
| 4 | `notebooks/04_analysis_reporting.ipynb`  | Regime analysis, PDF-quality charts, `index.md` |

## Key Results (to populate after backtest)
| Metric | Strategy | Long-Only |
|---|---|---|
| Sharpe | TBD | TBD |
| Sortino | TBD | TBD |
| Max DD | TBD | TBD |

## Related
- Framework: [00-framework](../00-framework)
- Hub site: [docs/](../docs)
