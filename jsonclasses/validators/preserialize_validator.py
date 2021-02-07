"""module for preserialize validator."""
from .validator import Validator
from ..fields import FieldDescription


class PreserializeValidator(Validator):
    """A PreserializeValidator tweaks field validation logic. Every validator
    after a preserialize validator are only triggered just before serialization
    into database.

    This is usually used before setonsave validator.
    """

    def define(self, fdesc: FieldDescription) -> None:
        fdesc.has_preserialize_validator = True
