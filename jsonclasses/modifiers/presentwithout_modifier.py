"""module for required modifier."""
from __future__ import annotations
from typing import Union, TYPE_CHECKING
from ..excs import ValidationException
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class PresentWithoutModifier(Modifier):
    """Fields marked with presentwithout modifier are forced presented if
    referring field is not present. If referring field has None value, this
    field's value should be present. If referring field has non None value,
    value of this field is not forced to be present.
    """

    def __init__(self, referring_keys: Union[str, list[str]]) -> None:
        if isinstance(referring_keys, str):
            self.referring_keys = [referring_keys]
        else:
            self.referring_keys = referring_keys

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is not None:
            return
        for key in self.referring_keys:
            try:
                referred_value = getattr(ctx.owner, key)
            except AttributeError:
                raise ValueError('unexist referring key '
                                 f'\'{key}\' '
                                 'passed to present without modifier')
            if referred_value is not None:
                return
        if ctx.val is None:
            ctx.raise_vexc(f'value is not present without {self.referring_keys}')
