"""Shared framework for macro signal strategies."""

from .alfred_client import (
    get_alfred_vintages,
    build_information_state,
    cache_vintages,
    load_cached_vintages,
)
from .signal_builder import (
    normalise_signal,
    excess_inflation_signal,
    excess_signal,
    yield_curve_slope,
    real_yield,
    credit_excess,
    real_m2_growth,
)
from .composite import (
    build_composite,
    investment_clock_regime,
    regime_to_asset,
    risk_parity_weights,
    REGIME_ASSET_MAP,
)
from .reporting import (
    plot_signal,
    plot_cumulative_pnl,
    plot_drawdown,
    plot_signal_vs_forward_returns,
    performance_metrics,
    metrics_table_markdown,
    save_all_figures,
)

__version__ = "0.1.0"
