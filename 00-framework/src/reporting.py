"""
reporting.py
============
Standard chart and table templates for publication to GitHub Pages.

All figures render in a consistent, press-ready style and save to
`assets/charts/` as 1200x700 PNGs at 150 dpi by default.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

import numpy as np
import pandas as pd

# Matplotlib import guarded so the module imports cleanly in environments
# (e.g. doc builds) without a display backend.
try:
    import matplotlib.pyplot as plt
    _HAS_MPL = True
except ImportError:  # pragma: no cover
    _HAS_MPL = False

PLOT_DEFAULTS = {
    "figsize": (12, 7),
    "dpi": 150,
    "grid_alpha": 0.25,
    "title_fontsize": 14,
    "label_fontsize": 11,
    "colors": [
        "#1f4e79",  # deep blue
        "#c0392b",  # brick red
        "#27ae60",  # emerald
        "#d68910",  # amber
        "#6c3483",  # purple
        "#7f8c8d",  # grey
    ],
}


def _apply_style(ax) -> None:
    ax.grid(True, alpha=PLOT_DEFAULTS["grid_alpha"])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def _ensure_mpl() -> None:
    if not _HAS_MPL:
        raise ImportError(
            "matplotlib is required for reporting. Install with "
            "`pip install matplotlib`."
        )


# ---------------------------------------------------------------------------
# Signal visualisation
# ---------------------------------------------------------------------------
def plot_signal(
    signal: pd.Series,
    title: str = "Signal",
    ylabel: str = "Z-score",
    events: Optional[dict[str, str]] = None,
    save_path: Optional[str | Path] = None,
):
    """Line plot of a signal with optional named macro-event vlines."""
    _ensure_mpl()
    fig, ax = plt.subplots(figsize=PLOT_DEFAULTS["figsize"],
                           dpi=PLOT_DEFAULTS["dpi"])
    ax.plot(signal.index, signal.values,
            color=PLOT_DEFAULTS["colors"][0], linewidth=1.4)
    ax.axhline(0, color="black", linewidth=0.6, alpha=0.4)

    if events:
        for label, date in events.items():
            d = pd.to_datetime(date)
            ax.axvline(d, linestyle="--", alpha=0.35, color="grey")
            ax.text(d, ax.get_ylim()[1] * 0.92, label,
                    rotation=90, fontsize=9, alpha=0.7)

    ax.set_title(title, fontsize=PLOT_DEFAULTS["title_fontsize"])
    ax.set_ylabel(ylabel, fontsize=PLOT_DEFAULTS["label_fontsize"])
    _apply_style(ax)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, bbox_inches="tight")
    return fig


# ---------------------------------------------------------------------------
# Cumulative PnL
# ---------------------------------------------------------------------------
def plot_cumulative_pnl(
    returns: pd.DataFrame,
    title: str = "Cumulative PnL",
    save_path: Optional[str | Path] = None,
):
    """Cumulative log-return curves, one per column of `returns`."""
    _ensure_mpl()
    fig, ax = plt.subplots(figsize=PLOT_DEFAULTS["figsize"],
                           dpi=PLOT_DEFAULTS["dpi"])
    cum = (1 + returns.fillna(0)).cumprod()
    for i, col in enumerate(cum.columns):
        ax.plot(cum.index, cum[col],
                label=col,
                color=PLOT_DEFAULTS["colors"][i % len(PLOT_DEFAULTS["colors"])],
                linewidth=1.5)
    ax.set_title(title, fontsize=PLOT_DEFAULTS["title_fontsize"])
    ax.set_ylabel("Growth of $1", fontsize=PLOT_DEFAULTS["label_fontsize"])
    ax.legend(frameon=False)
    _apply_style(ax)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, bbox_inches="tight")
    return fig


# ---------------------------------------------------------------------------
# Drawdowns
# ---------------------------------------------------------------------------
def plot_drawdown(
    returns: pd.Series,
    title: str = "Drawdown",
    save_path: Optional[str | Path] = None,
):
    _ensure_mpl()
    cum = (1 + returns.fillna(0)).cumprod()
    peak = cum.cummax()
    dd = (cum / peak - 1) * 100

    fig, ax = plt.subplots(figsize=PLOT_DEFAULTS["figsize"],
                           dpi=PLOT_DEFAULTS["dpi"])
    ax.fill_between(dd.index, dd.values, 0,
                    color=PLOT_DEFAULTS["colors"][1], alpha=0.45)
    ax.set_title(title, fontsize=PLOT_DEFAULTS["title_fontsize"])
    ax.set_ylabel("Drawdown (%)", fontsize=PLOT_DEFAULTS["label_fontsize"])
    _apply_style(ax)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, bbox_inches="tight")
    return fig


# ---------------------------------------------------------------------------
# Performance metrics table
# ---------------------------------------------------------------------------
def performance_metrics(
    returns: pd.Series,
    freq: int = 252,
    benchmark: Optional[pd.Series] = None,
) -> dict:
    """Standard table of performance metrics for a single return series."""
    r = returns.dropna()
    ann_return = (1 + r.mean()) ** freq - 1
    ann_vol = r.std() * np.sqrt(freq)
    sharpe = ann_return / ann_vol if ann_vol > 0 else np.nan

    downside = r[r < 0].std() * np.sqrt(freq)
    sortino = ann_return / downside if downside > 0 else np.nan

    cum = (1 + r).cumprod()
    peak = cum.cummax()
    max_dd = (cum / peak - 1).min()

    calmar = ann_return / abs(max_dd) if max_dd < 0 else np.nan
    win_rate = (r > 0).mean()

    out = {
        "Annualised Return": round(ann_return, 4),
        "Annualised Vol": round(ann_vol, 4),
        "Sharpe": round(sharpe, 3),
        "Sortino": round(sortino, 3),
        "Max Drawdown": round(max_dd, 4),
        "Calmar": round(calmar, 3),
        "Win Rate": round(win_rate, 3),
    }
    if benchmark is not None:
        joined = pd.concat([r, benchmark], axis=1).dropna()
        joined.columns = ["strat", "bench"]
        if len(joined) > 5:
            out["Correlation vs Benchmark"] = round(
                joined["strat"].corr(joined["bench"]), 3
            )
    return out


def metrics_table_markdown(metrics: dict, title: str = "Performance") -> str:
    """Render a metrics dict as a GitHub-flavoured markdown table."""
    rows = "\n".join(f"| {k} | {v} |" for k, v in metrics.items())
    return f"### {title}\n\n| Metric | Value |\n|---|---|\n{rows}\n"


# ---------------------------------------------------------------------------
# Distribution & IC helpers
# ---------------------------------------------------------------------------
def plot_signal_vs_forward_returns(
    signal: pd.Series,
    forward_returns: pd.Series,
    quantiles: int = 5,
    title: str = "Signal Quintile Forward Returns",
    save_path: Optional[str | Path] = None,
):
    _ensure_mpl()
    df = pd.concat([signal, forward_returns], axis=1).dropna()
    df.columns = ["signal", "fwd_ret"]
    df["bucket"] = pd.qcut(df["signal"], quantiles, labels=False, duplicates="drop")
    means = df.groupby("bucket")["fwd_ret"].mean()

    fig, ax = plt.subplots(figsize=PLOT_DEFAULTS["figsize"],
                           dpi=PLOT_DEFAULTS["dpi"])
    ax.bar(means.index, means.values,
           color=PLOT_DEFAULTS["colors"][0], alpha=0.8)
    ax.set_xlabel("Signal Quantile (low -> high)")
    ax.set_ylabel("Mean Forward Return")
    ax.set_title(title, fontsize=PLOT_DEFAULTS["title_fontsize"])
    _apply_style(ax)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, bbox_inches="tight")
    return fig


def save_all_figures(
    figures: Iterable, out_dir: str | Path = "assets/charts"
) -> list[Path]:
    """Save a list of (name, Figure) tuples to PNG."""
    _ensure_mpl()
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for name, fig in figures:
        p = out_dir / f"{name}.png"
        fig.savefig(p, bbox_inches="tight", dpi=PLOT_DEFAULTS["dpi"])
        paths.append(p)
    return paths
