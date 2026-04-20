![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](COLAB_LINK)
[![Pages](https://img.shields.io/badge/GitHub-Pages-orange)](PAGES_LINK)

# 06-money-supply

**Strategy:** Money Supply (Real M2) - Real M2 growth as equity timing signal.

## Abstract
Real M2 growth (nominal M2 deflated by headline CPI) captures liquidity conditions that drive equity multiples. Strong real M2 expansion precedes equity re-ratings; contraction precedes sell-offs.

## Signal Formula
```
RealM2Growth = g_{12m}(M2SL) - g_{12m}(CPIAUCSL); Signal = z_{60m}.shift(1)
```

## Directional Priors
- Positive real M2 growth is **bullish** for equity multiples
- Negative real M2 growth is **bearish** for risk assets
- Signal lags -- best as an overlay, not a timing tool

## ALFRED / FRED Series
| Series | Source | Vintage-Safe |
|---|---|---|
| M2SL  | ALFRED | YES |
| CPIAUCSL  | ALFRED | YES |
| M2REAL  | ALFRED | YES |

## Market Return Proxies (yfinance)
| Ticker | Role |
|---|---|
| SPY | US equities |
| QQQ | US tech / long-duration equity |
| GLD | Gold (alternative liquidity proxy) |

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
