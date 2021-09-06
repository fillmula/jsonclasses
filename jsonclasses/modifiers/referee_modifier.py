"""module for referee modifier."""
from ..fdef import Fdef
from .modifier import Modifier


class RefereeModifier(Modifier):
    """Readwrite modifier marks a reference field with a referee name."""

    def __init__(self, referee_key: str) -> None:
        self.referee_key = referee_key

    def define(self, fdef: Fdef) -> None:
        fdef._join_table_referee_key = self.referee_key
