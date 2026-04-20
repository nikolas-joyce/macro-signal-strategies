![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](COLAB_LINK)
[![Pages](https://img.shields.io/badge/GitHub-Pages-orange)](PAGES_LINK)

# 02-yield-curve

**Strategy:** Yield Curve Slope - 10Y-2Y slope as duration + equity regime signal.

## Abstract
The 10Y-2Y Treasury slope is treated as a leading indicator of growth and a duration tilt. A steepening curve from recession lows is historically bullish for equity beta and bearish for long-duration bond longs.

## Signal Formula
```
YieldCurveSlope = GS10 - GS2; Signal = z_{60m}(Slope).clip(+/-3).shift(1)
```

## Directional Priors
- Inverted curve is a **leading** recession signal (negative for equities 6-18m forward)
- Steepening from troughs is **positive** for equity beta
- Steepening is **negative** for long-duration bond longs (TLT)

## ALFRED / FRED Series
| Series | Source | Vintage-Safe |
|---|---|---|
| T10Y2Y  | ALFRED | YES |
| GS10  | ALFRED | YES |
| GS2  | ALFRED | YES |
| T10Y3M  | ALFRED | YES |

## Market Return Proxies (yfinance)
| Ticker | Role |
|---|---|
| TLT | Long duration bond proxy |
| IEF | Intermediate duration bond proxy |
| SPY | US equities |

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
