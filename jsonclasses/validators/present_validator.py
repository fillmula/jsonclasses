"""module for required validator."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..fdef import Fdef
from ..exceptions import ValidationException
from .validator import Validator
if TYPE_CHECKING:
    from ..ctx import Ctx


class PresentValidator(Validator):
    """Present validator marks a field as present. When validating, if no value
    is present in this field, validation will fail. This is useful for foreign
    key fields to do required validation.
    """

    def define(self, fdef: Fdef) -> None:
        fdef._required = True

    def validate(self, ctx: Ctx) -> None:
        if ctx.value is None:
            raise ValidationException(
                {'.'.join([str(k) for k in ctx.keypathr]): (f'Value at \'{kp}\''
                                        ' should be present.')},
                ctx.root)
