"""module for referrer validator."""
from ..field_definition import FieldDefinition
from .validator import Validator


class ReferrerValidator(Validator):
    """Readwrite validator marks a reference field with a referrer name."""

    def __init__(self, referrer_key: str) -> None:
        self.referrer_key = referrer_key

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.join_table_referrer_key = self.referrer_key
