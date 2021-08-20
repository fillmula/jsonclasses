"""module for unresolved validator."""
from ..exceptions import ValidationException
from ..fdef import Fdef, FieldType
from ..ctx import Ctx
from .validator import Validator


class UnresolvedValidator(Validator):
    """This validator contains unresolved names."""

    def __init__(self, arg: str) -> None:
        self.arg = arg

    def define(self, fdef: Fdef) -> None:
        fdef._unresolved = True
        fdef._unresolved_name = self.arg
