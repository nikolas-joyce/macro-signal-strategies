"""Strategy reporting -- inherits publication-ready charts from the framework."""

import sys
from pathlib import Path

_FRAMEWORK = Path(__file__).resolve().parents[2] / "00-framework"
if str(_FRAMEWORK) not in sys.path:
    sys.path.insert(0, str(_FRAMEWORK))

from src.reporting import (  # type: ignore  # noqa: F401,E402
    plot_signal,
    plot_cumulative_pnl,
    plot_drawdown,
    plot_signal_vs_forward_returns,
    performance_metrics,
    metrics_table_markdown,
    save_all_figures,
    PLOT_DEFAULTS,
)
