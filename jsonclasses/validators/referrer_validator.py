"""module for referrer validator."""
from ..fdef import Fdef
from .validator import Validator


class ReferrerValidator(Validator):
    """Readwrite validator marks a reference field with a referrer name."""

    def __init__(self, referrer_key: str) -> None:
        self.referrer_key = referrer_key

    def define(self, fdef: Fdef) -> None:
        fdef._join_table_referrer_key = self.referrer_key
