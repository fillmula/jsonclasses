"""module for validator validator."""
from ..exceptions import ValidationException
from .validator import Validator
from ..ctx import Ctx


class InvalidValidator(Validator):
    """A validator that turns value into invalid."""

    def validate(self, ctx: Ctx) -> None:
        """Raises invalid exception."""
        raise ValidationException(
            {ctx.keypath_root: f'value is invalid'},
            ctx.root
        )
