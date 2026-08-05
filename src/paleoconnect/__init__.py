"""Copyright (c) 2026 Gonzalo Rodriguez Rizk. All rights reserved.

paleoconnect: Palaeogeographic connectivity analysis for biogeographic dispersal studies
"""

from __future__ import annotations

from ._version import version as __version__
from .landmasses import LandmassDefinitions
from .model import ConnectivityModel
from .result import ConnectivityResult

__all__ = [
    "ConnectivityModel",
    "ConnectivityResult",
    "LandmassDefinitions",
    "__version__",
]
