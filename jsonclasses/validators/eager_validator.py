"""module for eager validator."""
from .validator import Validator
from ..fdef import Fdef


class EagerValidator(Validator):
    """An EagerValidator marks fields for initialization and set stage validation.
    This is used usually before heavy transforming validators.
    """

    def define(self, fdef: Fdef) -> None:
        fdef._has_eager_validator = True
