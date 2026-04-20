# Macro Signal Strategies — Project Brief
> **Purpose:** Hand this document to Claude Code or Cowork as the complete starting context for building the macro signal strategies research repository system. It captures all decisions, architecture, naming conventions, data sources, and notebook structures agreed upon in the planning session.

---

## 1. Project Vision

Build a suite of open-source, reproducible macro signal trading strategy research repositories — each backed by vintage-safe economic data from ALFRED, backtested with VectorBT in Google Colab, and published as GitHub Pages research notes. The project targets systematic macro traders, quant researchers, and finance students.

**Inspired by:** Macrosynergy / JPMaQS quantamental research methodology (excess inflation as trading signal across equities, fixed income, and FX).

---

## 2. Repository Architecture

### Top-Level Structure (GitHub Organisation)

```
org: macro-signal-strategies/
│
├── 00-framework/                  ← Shared utilities imported by all strategy repos
├── 01-excess-inflation/           ← Strategy 1 (flagship)
├── 02-yield-curve/                ← Strategy 2
├── 03-real-yield/                 ← Strategy 3
├── 04-credit-cycle/               ← Strategy 4
├── 05-labor-market/               ← Strategy 5
├── 06-money-supply/               ← Strategy 6
├── 07-financial-conditions/       ← Strategy 7
├── 08-investment-clock/           ← Strategy 8 (composite capstone)
└── docs/                          ← GitHub Pages hub site
```

### Per-Strategy Repo Structure

```
01-excess-inflation/
│
├── README.md                      ← Abstract + Colab badge + key results
├── _config.yml                    ← GitHub Pages Jekyll config
├── index.md                       ← Pages explainer ("the paper")
├── assets/
│   ├── charts/                    ← Exported PNGs for Pages site
│   └── css/custom.css
│
├── notebooks/
│   ├── 01_data_acquisition.ipynb
│   ├── 02_signal_construction.ipynb
│   ├── 03_backtest.ipynb
│   └── 04_analysis_reporting.ipynb
│
├── src/
│   ├── alfred_client.py           ← ALFRED API vintage wrapper
│   ├── signal_builder.py          ← Signal construction logic
│   ├── composite.py               ← Multi-signal aggregation
│   └── reporting.py               ← Chart/table generators
│
├── data/
│   ├── raw/                       ← ALFRED vintage pulls (cached parquet)
│   └── processed/                 ← Signals, returns, composites
│
├── requirements.txt
└── environment.yml
```

---

## 3. Naming Conventions

### Strategy Naming Pattern

```
[SignalConcept]_[MeasureType]_[AssetClass]_[PositionStyle]

Examples:
  ExcessCPI_Level_IRS_Directional
  ExcessCPI_Change_Equity_Overlay
  RelativeCPI_Level_FX_RelativeValue
  CreditGrowth_Excess_FixedIncome_Directional
  EmploymentGrowth_Rate_Equity_CrossCountry
  YieldCurve_Slope_Equity_RegimeFilter
```

### Tier Definitions

| Tier | Options |
|---|---|
| **Signal Concept** | ExcessCPI, CPI_Change, YieldCurve, RealYield, CreditGrowth, M2_Real, Employment, FinancialConditions |
| **Measure Type** | Level, Change, Slope, Excess, Relative, Composite |
| **Asset Class** | Equity, IRS, FX, Credit, MultiAsset |
| **Position Style** | Directional, Overlay, RelativeValue, CrossCountry, RegimeFilter |

### Code Variable Naming (snake_case)

```python
excess_cpi_level          # signal series
excess_cpi_level_zscore   # normalised signal
irs_receiver_return       # target return
eq_index_return           # equity target
pnl_directional           # strategy PnL
pnl_overlay               # overlay variant PnL
sharpe_strategy           # metric
sharpe_benchmark          # metric
```

### File Naming

```
YYYY-MM-DD not used — use versioned parquet:
  cpiaucsl_alfred_vintages.parquet
  excess_inflation_signal.parquet
  irs_backtest_results.pkl
  eq_overlay_backtest_results.pkl
```

---

## 4. Theoretical Framework

### Core Hypothesis (Excess Inflation)

> Excess inflation = CPI growth − effective inflation target (scaled by target, floor 2%)

**Directional predictions:**
- High excess inflation → **negative** for equities (rising discount rates outpace dividend growth)
- High excess inflation → **negative** for IRS receivers / bond longs (central bank tightening)
- High excess inflation → **positive** for local currency FX (tightening expected)

**Why it works:** These shifting monetary policy balances are not always fully priced by the market at the time of data release. The quantamental (point-in-time) format captures the information state actually available to traders.

