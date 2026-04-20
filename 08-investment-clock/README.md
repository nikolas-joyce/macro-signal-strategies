![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](COLAB_LINK)
[![Pages](https://img.shields.io/badge/GitHub-Pages-orange)](PAGES_LINK)

# 08-investment-clock

**Strategy:** Investment Clock - 4-quadrant Growth x Inflation multi-asset rotation (capstone).

## Abstract
Capstone composite. Signals from strategies 1-7 are aggregated into two orthogonal axes -- Growth direction and Inflation direction -- which define four macro regimes: Recovery, Expansion, Stagflation, Deflation. Each regime maps to a preferred asset class.

## Signal Formula
```
GrowthAxis = mean(Payrolls_z, CreditExcess_z, RealM2_z)
InflationAxis = mean(ExcessCPI_z, RealYield_z)
Regime = quadrant(GrowthAxis, InflationAxis)
```

## Directional Priors
- Recovery  (growth up, inflation down) -> **Equities**
- Expansion (growth up, inflation up)    -> **Commodities**
- Stagflation (growth down, inflation up) -> **Cash / short duration**
- Deflation (growth down, inflation down) -> **Bonds / receivers**

## ALFRED / FRED Series
| Series | Source | Vintage-Safe |
|---|---|---|
| CPIAUCSL  | ALFRED | YES |
| GDPC1  | ALFRED | YES |
| PAYEMS  | ALFRED | YES |
| M2SL  | ALFRED | YES |
| GS10  | ALFRED | YES |
| GS2  | ALFRED | YES |
| T5YIE  | ALFRED | YES |
| TOTLL  | ALFRED | YES |
| NFCI  | ALFRED | YES |

## Market Return Proxies (yfinance)
| Ticker | Role |
|---|---|
| SPY | Recovery pick |
| DJP | Expansion pick (commodities) |
| BIL | Stagflation pick (T-bills) |
| TLT | Deflation pick (long bonds) |

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
