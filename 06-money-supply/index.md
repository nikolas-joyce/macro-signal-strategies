---
layout: default
title: Money Supply (Real M2)
---

## Abstract
Real M2 growth (nominal M2 deflated by headline CPI) captures liquidity conditions that drive equity multiples. Strong real M2 expansion precedes equity re-ratings; contraction precedes sell-offs.

## Theory
The economic logic linking money supply (real m2) to asset returns:

- Positive real M2 growth is **bullish** for equity multiples
- Negative real M2 growth is **bearish** for risk assets
- Signal lags -- best as an overlay, not a timing tool

## Signal Construction
**Formula:**
```
RealM2Growth = g_{12m}(M2SL) - g_{12m}(CPIAUCSL); Signal = z_{60m}.shift(1)
```

After computing the raw series, a rolling 60-month z-score is applied, clipped at +/- 3 sigma, and lagged one period before use.

## Data
| Series | Source | Vintage-Safe |
|---|---|---|
| M2SL  | ALFRED | YES |
| CPIAUCSL  | ALFRED | YES |
| M2REAL  | ALFRED | YES |

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
