"""Strategy composite -- imports the framework helpers."""

import sys
from pathlib import Path

_FRAMEWORK = Path(__file__).resolve().parents[2] / "00-framework"
if str(_FRAMEWORK) not in sys.path:
    sys.path.insert(0, str(_FRAMEWORK))

from src.composite import *  # type: ignore  # noqa: F401,F403,E402