### Investment Clock Framework (Strategy 8)

Four macro regimes defined by Growth direction × Inflation direction:

| Regime | Growth | Inflation | Favoured Assets |
|---|---|---|---|
| Recovery | Rising | Falling | Equities |
| Expansion | Rising | Rising | Commodities |
| Stagflation | Falling | Rising | Cash, Short Duration |
| Deflation | Falling | Falling | Bonds, Receivers |

---

## 5. Data Sources

### Primary: ALFRED (Archival FRED)

**Purpose:** Vintage-safe data — provides the exact data release as it existed on any given historical date. Eliminates lookahead bias.

**API access:**
```python
# Free API key: register at fred.stlouisfed.org
from fredapi import Fred
fred = Fred(api_key='YOUR_KEY')

# Vintage data via ALFRED:
# https://alfred.stlouisfed.org/series/downloaddata?seid=CPIAUCSL&vintage_date=2010-01-15
```

### Key FRED/ALFRED Series by Strategy

| Strategy | Series IDs | Concept |
|---|---|---|
| Excess Inflation | `CPIAUCSL`, `CPILFESL`, `PCEPILFE`, `FEDFUNDS` | CPI headline, core, PCE, Fed rate proxy for target |
| Yield Curve | `T10Y2Y`, `GS10`, `GS2`, `T10Y3M` | Slope, long/short rates |
| Real Yield | `GS5`, `T5YIE`, `DFII5` | 5Y nominal, 5Y breakeven, 5Y TIPS |
| Credit Cycle | `TOTLL`, `GDPC1`, `M2SL`, `BUSLOANS` | Private credit, GDP, money supply |
| Labor Market | `PAYEMS`, `UNRATE`, `NROU`, `CLF16OV` | Payrolls, unemployment, NAIRU, labor force |
| Money Supply | `M2SL`, `CPIAUCSL`, `M2REAL` | Real M2 growth |
| Financial Conditions | `NFCI`, `NFCILEVERAGE`, `ANFCI` | Chicago Fed FCI |
| All / Composite | All of the above | Investment Clock |

### Secondary Sources

| Source | Use | Access |
|---|---|---|
| **OECD API** | Multi-country CPI, GDP for relative value | `stats.oecd.org/SDMX-JSON/data/` |
| **BIS** | Cross-country credit, FX, policy rates | `data.bis.org/api/` |
| **World Bank** | EM country data | `pip install wbgapi` |
| **yfinance** | ETF proxies for market returns | `pip install yfinance` |

### Market Return Proxies (yfinance tickers)

| Asset | Proxy ETF | Ticker |
|---|---|---|
| US Equities | SPY / IVV | `SPY` |
| Global ex-US Equities | ACWX | `ACWX` |
| Long Duration Bonds | TLT | `TLT` |
| Intermediate Bonds | IEF | `IEF` |
| USD Index (FX) | UUP | `UUP` |
| Commodities | DJP / PDBC | `DJP` |

---

## 6. Anti-Lookahead Bias Methodology

### The Problem

Standard FRED serves **revised** data. Backtesting on revised data overstates signal quality because traders in 2005 did not have the 2024-vintage CPI estimate — they had what was published in 2005.

### The Solution: Information State Construction

```python
def build_information_state(series_id: str, api_key: str) -> pd.DataFrame:
    """
    For each date t, use only the vintage of the data
    that was publicly available as of date t.
    Returns a Series indexed by date with no lookahead.
    """
    # 1. Pull all available vintages from ALFRED
    # 2. For each observation date, find the earliest vintage >= that date
    # 3. Use that vintage's value as the "known" value at time t
    # 4. Apply 1-period lag before using as signal
```

### Practical ALFRED Vintage Pull

```python
import requests
import pandas as pd

def get_alfred_vintages(series_id, api_key, start='1990-01-01'):
    url = f"https://api.stlouisfed.org/fred/series/vintagedates"
    params = {'series_id': series_id, 'api_key': api_key, 'file_type': 'json'}
    vintage_dates = requests.get(url, params=params).json()['vintage_dates']

    all_vintages = {}
    for vdate in vintage_dates:
        obs_url = f"https://api.stlouisfed.org/fred/series/observations"
        obs_params = {
            'series_id': series_id, 'api_key': api_key,
            'file_type': 'json', 'vintage_dates': vdate,
            'observation_start': start
        }
        obs = requests.get(obs_url, params=obs_params).json()['observations']
        all_vintages[vdate] = {o['date']: float(o['value'])
                               for o in obs if o['value'] != '.'}

    return pd.DataFrame(all_vintages)  # rows=obs_dates, cols=vintage_dates
```

