"""module for linkedby validator."""
from ..fields import FieldDescription, FieldStorage
from .validator import Validator


class LinkedByValidator(Validator):
    """Linked by validator marks a field linked with a foreign key."""

    def __init__(self, foreign_key: str) -> None:
        self.foreign_key = foreign_key

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_storage = FieldStorage.FOREIGN_KEY
        field_description.foreign_key = self.foreign_key
        field_description.use_join_table = False
