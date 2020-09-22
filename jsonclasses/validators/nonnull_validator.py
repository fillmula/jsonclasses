"""module for nonnull validator."""
from typing import Any
from .validator import Validator
from ..utils.nonnull_note import NonnullNote
from ..contexts import ValidatingContext, TransformingContext


class NonnullValidator(Validator):
    """A nonnull validator transforms None into empty library."""

    def validate(self, context: ValidatingContext) -> None:
        pass

    def transform(self, context: TransformingContext) -> Any:
        return NonnullNote() if context.value is None else context.value