---

## 7. Signal Construction Standards

### Excess Inflation Signal (Strategy 1 — Reference Implementation)

```python
import pandas as pd
import numpy as np

# Step 1: 6-month-over-6-month annualised CPI change
cpi_6m_change = cpi.pct_change(6).apply(lambda x: (1 + x)**2 - 1) * 100

# Step 2: Effective inflation target proxy
# Use 2.0% for USD, EUR, GBP, AUD, CAD, NZD
# Use 1.0% for JPY, CHF (post-ZLB)
inflation_target = 2.0

# Step 3: Raw excess inflation
excess_inflation = cpi_6m_change - inflation_target

# Step 4: Scale by target (floor 2% for cross-country comparability)
excess_inflation_scaled = excess_inflation / max(inflation_target, 2.0)

# Step 5: Rolling z-score normalisation (5Y window)
signal_zscore = (
    (excess_inflation_scaled - excess_inflation_scaled.rolling(60).mean())
    / excess_inflation_scaled.rolling(60).std()
).clip(-3, 3)

# Step 6: Lag by 1 period (no same-period lookahead)
signal_lagged = signal_zscore.shift(1)
```

### General Signal Normalisation (all strategies)

```python
def normalise_signal(raw: pd.Series, window: int = 60) -> pd.Series:
    """Rolling z-score, clipped at ±3σ, lagged 1 period."""
    mu = raw.rolling(window).mean()
    sigma = raw.rolling(window).std()
    return ((raw - mu) / sigma).clip(-3, 3).shift(1)
```

### Composite Signal (Strategy 8)

```python
def build_composite(signals: dict, weights: dict = None) -> pd.Series:
    """Equal risk-weight composite (conceptual parity) unless weights specified."""
    df = pd.DataFrame(signals)
    if weights is None:
        weights = {k: 1/len(signals) for k in signals}
    weight_series = pd.Series(weights)
    return df.multiply(weight_series).sum(axis=1)
```

---

## 8. Notebook Structure (All Four Notebooks — Standard Across All Repos)

### Notebook 1: Data Acquisition (`01_data_acquisition.ipynb`)

**Sections:**
1. Setup & Imports (install cell + Google Drive mount)
2. ALFRED Configuration (API key, vintage date logic)
3. Series Pull (all required FRED series, ALFRED vintage format)
4. Vintage Alignment (construct information state DataFrame)
5. Market Return Data (yfinance ETF proxies)
6. Data Quality Checks (vintage coverage heatmap, revision magnitude chart)
7. Export (`data/processed/aligned_panel.parquet`)

**Expected outputs:**
- Vintage coverage heatmap
- Revision magnitude chart (how much CPI gets revised post-release)
- Information-state panel DataFrame

---

### Notebook 2: Signal Construction (`02_signal_construction.ipynb`)

**Sections:**
1. Load aligned panel
2. Raw Signal Computation (formula as LaTeX in markdown cell)
3. Signal Transformations (z-score, clip, lag)
4. Alternative Signal Variants (headline vs. core, 3m vs. 6m, level vs. change)
5. Signal Validation (time series plot, distribution histogram, autocorrelation)
6. Predictive Power Pre-Backtest (rolling IC, scatter by quantile, balanced accuracy)
7. Export (`data/processed/signals.parquet`)

**Expected outputs:**
- Signal time series with annotated macro crises
- Information Coefficient bar chart by year
- Quintile return chart (Q1 vs. Q5 forward returns)

---

### Notebook 3: Backtest (`03_backtest.ipynb`)

**Sections:**
1. Load signals + returns
2. VectorBT Setup (frequency, slippage, fee assumptions, vol-targeting)
3. Strategy Variants:
   - (a) Pure directional: long when signal > 0, short when < 0
   - (b) Long-only overlay: hold when signal > threshold, else flat
   - (c) Continuous sizing: position = f(signal z-score), capped ±1
   - (d) Relative value (if multi-country)
4. VectorBT Simulation (`vbt.Portfolio.from_signals()`)
5. Performance Metrics Table (Sharpe, Sortino, max drawdown, Calmar, win rate, benchmark correlation)
6. Benchmark Comparison (PnL chart, drawdown chart, rolling 2Y Sharpe)
7. Robustness Checks (walk-forward, parameter sensitivity, sub-period, tx cost sensitivity)
8. Export (`data/processed/backtest_results.pkl`)

