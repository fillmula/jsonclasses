"""module for assigning operator directly validator."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..exceptions import ValidationException
from .validator import Validator
from ..fdef import Fdef
if TYPE_CHECKING:
    from ..ctx import Ctx


class AsopdValidator(Validator):
    """Assigning operator directly validator assigns the operator to the
    current field directly.
    """

    def define(self, fdef: Fdef) -> None:
        fdef._requires_operator_assign = True

    def validate(self, ctx: Ctx) -> None:
        if ctx.root.is_new or ctx.keypathr[-1] in ctx.root.modified_fields:
            if ctx.value is None:
                raise ValidationException(
                    keypath_messages={
                        '.'.join([str(k) for k in ctx.keypathr]): "no operator being assigned"},
                    root=ctx.root)
