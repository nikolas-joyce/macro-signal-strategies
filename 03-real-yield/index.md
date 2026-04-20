---
layout: default
title: Real Yield
---

## Abstract
Real yields are computed as 5Y nominal minus 5Y breakeven inflation. Rising real yields tighten financial conditions, hurting long-duration bonds and weakening risk currencies versus USD.

## Theory
The economic logic linking real yield to asset returns:

- Rising real yield is **negative** for long-duration bonds
- Rising real yield is **positive** for USD (vs. risk FX)
- Signal works best outside ZLB regimes

## Signal Construction
**Formula:**
```
RealYield = GS5 - T5YIE; Signal = z_{60m}(RealYield).clip(+/-3).shift(1)
```

After computing the raw series, a rolling 60-month z-score is applied, clipped at +/- 3 sigma, and lagged one period before use.

## Data
| Series | Source | Vintage-Safe |
|---|---|---|
| GS5  | ALFRED | YES |
| T5YIE  | ALFRED | YES |
| DFII5  | ALFRED | YES |

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
