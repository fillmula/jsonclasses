"""module for writenonnull validator."""
from ..fields import FieldDescription, WriteRule
from .validator import Validator


class WriteNonnullValidator(Validator):
    """Write nonnull validator marks a field as writenonnull. Fields are
    allowed to be modified. However, nil value won't be set.
    """

    def define(self, field_description: FieldDescription) -> None:
        field_description.write_rule = WriteRule.WRITE_NONNULL