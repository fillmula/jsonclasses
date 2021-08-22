"""module for alpha validator."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..exceptions import ValidationException
from .validator import Validator
from ..ctx import Ctx


class AlphaValidator(Validator):
    """Alpha validator raises if value is not a alpha."""

    def validate(self, ctx: Ctx) -> None:
        if ctx.value is None:
            return
        value = ctx.value
        if not value.isalpha():
            kp = ctx.keypath_root
            raise ValidationException(
                {kp: f'product_name \'{value}\' at \'{kp}\' is not a alpha.'},
                ctx.root
            )
