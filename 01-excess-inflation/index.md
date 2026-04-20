---
layout: default
title: Excess Inflation Signal
---

## Abstract
Point-in-time CPI data from ALFRED is used to reconstruct the inflation surprise actually observable to traders at each historical date. Excess inflation (CPI 6m/6m annualised minus each central bank's target) is z-scored and traded as (a) a long-short directional, (b) an equity risk overlay, and (c) an FX relative-value construct.

## Theory
Shifts in monetary-policy balance that arise when realised inflation runs above target are not always fully priced at release. In the quantamental (point-in-time) format, signals capture the information state actually available to traders, avoiding the backtest inflation that comes from trading against modern revised CPI.

Directional priors:
- High excess inflation is **negative** for equities (rising discount rates outpace dividend growth)
- High excess inflation is **negative** for IRS receivers / bond longs (central-bank tightening)
- High excess inflation is **positive** for local-currency FX (tightening expectations)

## Signal Construction
**Formula:** ExcessInflation = (CPI_{6m/6m, annualised} - Target) / max(Target, 2%)

After computing the raw series, a rolling 60-month z-score is applied, clipped at +/- 3 sigma, and lagged one period before use.

## Data
| Series | Source | Vintage-Safe |
|--------|--------|-------------|
| CPIAUCSL  | ALFRED | YES |
| CPILFESL  | ALFRED | YES |
| PCEPILFE  | ALFRED | YES |
| FEDFUNDS  | ALFRED | YES |

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
- ALFRED vintage coverage is thinner pre-1995
- ETF proxies introduce basis risk versus true IRS / FX futures
- US-centric inflation target assumptions (2% for USD/EUR/GBP/AUD/CAD/NZD, 1% for JPY/CHF)
- Strategy is sensitive to regime shifts at the zero lower bound
