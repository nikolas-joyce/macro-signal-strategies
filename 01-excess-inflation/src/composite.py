"""Composite re-export for this strategy repo.

The flagship repo typically uses only its own signal, but exposes the
framework composite helpers so researchers can quickly combine variants
(headline vs. core CPI, 3m vs. 6m, etc.).
"""

import sys
from pathlib import Path

_FRAMEWORK = Path(__file__).resolve().parents[2] / "00-framework"
if str(_FRAMEWORK) not in sys.path:
    sys.path.insert(0, str(_FRAMEWORK))

from src.composite import (  # type: ignore  # noqa: F401,E402
    build_composite,
    investment_clock_regime,
    regime_to_asset,
    risk_parity_weights,
    REGIME_ASSET_MAP,
)
