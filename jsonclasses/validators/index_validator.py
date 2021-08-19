"""module for index validator."""
from .validator import Validator
from ..fdef import Fdef


class IndexValidator(Validator):
    """Index validator implies this column should be indexed in database."""

    def define(self, fdef: Fdef) -> None:
        fdef._index = True
