---
layout: default
title: Labor Market
---

## Abstract
The labor-market signal compares non-farm payroll growth against civilian labor-force growth, net of the natural unemployment rate (NAIRU). Tight labor markets precede central-bank tightening cycles.

## Theory
The economic logic linking labor market to asset returns:

- Tight labor markets are **negative** for bonds (tightening follows)
- Unemployment crossing NAIRU downward is **early stage bullish** for equities
- Deteriorating payrolls are **positive** for bond longs

## Signal Construction
**Formula:**
```
LaborTightness = g_{12m}(PAYEMS) - g_{12m}(CLF16OV); Signal = z_{60m}.shift(1)
```

After computing the raw series, a rolling 60-month z-score is applied, clipped at +/- 3 sigma, and lagged one period before use.

## Data
| Series | Source | Vintage-Safe |
|---|---|---|
| PAYEMS  | ALFRED | YES |
| UNRATE  | ALFRED | YES |
| NROU  | ALFRED | YES |
| CLF16OV  | ALFRED | YES |

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
