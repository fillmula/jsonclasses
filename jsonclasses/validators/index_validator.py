"""module for index validator."""
from .validator import Validator
from ..field_definition import FieldDefinition


class IndexValidator(Validator):
    """Index validator implies this column should be indexed in database."""

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.index = True
