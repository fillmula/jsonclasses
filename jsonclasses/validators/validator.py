"""module for validator validator."""
from typing import Any
from ..fdef import Fdef
from ..ctx import VCtx, TCtx, JCtx


class Validator:
    """Abstract and base class for validators."""

    def define(self, fdef: Fdef) -> None:
        """A hook and chance for validator to update field description."""

    def validate(self, ctx: VCtx) -> None:
        """Validate the validity of the object."""

    def transform(self, ctx: TCtx) -> Any:
        """Transform raw input object into JSON Class acceptable object."""
        return ctx.value

    def tojson(self, ctx: JCtx) -> Any:
        """Transform JSON Class object and fields into JSON dict and values."""
        return ctx.value

    def serialize(self, ctx: TCtx) -> Any:
        """A chance for validators to update the object's value before the
        value is serialized into the database. This is only triggered for
        objects which are modified and have fields to write to the database.

        Unmodified objects won't cause serialize to trigger. JSON Classes which
        are not subclasses of ORMObject won't trigger this.
        """
        return ctx.value
