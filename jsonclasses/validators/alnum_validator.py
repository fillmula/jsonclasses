"""module for alnum validator."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..exceptions import ValidationException
from .validator import Validator
from ..ctx import Ctx


class AlnumValidator(Validator):
    """Alnum validator raises if value is not made up of alpha and number."""

    def validate(self, ctx: Ctx) -> None:
        if ctx.value is None:
            return
        value = ctx.value
        if not value.isalnum():
            kp = ctx.keypath_root
            raise ValidationException(
                {kp: f'product_code \'{value}\' at \'{kp}\' is not made up of alpha and number.'},
                ctx.root
            )
