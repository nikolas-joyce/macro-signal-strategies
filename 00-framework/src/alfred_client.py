"""
alfred_client.py
================
ALFRED (Archival FRED) API wrapper providing vintage-safe economic data.

The purpose of this module is to eliminate lookahead bias by reconstructing
the "information state" available at any historical date t -- i.e. the values
that were actually published and known to market participants as of t, rather
than the modern revised series.

Primary functions
-----------------
- get_alfred_vintages: Pull every vintage of a series that ALFRED exposes.
- build_information_state: Collapse the vintage matrix into a single point-in-time
  series suitable for backtesting (earliest-known-value-as-of-t logic).

Typical usage
-------------
>>> import os
>>> from alfred_client import get_alfred_vintages, build_information_state
>>> vintages = get_alfred_vintages('CPIAUCSL', os.environ['FRED_API_KEY'])
>>> cpi_pit  = build_information_state(vintages)
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Optional

import pandas as pd
import requests

FRED_BASE = "https://api.stlouisfed.org/fred"


# ---------------------------------------------------------------------------
# Low-level ALFRED pull
# ---------------------------------------------------------------------------
def get_alfred_vintages(
    series_id: str,
    api_key: str,
    start: str = "1990-01-01",
    sleep: float = 0.15,
) -> pd.DataFrame:
    """
    Pull every vintage of `series_id` from ALFRED.

    Parameters
    ----------
    series_id : str
        FRED/ALFRED series identifier, e.g. 'CPIAUCSL'.
    api_key : str
        FRED API key (free -- register at fred.stlouisfed.org).
    start : str, default '1990-01-01'
        Earliest observation date to request (`observation_start`).
    sleep : float, default 0.15
        Seconds to pause between vintage requests to respect rate limits.

    Returns
    -------
    pd.DataFrame
        Rows indexed by observation date, columns labelled by vintage date.
        Each cell is the value published for that obs_date in that vintage.
        Missing cells = not yet published / not available in that vintage.
    """
    # 1. List every vintage date ALFRED has for this series
    vdate_resp = requests.get(
        f"{FRED_BASE}/series/vintagedates",
        params={
            "series_id": series_id,
            "api_key": api_key,
            "file_type": "json",
        },
        timeout=30,
    )
    vdate_resp.raise_for_status()
    vintage_dates = vdate_resp.json()["vintage_dates"]

    # 2. For each vintage, pull the series as it looked on that date
    all_vintages: dict[str, dict[str, float]] = {}
    for vdate in vintage_dates:
        obs_resp = requests.get(
            f"{FRED_BASE}/series/observations",
            params={
                "series_id": series_id,
                "api_key": api_key,
                "file_type": "json",
                "vintage_dates": vdate,
                "observation_start": start,
            },
            timeout=30,
        )
        obs_resp.raise_for_status()
        obs = obs_resp.json()["observations"]
        all_vintages[vdate] = {
            o["date"]: float(o["value"])
            for o in obs
            if o["value"] not in (".", "", None)
        }
        time.sleep(sleep)

    df = pd.DataFrame(all_vintages)
    df.index = pd.to_datetime(df.index)
    df.columns = pd.to_datetime(df.columns)
    df = df.sort_index(axis=0).sort_index(axis=1)
    return df


# ---------------------------------------------------------------------------
# Point-in-time (information state) construction
# ---------------------------------------------------------------------------
def build_information_state(
    vintages: pd.DataFrame,
    lag_periods: int = 1,
) -> pd.DataFrame:
    """
    Collapse an ALFRED vintage matrix into a point-in-time DataFrame.

    For each observation date t, this returns the value of the series as it
    was first publicly available -- i.e. the earliest vintage whose release
    date is >= the observation date. An optional lag is then applied so the
    backtester can never peek at same-period data.

    Parameters
    ----------
    vintages : pd.DataFrame
        Output of `get_alfred_vintages` -- rows=obs_date, cols=vintage_date.
    lag_periods : int, default 1
        Additional integer lag (in observation periods) applied to the
        information-state series to guarantee no same-period lookahead.

    Returns
    -------
    pd.DataFrame
        Single-column DataFrame ['value'] indexed by observation date giving
        the lagged point-in-time value of the series.
    """
    if vintages.empty:
        return pd.DataFrame(columns=["value"])

    obs_dates = vintages.index
    vintage_dates = vintages.columns

    records: list[tuple[pd.Timestamp, Optional[float]]] = []
    for obs_date in obs_dates:
        # Earliest vintage published on or after the observation date
        eligible = vintage_dates[vintage_dates >= obs_date]
        if len(eligible) == 0:
            records.append((obs_date, None))
            continue
        first_vintage = eligible.min()
        val = vintages.loc[obs_date, first_vintage]
        records.append((obs_date, val))

    pit = pd.DataFrame(records, columns=["date", "value"]).set_index("date")
    pit["value"] = pd.to_numeric(pit["value"], errors="coerce")
    if lag_periods > 0:
        pit["value"] = pit["value"].shift(lag_periods)
    return pit


# ---------------------------------------------------------------------------
# Caching helpers
# ---------------------------------------------------------------------------
def cache_vintages(
    vintages: pd.DataFrame,
    series_id: str,
    out_dir: str | Path = "data/raw",
) -> Path:
    """Persist a vintage matrix to parquet for later reuse."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{series_id.lower()}_alfred_vintages.parquet"
    # Parquet requires string column labels
    to_save = vintages.copy()
    to_save.columns = [c.strftime("%Y-%m-%d") for c in to_save.columns]
    to_save.to_parquet(path)
    return path


def load_cached_vintages(
    series_id: str,
    in_dir: str | Path = "data/raw",
) -> pd.DataFrame:
    """Load a previously cached vintage matrix."""
    path = Path(in_dir) / f"{series_id.lower()}_alfred_vintages.parquet"
    df = pd.read_parquet(path)
    df.columns = pd.to_datetime(df.columns)
    return df
