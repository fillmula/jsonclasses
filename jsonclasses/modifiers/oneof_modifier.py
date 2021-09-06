"""module for oneof modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any
from ..excs import ValidationException
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class OneOfModifier(Modifier):
    """One of modifier validates value against a list of available values."""

    def __init__(self, val_list: list[Any]) -> None:
        self.val_list = val_list

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return None
        if ctx.val not in self.val_list:
            raise ValidationException(
                {'.'.join([str(k) for k in ctx.keypathr]): f'value is not in {self.str_list}'},
                ctx.root
            )
