"""module for before modifier."""
from __future__ import annotations
from typing import Union, TYPE_CHECKING
from datetime import date, datetime
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class BeforeModifier(Modifier):
    """Before modifier validates date against before date."""

    def __init__(self, point: Union[date, datetime]) -> None:
        self.point = point

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        if type(ctx.val) is date and type(self.point) is date:
            if ctx.val >= self.point:
                ctx.raise_vexc('value is too late')
        if type(ctx.val) is datetime and type(self.point) is datetime:
            if ctx.val >= self.point:
                ctx.raise_vexc('value is too late')
        else:
            value = ctx.val
            point = self.point
            if type(ctx.val) is date:
                value = datetime.combine(ctx.val, datetime.min.time())
            if type(self.point) is date:
                point = datetime.combine(self.point, datetime.min.time())
            if value >= point:
                ctx.raise_vexc('value is too late')
