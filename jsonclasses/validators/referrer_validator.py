"""module for referrer validator."""
from typing import Any
from ..field_description import FieldDescription
from ..config import Config
from .validator import Validator


class ReferrerValidator(Validator):
    """Readwrite validator marks a reference field with a referrer name."""

    def __init__(self, referrer_key: str) -> None:
        self.referrer_key = referrer_key

    def define(self, field_description: FieldDescription) -> None:
        field_description.join_table_referrer_key = self.referrer_key

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        pass
