"""module for email modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from re import compile, match
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


email_regex = compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

class EmailModifier(Modifier):
    """Email modifier raises if value is not valid email."""

    def validate(self, ctx: Ctx) -> None:
        if isinstance(ctx.val, str) and match(email_regex, ctx.val) is None:
            ctx.raise_vexc('value is not email string')
