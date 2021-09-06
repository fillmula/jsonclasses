"""module for alnum modifier."""
from __future__ import annotations
from ..fdef import Fdef, FieldType
from .modifier import Modifier


class AnyModifier(Modifier):
    """Field marked with any modifier can be any value."""

    def define(self, fdef: Fdef) -> None:
        fdef._field_type = FieldType.ANY
