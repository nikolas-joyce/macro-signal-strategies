"""Thin shim that re-exports the framework ALFRED client.

Add strategy-specific overrides below (e.g. custom vintage caching,
alternative release-date logic) without modifying the framework.
"""

import sys
from pathlib import Path

# Allow `from src.alfred_client import ...` both when running from the repo
# root and when sys.path already includes the framework directory.
_FRAMEWORK = Path(__file__).resolve().parents[2] / "00-framework"
if str(_FRAMEWORK) not in sys.path:
    sys.path.insert(0, str(_FRAMEWORK))

from src.alfred_client import (  # type: ignore  # noqa: F401,E402
    get_alfred_vintages,
    build_information_state,
    cache_vintages,
    load_cached_vintages,
)
