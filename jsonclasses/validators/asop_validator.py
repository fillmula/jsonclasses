"""module for assigning operator validator."""
from typing import Callable
from inspect import signature
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext
from ..field_definition import FieldDefinition


class AsopValidator(Validator):
    """Assigning operator validator assigns the transfromed operator to the
    current field.
    """

    def __init__(self, transformer: Callable) -> None:
        if not callable(transformer):
            raise ValueError('asop transformer is not callable')
        params_len = len(signature(transformer).parameters)
        if params_len > 3 or params_len < 1:
            raise ValueError('not a valid asop transformer')
        self.transformer = transformer

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.requires_operator_assign = True
        fdesc.operator_assign_transformer = self.transformer

    def validate(self, context: ValidatingContext) -> None:
        if context.owner.is_new or context.keypath_owner in context.owner.modified_fields:
            if context.value is None:
                raise ValidationException(
                    keypath_messages={
                        context.keypath_root: "no operator being assigned"},
                    root=context.root)
