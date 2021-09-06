"""module for oneof modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any
from ..excs import ValidationException
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class OneOfModifier(Modifier):
    """One of modifier validates value against a list of available values."""

    def __init__(self, choices: list[Any]) -> None:
        self.choices = choices

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is not None and ctx.val not in self.choices:
            ctx.raise_vexc(f'value is not in {self.choices}')
