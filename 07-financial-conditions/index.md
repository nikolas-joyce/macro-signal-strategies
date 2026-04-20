---
layout: default
title: Financial Conditions
---

## Abstract
The Chicago Fed's National Financial Conditions Index (NFCI) aggregates ~100 credit, risk, and leverage indicators. Tightening conditions (rising NFCI) are a proximate equity sell signal; loosening conditions support risk-on.

## Theory
The economic logic linking financial conditions to asset returns:

- Rising NFCI is **negative** for equities (high-frequency)
- Falling NFCI is **positive** for equity beta
- Use level **and** change to catch inflection points

## Signal Construction
**Formula:**
```
FCSignal = (NFCI_level + NFCI_change_{3m}) / 2; Signal = z_{60m}.shift(1)
```

After computing the raw series, a rolling 60-month z-score is applied, clipped at +/- 3 sigma, and lagged one period before use.

## Data
| Series | Source | Vintage-Safe |
|---|---|---|
| NFCI  | ALFRED | YES |
| NFCILEVERAGE  | ALFRED | YES |
| ANFCI  | ALFRED | YES |

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
