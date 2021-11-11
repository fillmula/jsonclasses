"""module for oneof modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable
from ..excs import ValidationException
from .modifier import Modifier
if TYPE_CHECKING:
    from ..types import Types
    from ..ctx import Ctx


class OneOfModifier(Modifier):
    """One of modifier validates value against a list of available values."""

    def __init__(self, choices: list[Any] | Callable | Types) -> None:
        self.choices = choices

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        choices = self.resolve_param(self.choices, ctx)
        if ctx.val is not None and ctx.val not in choices:
            ctx.raise_vexc(f'value is not in choices')
