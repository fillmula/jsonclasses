"""module for setonsave modifier."""
from __future__ import annotations
from typing import Callable, Any, TYPE_CHECKING
from inspect import signature
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class SetOnSaveModifier(Modifier):
    """Set on save modifier updates or sets value on save."""

    def __init__(self, setter: Callable | Types) -> None:
        from ..types import Types
        if not isinstance(setter, Types):
            if not callable(setter):
                raise ValueError('setonsave setter is not callable')
            params_len = len(signature(setter).parameters)
            if params_len > 1:
                raise ValueError('not a valid setonsave setter')
        self.setter = setter

    def serialize(self, ctx: Ctx) -> Any:
        if callable(self.setter):
            params_len = len(signature(self.setter).parameters)
            if params_len == 1:
                return self.setter(ctx.val)
            return self.setter()
        else:
            return self.setter.modifier.transform(ctx)
