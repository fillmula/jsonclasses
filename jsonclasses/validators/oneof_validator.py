"""module for oneof validator."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..exceptions import ValidationException
from .validator import Validator
if TYPE_CHECKING:
    from ..ctx import Ctx


class OneOfValidator(Validator):
    """One of validator validates value against a list of available values."""

    def __init__(self, str_list: list[str]) -> None:
        self.str_list = str_list

    def validate(self, ctx: Ctx) -> None:
        if ctx.value is None:
            return None
        if ctx.value not in self.str_list:
            raise ValidationException(
                {'.'.join([str(k) for k in ctx.keypathr]): f'Value \'{ctx.value}\' at \'{kp}\' should be one of {self.str_list}.'},
                ctx.root
            )
