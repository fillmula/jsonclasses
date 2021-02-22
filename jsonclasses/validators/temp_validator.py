"""module for temp validator."""
from .validator import Validator
from ..field_definition import FieldDefinition


class TempValidator(Validator):
    """A temp validator marks a field as temporary field. Value of temporary
    field is never written to database. As long as database write happens,
    temporary fields' values are set to None.
    """

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.is_temp_field = True
