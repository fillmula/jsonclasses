"""module for email modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from re import compile, match
from ..excs import ValidationException
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class EmailModifier(Modifier):
    """Email modifier raises if value is not valid email."""

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        value = ctx.val
        regex = compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        )


        if match(regex, value) is None:
            kp = '.'.join([str(k) for k in ctx.keypathr])
            raise ValidationException(
                {kp: f'value is not email string'},
                ctx.root
            )
