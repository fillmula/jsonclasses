"""module for validator validator."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..excs import ValidationException
from .validator import Validator
if TYPE_CHECKING:
    from ..ctx import Ctx


class InvalidValidator(Validator):
    """A validator that turns value into invalid."""

    def validate(self, ctx: Ctx) -> None:
        """Raises invalid exception."""
        raise ValidationException(
            {'.'.join([str(k) for k in ctx.keypathr]): f'value is invalid'},
            ctx.root
        )
