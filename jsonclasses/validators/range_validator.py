"""module for range validator."""
from __future__ import annotations
from typing import Union, TYPE_CHECKING
from .validator import Validator
from .min_validator import MinValidator
from .max_validator import MaxValidator
if TYPE_CHECKING:
    from ..ctx import Ctx


class RangeValidator(Validator):
    """A range validator validates value against a range."""

    def __init__(self, min: Union[int, float], max: Union[int, float]):
        self.min = min
        self.max = max

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        MinValidator(self.min).validate(ctx)
        MaxValidator(self.max).validate(ctx)
