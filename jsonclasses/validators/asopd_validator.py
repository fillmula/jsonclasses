"""module for assigning operator directly validator."""
from typing import Any
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext
from ..fdef import Fdef


class AsopdValidator(Validator):
    """Assigning operator directly validator assigns the operator to the
    current field directly.
    """

    def define(self, fdef: Fdef) -> None:
        fdef.requires_operator_assign = True

    def validate(self, context: ValidatingContext) -> None:
        if context.owner.is_new or context.keypath_owner in context.owner.modified_fields:
            if context.value is None:
                raise ValidationException(
                    keypath_messages={
                        context.keypath_root: "no operator being assigned"},
                    root=context.root)
