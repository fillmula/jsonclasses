"""module for writenonnull validator."""
from ..field_definition import FieldDefinition, WriteRule
from .validator import Validator


class WriteNonnullValidator(Validator):
    """Write nonnull validator marks a field as writenonnull. Fields are
    allowed to be modified. However, nil value won't be set.
    """

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.write_rule = WriteRule.WRITE_NONNULL
