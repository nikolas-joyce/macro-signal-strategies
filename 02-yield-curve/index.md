---
layout: default
title: Yield Curve Slope
---

## Abstract
The 10Y-2Y Treasury slope is treated as a leading indicator of growth and a duration tilt. A steepening curve from recession lows is historically bullish for equity beta and bearish for long-duration bond longs.

## Theory
The economic logic linking yield curve slope to asset returns:

- Inverted curve is a **leading** recession signal (negative for equities 6-18m forward)
- Steepening from troughs is **positive** for equity beta
- Steepening is **negative** for long-duration bond longs (TLT)

## Signal Construction
**Formula:**
```
YieldCurveSlope = GS10 - GS2; Signal = z_{60m}(Slope).clip(+/-3).shift(1)
```

After computing the raw series, a rolling 60-month z-score is applied, clipped at +/- 3 sigma, and lagged one period before use.

## Data
| Series | Source | Vintage-Safe |
|---|---|---|
| T10Y2Y  | ALFRED | YES |
| GS10  | ALFRED | YES |
| GS2  | ALFRED | YES |
| T10Y3M  | ALFRED | YES |

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
