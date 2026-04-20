![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](COLAB_LINK)
[![Pages](https://img.shields.io/badge/GitHub-Pages-orange)](PAGES_LINK)

# 03-real-yield

**Strategy:** Real Yield - 5Y nominal minus 5Y breakeven as bond + FX signal.

## Abstract
Real yields are computed as 5Y nominal minus 5Y breakeven inflation. Rising real yields tighten financial conditions, hurting long-duration bonds and weakening risk currencies versus USD.

## Signal Formula
```
RealYield = GS5 - T5YIE; Signal = z_{60m}(RealYield).clip(+/-3).shift(1)
```

## Directional Priors
- Rising real yield is **negative** for long-duration bonds
- Rising real yield is **positive** for USD (vs. risk FX)
- Signal works best outside ZLB regimes

## ALFRED / FRED Series
| Series | Source | Vintage-Safe |
|---|---|---|
| GS5  | ALFRED | YES |
| T5YIE  | ALFRED | YES |
| DFII5  | ALFRED | YES |

## Market Return Proxies (yfinance)
| Ticker | Role |
|---|---|
| TLT | Long duration |
| TIP | TIPS proxy |
| UUP | USD index proxy |

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
