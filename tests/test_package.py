from __future__ import annotations

import importlib.metadata

import paleoconnect as m


def test_version() -> None:
    assert importlib.metadata.version("paleoconnect") == m.__version__
