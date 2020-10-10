"""module for eager validator."""
from .validator import Validator
from ..fields import FieldDescription


class EagerValidator(Validator):
    """An EagerValidator marks fields for initialization and set stage validation.
    This is used usually before heavy transforming validators.
    """

    def define(self, fdesc: FieldDescription) -> None:
        fdesc.has_eager_validator = True
