"""module for assigning operator directly validator."""
from typing import TYPE_CHECKING
from ..exceptions import ValidationException
from .validator import Validator
from ..ctx import Ctx
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
        if ctx.owner.is_new or ctx.keypath_owner in ctx.owner.modified_fields:
            if ctx.value is None:
                raise ValidationException(
                    keypath_messages={
                        ctx.keypath_root: "no operator being assigned"},
                    root=ctx.root)
