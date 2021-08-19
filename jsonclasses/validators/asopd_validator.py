"""module for assigning operator directly validator."""
from typing import Any
from ..exceptions import ValidationException
from .validator import Validator
from ..ctxs import VCtx
from ..fdef import Fdef


class AsopdValidator(Validator):
    """Assigning operator directly validator assigns the operator to the
    current field directly.
    """

    def define(self, fdef: Fdef) -> None:
        fdef._requires_operator_assign = True

    def validate(self, context: VCtx) -> None:
        if context.owner.is_new or context.keypath_owner in context.owner.modified_fields:
            if context.value is None:
                raise ValidationException(
                    keypath_messages={
                        context.keypath_root: "no operator being assigned"},
                    root=context.root)
