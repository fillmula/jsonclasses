"""module for after modifier."""
from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from datetime import date, datetime
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class AfterModifier(Modifier):
    """After modifier validates date against after date."""

    def __init__(self, point: date | datetime | Callable | Types) -> None:
        self.point = point

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        value = ctx.val
        point = self.resolve_param(self.point, ctx)
        if type(value) is date and type(point) is date:
            if value <= point:
                ctx.raise_vexc('value is too early')
        if type(value) is datetime and type(point) is datetime:
            if value <= point:
                ctx.raise_vexc('value is too early')
        else:
            value = value
            point = point
            if type(value) is date:
                value = datetime.combine(value, datetime.min.time())
            if type(point) is date:
                point = datetime.combine(point, datetime.min.time())
            if value <= point:
                ctx.raise_vexc('value is too early')
