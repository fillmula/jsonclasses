"""module for unresolved validator."""
from ..fdef import Fdef
from .validator import Validator


class UnresolvedValidator(Validator):
    """This validator contains unresolved names."""

    def __init__(self, arg: str) -> None:
        self.arg = arg

    def define(self, fdef: Fdef) -> None:
        fdef._unresolved = True
        fdef._unresolved_name = self.arg
