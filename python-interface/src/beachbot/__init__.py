#   -------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------
"""Python Package Template"""
from __future__ import annotations
from importlib.metadata import version as _version, PackageNotFoundError

try:
    __version__ = _version(__name__)
except PackageNotFoundError:
    pass


__all__ = ["manipulators", "sensors"] # "sensors", "platforms"

from . import manipulators
from . import sensors

from . import utils
