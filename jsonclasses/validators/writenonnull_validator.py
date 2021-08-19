"""module for writenonnull validator."""
from ..fdef import Fdef, WriteRule
from .validator import Validator


class WriteNonnullValidator(Validator):
    """Write nonnull validator marks a field as writenonnull. Fields are
    allowed to be modified. However, nil value won't be set.
    """

    def define(self, fdef: Fdef) -> None:
        fdef._write_rule = WriteRule.WRITE_NONNULL
