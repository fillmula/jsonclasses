"""module for required modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..excs import ValidationException
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class PresentWithModifier(Modifier):
    """Fields marked with presentwith modifier are forced presented if
    referring field is present. If referring field has None value, this field's
    value is optional. If referring field has non None value, value of this
    field is required.
    """

    def __init__(self, referring_key: str) -> None:
        self.referring_key = referring_key

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is not None:
            return
        try:
            referred_value = getattr(ctx.owner, self.referring_key)
        except AttributeError:
            raise ValueError(f'unexist referring key \'{self.referring_key}\' '
                             'passed to present with modifier')
        if referred_value is not None and ctx.val is None:
            ctx.raise_vexc(f"value is not present with '{self.referring_key}'")
