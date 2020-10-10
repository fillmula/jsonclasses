"""module for referee validator."""
from ..fields import FieldDescription
from .validator import Validator


class RefereeValidator(Validator):
    """Readwrite validator marks a reference field with a referee name."""

    def __init__(self, referee_key: str) -> None:
        self.referee_key = referee_key

    def define(self, fdesc: FieldDescription) -> None:
        fdesc.join_table_referee_key = self.referee_key
