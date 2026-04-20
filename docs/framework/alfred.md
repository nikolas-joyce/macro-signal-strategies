---
layout: default
title: ALFRED Vintage Methodology
---

# ALFRED Vintage Methodology

## The Problem
Standard FRED serves **revised** data. Backtesting on revised data overstates signal quality because traders in 2005 did not have the 2024-vintage CPI estimate - they had what was published in 2005.

## The Solution: Information State Construction
For each date t, use only the vintage of the data that was publicly available as of t.

1. Pull every vintage available from ALFRED.
2. For each observation date, find the earliest vintage whose release date is >= the observation date.
3. Use that vintage's value as the "known" value at t.
4. Apply a 1-period lag before the value enters any trading signal.

## Implementation

```python
import requests
import pandas as pd

def get_alfred_vintages(series_id, api_key, start='1990-01-01'):
    url = "https://api.stlouisfed.org/fred/series/vintagedates"
    params = {'series_id': series_id, 'api_key': api_key, 'file_type': 'json'}
    vintage_dates = requests.get(url, params=params).json()['vintage_dates']

    all_vintages = {}
    for vdate in vintage_dates:
        obs_url = "https://api.stlouisfed.org/fred/series/observations"
        obs_params = {
            'series_id': series_id, 'api_key': api_key,
            'file_type': 'json', 'vintage_dates': vdate,
            'observation_start': start,
        }
        obs = requests.get(obs_url, params=obs_params).json()['observations']
        all_vintages[vdate] = {o['date']: float(o['value'])
                               for o in obs if o['value'] != '.'}

    return pd.DataFrame(all_vintages)
```

See `00-framework/src/alfred_client.py` for the canonical implementation plus caching helpers.

## Vintage Coverage Caveats
- Daily/weekly series have thousands of vintages - pulls are slow. Cache everything.
- Coverage is thin pre-1995 for many series.
- Some series (e.g. quarterly GDP revisions) have unusually large revision magnitudes; quality-check before trusting.
