---
layout: default
title: Credit Cycle
---

## Abstract
Credit cycle signal tracks excess growth of private credit relative to real GDP. Above-trend credit expansion precedes equity tops and credit spread widening; contractions precede recoveries.

## Theory
The economic logic linking credit cycle to asset returns:

- Excess credit growth precedes **equity drawdowns** (12-24m lead)
- Credit contractions precede **recoveries**
- Signal is quarterly -- use cautiously at higher frequencies

## Signal Construction
**Formula:**
```
CreditExcess = g_{4q}(TOTLL) - g_{4q}(GDPC1); Signal = z_{20q}.clip(+/-3).shift(1)
```

After computing the raw series, a rolling 60-month z-score is applied, clipped at +/- 3 sigma, and lagged one period before use.

## Data
| Series | Source | Vintage-Safe |
|---|---|---|
| TOTLL  | ALFRED | YES |
| GDPC1  | ALFRED | YES |
| M2SL  | ALFRED | YES |
| BUSLOANS  | ALFRED | YES |

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