**Expected outputs:**
- Cumulative PnL chart (all variants + benchmark)
- Drawdown chart
- Parameter sensitivity heatmap (Sharpe vs. lookback × threshold)
- Sub-period performance table

---

### Notebook 4: Analysis & Reporting (`04_analysis_reporting.ipynb`)

**Sections:**
1. Load all outputs from Notebooks 1–3
2. Executive Summary Statistics (auto-generated markdown metrics table)
3. Signal Deep-Dive (behavior during named macro episodes: GFC, COVID, 2022 inflation shock)
4. Cross-Strategy Correlation (if running multiple strategies)
5. Regime Analysis (4-quadrant performance, conditional Sharpes)
6. Export for GitHub Pages (charts as PNG to `assets/charts/`, metrics HTML snippet)
7. Limitations & Caveats

**Expected outputs:**
- Strategy Fact Sheet (styled HTML table)
- Publication-ready annotated charts
- Auto-generated `index.md` summary block

---

## 9. VectorBT Configuration Standards

```python
# Standard Colab install cell (top of Notebook 3)
!pip install -q vectorbt yfinance fredapi pandas-ta matplotlib seaborn

import vectorbt as vbt
import pandas as pd
import numpy as np

# Vol-targeting wrapper
def vol_target_returns(returns: pd.Series, target_vol: float = 0.10) -> pd.Series:
    """Scale position sizes to target annualised volatility."""
    realised_vol = returns.rolling(63).std() * np.sqrt(252)
    scalar = (target_vol / realised_vol).shift(1).clip(0.1, 3.0)
    return returns * scalar

# Standard portfolio construction
portfolio = vbt.Portfolio.from_signals(
    close=prices,
    entries=signal_long,
    exits=signal_short,
    freq='M',
    init_cash=100_000,
    fees=0.0005,       # 5 bps
    slippage=0.001,    # 10 bps round-trip
)
```

---

## 10. Google Colab Setup Pattern

```python
# ─── Cell 1: Drive mount (top of every notebook) ───────────────────────────
from google.colab import drive
drive.mount('/content/drive')
BASE_PATH = '/content/drive/MyDrive/macro_strategies/'
import os; os.makedirs(BASE_PATH + 'data/raw', exist_ok=True)
os.makedirs(BASE_PATH + 'data/processed', exist_ok=True)

# ─── Cell 2: Standard installs ───────────────────────────────────────────────
!pip install -q fredapi vectorbt yfinance pandas-ta matplotlib seaborn pyarrow

# ─── Cell 3: API keys (store in Colab Secrets, not hardcoded) ──────────────
from google.colab import userdata
FRED_API_KEY = userdata.get('FRED_API_KEY')
```

---

## 11. GitHub Pages Structure

### Per-Repo `_config.yml`

```yaml
theme: minima
title: "Excess Inflation Signal"
description: "Systematic macro overlay using CPI vs. inflation target"
baseurl: "/01-excess-inflation"
url: "https://macro-signal-strategies.github.io"
show_excerpts: true
```

### Per-Repo `index.md` Template

```markdown
---
layout: default
title: [Strategy Name]
---

## Abstract
[2-3 sentences: signal, hypothesis, key result]

## Theory
[Economic logic — why this signal should work]

## Signal Construction
**Formula:** Excess Inflation = (CPI₆ₘ/₆ₘ − Target) / max(Target, 2%)

## Data
| Series | Source | Vintage-Safe |
|--------|--------|-------------|
| CPIAUCSL | ALFRED | ✅ |

## Results
![Cumulative PnL](assets/charts/pnl_cumulative.png)

| Metric | Strategy | Long-Only |
|--------|----------|-----------|
| Sharpe | 0.94 | 0.58 |
| Sortino | 1.37 | 0.76 |
| Max DD | -12% | -34% |

## Open in Colab
[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](LINK)

## Limitations
- ALFRED vintage gaps pre-1995
- ETF proxies not futures (basis risk)
- US-centric inflation target assumptions
```

### Hub Site `docs/index.md`

