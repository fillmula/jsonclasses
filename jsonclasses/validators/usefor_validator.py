"""module for readonly validator."""
from ..fields import FieldDescription
from .validator import Validator


class UseForValidator(Validator):
    """Primary validator marks a field as the primary key."""

    def __init__(self, usage: str) -> None:
        self.usage = usage

    def define(self, fdesc: FieldDescription) -> None:
        fdesc.usage = self.usage
