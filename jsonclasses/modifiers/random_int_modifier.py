"""module for random int modifier."""
from __future__ import annotations
from random import randrange
from typing import Any, TYPE_CHECKING, Callable, Union
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class RandomIntModifier(Modifier):
    """Random int modifier generates random int as result."""

    def __init__(self, min_value: int | float | Callable | Types,
                max_value: int | float | Callable | Types) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def transform(self, ctx: Ctx) -> Any:
        min_value = self.resolve_param(self.min_value, ctx)
        max_value = self.resolve_param(self.max_value, ctx)
        if min_value < max_value:
            return randrange(min_value, max_value)
        else:
            message = f'{min_value} is not less than or equal {max_value}'
        ctx.raise_vexc(message)
