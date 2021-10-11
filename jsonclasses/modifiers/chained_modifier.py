"""module for chained modifier."""
from __future__ import annotations
from jsonclasses.vmsgcollector import VMsgCollector
from typing import Any, Optional, cast, TYPE_CHECKING
from functools import reduce
from ..excs import ValidationException
from .modifier import Modifier
from .eager_modifier import EagerModifier
from .preserialize_modifier import PreserializeModifier
from ..isjsonclass import isjsonobject
if TYPE_CHECKING:
    from ..ctx import Ctx


class ChainedModifier(Modifier):
    """Chained modifier has a series of modifiers chained."""

    def __init__(self, modifiers: Optional[list[Modifier]] = None) -> None:
        self.vs = modifiers or []

    def append(self, *args: Modifier) -> ChainedModifier:
        """Append modifiers to this chained modifier chain."""
        return ChainedModifier([*self.vs, *args])

    def _first_vidx(self, cls: type[Modifier]) -> Optional[int]:
        """This function returns the first modifier of class' index.

        Returns:
        Optional[int]: The found index or None.
        """
        v = next((v for v in self.vs if isinstance(v, cls)), None)
        return self.vs.index(v) if v is not None else None

    def _last_vidx(self, cls: type[Modifier]) -> Optional[int]:
        v = next((v for v in self.vs[::-1] if isinstance(v, cls)), None)
        return self.vs.index(v) if v is not None else None

    @property
    def _levidx(self) -> Optional[int]:
        return self._last_vidx(EagerModifier)

    @property
    def _fpvidx(self) -> Optional[int]:
        return self._first_vidx(PreserializeModifier)

    @property
    def _tvs(self) -> list[Modifier]:
        """The modifiers which should be perform eager validation on.

        This is from the beginning to the last eager modifier before the first
        preserialize modifier.
        """
        # TODO: accounting into e and p
        return self.vs[:self._levidx] if self._levidx is not None else []

    @property
    def _pvs(self) -> list[Modifier]:
        """
        """
        return self.vs[self._fpvidx:] if self._fpvidx is not None else []

    @property
    def _nvs(self) -> list[Modifier]:
        """Modifiers between last eager modifier and first preserialize
        modifier. These modifiers should be performed in normal validation
        process.
        """
        return self.vs[self._levidx:self._fpvidx]

    def _vt(self, v: Modifier, ctx: Ctx) -> Any:
        """Validate as transform."""
        retval = v.transform(ctx)
        v.validate(ctx.nval(retval))
        return retval

    def _sv(self, v: Modifier, ctx: Ctx) -> Any:
        """Serialize as validate."""
        val = v.serialize(ctx)
        v.validate(ctx.nval(val))
        if isjsonobject(ctx.parent):
            setattr(ctx.parent, cast(str, ctx.keypathp[0]), val)
        return val

    def validate(self, ctx: Ctx) -> None:
        ctor = VMsgCollector()
        for modifier in self._nvs:
            try:
                modifier.validate(ctx)
            except ValidationException as exception:
                ctor.receive(exception.keypath_messages)
                if not ctx.ctxcfg.all_fields:
                    break
        if ctor.has_msgs:
            ctx.raise_mvexc(ctor.messages)

    def transform(self, ctx: Ctx) -> Any:
        val = ctx.val
        val = reduce(lambda val, v: self._vt(v, ctx.nval(val)), self._tvs, val)
        val = reduce(lambda val, v: v.transform(ctx.nval(val)), self._nvs, val)
        return val

    def tojson(self, ctx: Ctx) -> Any:
        return reduce(lambda val, v: v.tojson(ctx.nval(val)), self.vs, ctx.val)

    def serialize(self, ctx: Ctx) -> Any:
        val = ctx.val
        val = reduce(lambda val, v: v.serialize(ctx.nval(val)), self._tvs, val)
        val = reduce(lambda val, v: v.serialize(ctx.nval(val)), self._nvs, val)
        val = reduce(lambda val, v: self._sv(v, ctx.nval(val)), self._pvs, val)
        return val
