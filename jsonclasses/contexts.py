"""This module defines JSON Class context objects."""
from __future__ import annotations
from typing import Any, NamedTuple, TYPE_CHECKING
if TYPE_CHECKING:
    from .config import Config


class TransformingContext(NamedTuple):
    """The context on which transforming is performing. It contains necessary
    information for validators to transform the field values correctly.
    """
    value: Any
    keypath: str
    root: Any
    all_fields: bool
    config: Config
