"""module for linkedthru validator."""
from ..fields import FieldDescription, FieldStorage
from .validator import Validator
from ..contexts import ValidatingContext


class LinkedThruValidator(Validator):
    """Linked by validator marks a field linked with a joinning table."""

    def __init__(self, foreign_key: str) -> None:
        self.foreign_key = foreign_key

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_storage = FieldStorage.FOREIGN_KEY
        field_description.foreign_key = self.foreign_key
        field_description.use_join_table = True

    def validate(self, context: ValidatingContext) -> None:
        pass
