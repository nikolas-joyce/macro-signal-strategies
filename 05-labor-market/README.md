![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](COLAB_LINK)
[![Pages](https://img.shields.io/badge/GitHub-Pages-orange)](PAGES_LINK)

# 05-labor-market

**Strategy:** Labor Market - Payrolls vs labor force signal for equities + FX.

## Abstract
The labor-market signal compares non-farm payroll growth against civilian labor-force growth, net of the natural unemployment rate (NAIRU). Tight labor markets precede central-bank tightening cycles.

## Signal Formula
```
LaborTightness = g_{12m}(PAYEMS) - g_{12m}(CLF16OV); Signal = z_{60m}.shift(1)
```

## Directional Priors
- Tight labor markets are **negative** for bonds (tightening follows)
- Unemployment crossing NAIRU downward is **early stage bullish** for equities
- Deteriorating payrolls are **positive** for bond longs

## ALFRED / FRED Series
| Series | Source | Vintage-Safe |
|---|---|---|
| PAYEMS  | ALFRED | YES |
| UNRATE  | ALFRED | YES |
| NROU  | ALFRED | YES |
| CLF16OV  | ALFRED | YES |

## Market Return Proxies (yfinance)
| Ticker | Role |
|---|---|
| SPY | US equities |
| TLT | Long duration bonds |
| UUP | USD index |

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
