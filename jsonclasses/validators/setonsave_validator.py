"""module for setonsave validator."""
from __future__ import annotations
from typing import Callable, Any, TYPE_CHECKING
from inspect import signature
from .validator import Validator
if TYPE_CHECKING:
    from ..ctx import Ctx


class SetOnSaveValidator(Validator):
    """Setonsave validator updates or sets value on save."""

    def __init__(self, setter: Callable) -> None:
        if not callable(setter):
            raise ValueError('setonsave setter is not callable')
        params_len = len(signature(setter).parameters)
        if params_len > 1:
            raise ValueError('not a valid setonsave setter')
        self.setter = setter

    def serialize(self, ctx: Ctx) -> Any:
        params_len = len(signature(self.setter).parameters)
        if params_len == 1:
            return self.setter(ctx.val)
        return self.setter()
