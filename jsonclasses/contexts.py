"""This module defines JSON Class context objects."""
from __future__ import annotations
from typing import Any, NamedTuple, TypeVar, Optional, Generic, TYPE_CHECKING
if TYPE_CHECKING:
    from .config import Config
    from .json_object import JSONObject
    T = TypeVar('T', bound=JSONObject)


class TransformingContext(NamedTuple, Generic[T]):
    """The context on which transforming is performing. It contains necessary
    information for validators to transform the field values correctly.

    During transforming, eager validations are performed when needed. So all
    items from validating context are required for transforming.
    """
    value: Any
    keypath: str
    root: Any
    all_fields: bool
    config: Config
    dest: Optional[T] = None
    fill_dest_blanks: bool = True


class ValidatingContext(NamedTuple):
    """The context on which validating is performing. It contains necessary
    information for validators to validate the field values correctly.
    """
    value: Any
    keypath: str
    root: Any
    all_fields: bool
    config: Config


class ToJSONContext(NamedTuple):
    """The context on which `tojson` is performing. It contains necessary
    information for validators to convert the field values to JSON correctly.
    """
    value: Any
    config: Config
    ignore_writeonly: bool = False
