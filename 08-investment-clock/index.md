---
layout: default
title: Investment Clock
---

## Abstract
Capstone composite. Signals from strategies 1-7 are aggregated into two orthogonal axes -- Growth direction and Inflation direction -- which define four macro regimes: Recovery, Expansion, Stagflation, Deflation. Each regime maps to a preferred asset class.

## Theory
The economic logic linking investment clock to asset returns:

- Recovery  (growth up, inflation down) -> **Equities**
- Expansion (growth up, inflation up)    -> **Commodities**
- Stagflation (growth down, inflation up) -> **Cash / short duration**
- Deflation (growth down, inflation down) -> **Bonds / receivers**

## Signal Construction
**Formula:**
```
GrowthAxis = mean(Payrolls_z, CreditExcess_z, RealM2_z)
InflationAxis = mean(ExcessCPI_z, RealYield_z)
Regime = quadrant(GrowthAxis, InflationAxis)
```

After computing the raw series, a rolling 60-month z-score is applied, clipped at +/- 3 sigma, and lagged one period before use.

## Data
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

## Results
![Cumulative PnL](assets/charts/pnl_cumulative.png)

| Metric | Strategy | Long-Only |
|--------|----------|-----------|
| Sharpe | TBD | TBD |
| Sortino | TBD | TBD |
| Max DD | TBD | TBD |

## Open in Colab
[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](COLAB_LINK)

## Limitations
- Some series have limited ALFRED vintage history pre-2000.
- ETF proxies introduce basis risk versus true futures / swaps.
- Signal assumes regime stationarity over the 60-month z-score window.
- Applicability may break down at the zero lower bound.
