![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](COLAB_LINK)
[![Pages](https://img.shields.io/badge/GitHub-Pages-orange)](PAGES_LINK)

# 04-credit-cycle

**Strategy:** Credit Cycle - Private credit growth vs GDP trend as equity/credit signal.

## Abstract
Credit cycle signal tracks excess growth of private credit relative to real GDP. Above-trend credit expansion precedes equity tops and credit spread widening; contractions precede recoveries.

## Signal Formula
```
CreditExcess = g_{4q}(TOTLL) - g_{4q}(GDPC1); Signal = z_{20q}.clip(+/-3).shift(1)
```

## Directional Priors
- Excess credit growth precedes **equity drawdowns** (12-24m lead)
- Credit contractions precede **recoveries**
- Signal is quarterly -- use cautiously at higher frequencies

## ALFRED / FRED Series
| Series | Source | Vintage-Safe |
|---|---|---|
| TOTLL  | ALFRED | YES |
| GDPC1  | ALFRED | YES |
| M2SL  | ALFRED | YES |
| BUSLOANS  | ALFRED | YES |

## Market Return Proxies (yfinance)
| Ticker | Role |
|---|---|
| SPY | US equities |
| HYG | High-yield credit |
| LQD | Investment-grade credit |

## Notebooks
| # | Notebook | Role |
|---|---|---|
| 1 | `notebooks/01_data_acquisition.ipynb`   | Pull ALFRED vintages, build info-state panel |
| 2 | `notebooks/02_signal_construction.ipynb` | Raw signal + z-score + variants |
| 3 | `notebooks/03_backtest.ipynb`            | VectorBT sims: directional / overlay / sized |
| 4 | `notebooks/04_analysis_reporting.ipynb`  | Regime analysis, charts, export to `index.md` |

## Related
- Framework: [00-framework](../00-framework)
- Hub site: [docs/](../docs)
