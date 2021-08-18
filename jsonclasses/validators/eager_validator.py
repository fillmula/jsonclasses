"""module for eager validator."""
from .validator import Validator
from ..field_definition import FieldDefinition


class EagerValidator(Validator):
    """An EagerValidator marks fields for initialization and set stage validation.
    This is used usually before heavy transforming validators.
    """

    def define(self, fdef: FieldDefinition) -> None:
        fdef.has_eager_validator = True
