"""module for modifier modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..fdef import Fdef, FieldType
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class TypeModifier(Modifier):
    """Abstract modifier for checking object's type."""

    def __init__(self) -> None:
        self.cls: type = object
        self.field_type: FieldType = FieldType.ANY
        self.exact_type: bool = False

    def define(self, fdef: Fdef) -> None:
        fdef._field_type = self.field_type

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        if self.exact_type:
            if type(ctx.val) is self.cls:
                return
        else:
            if isinstance(ctx.val, self.cls):
                return
        ctx.raise_vexc(f'value is not {self.cls.__name__}')