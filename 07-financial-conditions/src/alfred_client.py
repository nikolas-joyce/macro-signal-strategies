"""Thin shim that re-exports the framework ALFRED client."""

import sys
from pathlib import Path

_FRAMEWORK = Path(__file__).resolve().parents[2] / "00-framework"
if str(_FRAMEWORK) not in sys.path:
    sys.path.insert(0, str(_FRAMEWORK))

from src.alfred_client import (  # type: ignore  # noqa: F401,E402
    get_alfred_vintages,
    build_information_state,
    cache_vintages,
    load_cached_vintages,
)
