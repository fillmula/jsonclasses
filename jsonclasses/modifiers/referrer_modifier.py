"""module for referrer modifier."""
from ..fdef import FDef
from .modifier import Modifier


class ReferrerModifier(Modifier):
    """Readwrite modifier marks a reference field with a referrer name."""

    def __init__(self, referrer_key: str) -> None:
        self.referrer_key = referrer_key

    def define(self, fdef: FDef) -> None:
        fdef._join_table_referrer_key = self.referrer_key