```markdown
# Macro Signal Strategies

Open-source systematic macro trading research.
Each strategy uses vintage-safe ALFRED data + VectorBT backtesting.

## Strategy Library

| # | Strategy | Signal | Assets |
|---|---|---|---|
| 1 | [Excess Inflation](../01-excess-inflation) | CPI vs target | Equity overlay, IRS, FX |
| 2 | [Yield Curve](../02-yield-curve) | 10Y–2Y slope | Duration, equity timing |
| 3 | [Real Yield](../03-real-yield) | Nominal − breakeven | Bond RV, FX |
| 4 | [Credit Cycle](../04-credit-cycle) | Credit vs GDP trend | Equity vs credit |
| 5 | [Labor Market](../05-labor-market) | Payrolls vs labor force | Equity, FX |
| 6 | [Money Supply](../06-money-supply) | Real M2 growth | Equity timing |
| 7 | [Financial Conditions](../07-financial-conditions) | NFCI level + change | Equity beta |
| 8 | [Investment Clock](../08-investment-clock) | Growth × Inflation | Multi-asset rotation |

## Framework
- [ALFRED Vintage Methodology](framework/alfred.md)
- [Signal Normalisation Standard](framework/signals.md)
- [VectorBT Configuration Guide](framework/vectorbt.md)
```

---

## 12. Strategy Roadmap & Build Order

### Build Sequence

| Order | Repo | Reason |
|---|---|---|
| **1st** | `00-framework` | Shared tools — ALFRED client, signal normaliser, VectorBT wrapper, chart templates |
| **2nd** | `01-excess-inflation` | Flagship — most theory, cleanest signal, sets the template |
| **3rd** | `02-yield-curve` | Simpler data, strong literature, good contrast |
| **4th** | `03-real-yield` | Extends yield curve with breakeven inflation |
| **5th** | `04-credit-cycle` | Adds credit data layer |
| **6th** | `05-labor-market` | Employment signal |
| **7th** | `06-money-supply` | M2 real growth timing |
| **8th** | `07-financial-conditions` | NFCI overlay |
| **Last** | `08-investment-clock` | Aggregates all prior signals — natural capstone |

### Full Strategy Reference

| # | Repo Name | Signal | Assets | Key ALFRED Series |
|---|---|---|---|---|
| 1 | `01-excess-inflation` | CPI vs target | Equity overlay, IRS, FX | `CPIAUCSL`, `CPILFESL`, `FEDFUNDS` |
| 2 | `02-yield-curve` | 10Y–2Y slope | Duration, equity timing | `T10Y2Y`, `GS10`, `GS2` |
| 3 | `03-real-yield` | Nominal − breakeven | Bond RV, FX | `GS5`, `T5YIE`, `DFII5` |
| 4 | `04-credit-cycle` | Private credit vs GDP | Equity vs credit | `TOTLL`, `GDPC1`, `M2SL` |
| 5 | `05-labor-market` | Payrolls vs labor force | Equity, FX | `PAYEMS`, `UNRATE`, `NROU` |
| 6 | `06-money-supply` | Real M2 growth | Equity timing | `M2SL`, `CPIAUCSL` |
| 7 | `07-financial-conditions` | NFCI level + change | Equity beta overlay | `NFCI`, `NFCILEVERAGE` |
| 8 | `08-investment-clock` | Growth × Inflation 4-quadrant | Multi-asset rotation | All of the above |

---

## 13. First Task for Claude Code / Cowork

**Immediate actions — in this order:**

1. Create the GitHub organisation folder structure locally (all 9 repos + docs hub)
2. Scaffold `00-framework/` with:
   - `alfred_client.py` (vintage pull + information state builder)
   - `signal_builder.py` (normalise_signal, excess_signal, composite functions)
   - `reporting.py` (standard chart templates)
   - `requirements.txt`
3. Scaffold `01-excess-inflation/` fully:
   - All 4 notebook shells with markdown section headers pre-populated
   - `README.md` with Colab badges
   - `index.md` for GitHub Pages
   - `_config.yml`
   - `src/` files mirroring `00-framework/`
4. Repeat scaffold for all remaining repos (2–8) using same template
5. Build `docs/index.md` hub site

**Standard README badge block (insert at top of every README.md):**

```markdown
![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](COLAB_LINK)
[![Pages](https://img.shields.io/badge/GitHub-Pages-orange)](PAGES_LINK)
```

---

## 14. Key Design Principles

1. **No lookahead bias** — always use ALFRED vintages, always lag signal by 1 period
2. **Point-in-time format** — signals reflect what was published and known at each date
3. **Regime awareness** — note when signal doesn't apply (ZLB regimes, Japan exception)
4. **Intellectual honesty** — every notebook ends with a limitations section
5. **Reproducibility** — all data pulls cached to Drive, seeds set, versions pinned
6. **Modularity** — `00-framework` is the single source of truth for shared logic
7. **Pages-first** — every notebook exports publication-ready charts automatically

---

*Generated from planning session: April 2026*
*Tools: ALFRED (St. Louis Fed) + VectorBT + Google Colab + GitHub Pages*
*Inspired by: Macrosynergy quantamental research methodology*
