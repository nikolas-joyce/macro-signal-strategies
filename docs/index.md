# Macro Signal Strategies

Open-source systematic macro trading research.
Each strategy uses vintage-safe ALFRED data + VectorBT backtesting.

## Strategy Library

| # | Strategy | Signal | Assets |
|---|---|---|---|
| 1 | [Excess Inflation](../01-excess-inflation) | CPI vs target | Equity overlay, IRS, FX |
| 2 | [Yield Curve](../02-yield-curve) | 10Y-2Y slope | Duration, equity timing |
| 3 | [Real Yield](../03-real-yield) | Nominal - breakeven | Bond RV, FX |
| 4 | [Credit Cycle](../04-credit-cycle) | Credit vs GDP trend | Equity vs credit |
| 5 | [Labor Market](../05-labor-market) | Payrolls vs labor force | Equity, FX |
| 6 | [Money Supply](../06-money-supply) | Real M2 growth | Equity timing |
| 7 | [Financial Conditions](../07-financial-conditions) | NFCI level + change | Equity beta |
| 8 | [Investment Clock](../08-investment-clock) | Growth x Inflation | Multi-asset rotation |

## Framework
- [ALFRED Vintage Methodology](framework/alfred.md)
- [Signal Normalisation Standard](framework/signals.md)
- [VectorBT Configuration Guide](framework/vectorbt.md)

## Design Principles
1. **No lookahead bias** - ALFRED vintages everywhere, signals lagged by 1 period.
2. **Point-in-time format** - every signal reflects what was actually published at each date.
3. **Regime awareness** - each note documents where the signal breaks down.
4. **Intellectual honesty** - every notebook ends with a limitations section.
5. **Reproducibility** - all data cached to parquet, seeds set, versions pinned.

## Inspiration
Methodology adapted from Macrosynergy / JPMaQS quantamental research - excess inflation as a trading signal across equities, fixed income, and FX.
