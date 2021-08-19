"""module for readonly validator."""
from ..fdef import Fdef
from .validator import Validator


class UseForValidator(Validator):
    """Primary validator marks a field as the primary key."""

    def __init__(self, usage: str) -> None:
        self.usage = usage

    def define(self, fdef: Fdef) -> None:
        fdef._usage = self.usage
