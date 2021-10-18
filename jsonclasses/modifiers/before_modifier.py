"""module for before modifier."""
from __future__ import annotations
from typing import Callable, Union, TYPE_CHECKING
from datetime import date, datetime
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types

class BeforeModifier(Modifier):
    """Before modifier validates date against before date."""

    def __init__(self, point: date | datetime | Callable | Types) -> None:
        self.point = point

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        value = ctx.val
        point = self.resolve_param(self.point, ctx)
        if type(value) is date:
            value = datetime.combine(ctx.val, datetime.min.time())
        if type(point) is date:
            point = datetime.combine(self.resolve_param(self.point, ctx), datetime.min.time())
        if point is None:
            return ctx.val
        if value >= point:
            ctx.raise_vexc('value is too late')
