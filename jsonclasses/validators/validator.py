"""module for validator validator."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from ..fdef import Fdef
if TYPE_CHECKING:
    from ..ctx import Ctx


class Validator:
    """Abstract and base class for validators."""

    def define(self, fdef: Fdef) -> None:
        """A hook and chance for validator to update field description."""

    def validate(self, ctx: Ctx) -> None:
        """Validate the validity of the object."""

    def transform(self, ctx: Ctx) -> Any:
        """Transform raw input object into JSON Class acceptable object."""
        return ctx.val

    def tojson(self, ctx: Ctx) -> Any:
        """Transform JSON Class object and fields into JSON dict and values."""
        return ctx.val

    def serialize(self, ctx: Ctx) -> Any:
        """A chance for validators to update the object's value before the
        value is serialized into the database. This is only triggered for
        objects which are modified and have fields to write to the database.

        Unmodified objects won't cause serialize to trigger. JSON Classes which
        are not subclasses of ORMObject won't trigger this.
        """
        return ctx.val
