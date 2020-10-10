"""module for linkedthru validator."""
from ..fields import FieldDescription, FieldStorage
from .validator import Validator


class LinkedThruValidator(Validator):
    """Linked by validator marks a field linked with a joinning table."""

    def __init__(self, foreign_key: str) -> None:
        self.foreign_key = foreign_key

    def define(self, fdesc: FieldDescription) -> None:
        fdesc.field_storage = FieldStorage.FOREIGN_KEY
        fdesc.foreign_key = self.foreign_key
        fdesc.use_join_table = True
