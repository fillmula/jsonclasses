from __future__ import annotations
from typing import TYPE_CHECKING, Callable
from inspect import signature
from ..fdef import FStore, Fdef
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class SetterModifier(Modifier):
    """Setter modifier provides setter to a calculated field."""

    def __init__(self, calc: Callable | Types) -> None:
        from ..types import Types
        self.calc = calc
        if not isinstance(calc, Types):
            if not callable(calc):
                raise ValueError('setter is not callable')
            params_len = len(signature(calc).parameters)
            if params_len != 2:
                raise ValueError('not a valid setter')

    def define(self, fdef: Fdef) -> None:
        fdef._fstore = FStore.CALCULATED
        fdef._setter = self.calc
