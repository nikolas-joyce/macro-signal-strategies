![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](COLAB_LINK)
[![Pages](https://img.shields.io/badge/GitHub-Pages-orange)](PAGES_LINK)

# 07-financial-conditions

**Strategy:** Financial Conditions - NFCI level and change as equity beta overlay.

## Abstract
The Chicago Fed's National Financial Conditions Index (NFCI) aggregates ~100 credit, risk, and leverage indicators. Tightening conditions (rising NFCI) are a proximate equity sell signal; loosening conditions support risk-on.

## Signal Formula
```
FCSignal = (NFCI_level + NFCI_change_{3m}) / 2; Signal = z_{60m}.shift(1)
```

## Directional Priors
- Rising NFCI is **negative** for equities (high-frequency)
- Falling NFCI is **positive** for equity beta
- Use level **and** change to catch inflection points

## ALFRED / FRED Series
| Series | Source | Vintage-Safe |
|---|---|---|
| NFCI  | ALFRED | YES |
| NFCILEVERAGE  | ALFRED | YES |
| ANFCI  | ALFRED | YES |

## Market Return Proxies (yfinance)
| Ticker | Role |
|---|---|
| SPY | US equities |
| IWM | US small-cap (high-beta) |
| HYG | High-yield credit |

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
