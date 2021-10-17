"""module for modifier modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from inspect import signature
from ..fdef import Fdef
from ..pkgutils import check_and_install_packages
if TYPE_CHECKING:
    from ..ctx import Ctx


class Modifier:
    """Abstract and base class for modifiers."""

    def packages(self) -> dict[str, (str, str)] | None:
        return None

    def check_packages(self) -> None:
        check_and_install_packages(self.packages())

    def resolve_param(self, param: Any, ctx: Ctx) -> Any:
        from ..types import Types
        if isinstance(param, Types):
            newctx = ctx.nval(None)
            return param.modifier.transform(newctx)
        elif callable(param):
            params_len = len(signature(param).parameters)
            if params_len == 0:
                return param()
            elif params_len == 1:
                return param(ctx.owner)
            elif params_len == 2:
                return param(ctx.owner, ctx)
            else:
                raise ValueError('not a valid parameter')
        else:
            return param

    def define(self, fdef: Fdef) -> None:
        """A hook and chance for modifier to update field description."""

    def validate(self, ctx: Ctx) -> None:
        """Validate the validity of the object."""

    def transform(self, ctx: Ctx) -> Any:
        """Transform raw input object into JSON Class acceptable object."""
        return ctx.val

    def tojson(self, ctx: Ctx) -> Any:
        """Transform JSON Class object and fields into JSON dict and values."""
        return ctx.val

    def serialize(self, ctx: Ctx) -> Any:
        """A chance for modifiers to update the object's value before the
        value is serialized into the database. This is only triggered for
        objects which are modified and have fields to write to the database.

        Unmodified objects won't cause serialize to trigger. JSON Classes which
        are not subclasses of ORMObject won't trigger this.
        """
        return ctx.val
