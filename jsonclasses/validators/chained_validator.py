"""module for chained validator."""
from __future__ import annotations
from typing import Any, Optional, TYPE_CHECKING
from functools import reduce
from ..excs import ValidationException
from .validator import Validator
from .eager_validator import EagerValidator
from .preserialize_validator import PreserializeValidator
if TYPE_CHECKING:
    from ..ctx import Ctx


class ChainedValidator(Validator):
    """Chained validator has a series of validators chained."""

    def __init__(self, validators: Optional[list[Validator]] = None) -> None:
        self.vs = validators or []

    def append(self, *args: Validator) -> ChainedValidator:
        """Append validators to this chained validator chain."""
        return ChainedValidator([*self.vs, *args])

    def _first_vidx(self, cls: type[Validator]) -> Optional[int]:
        """This function returns the first validator of class' index.

        Returns:
        Optional[int]: The found index or None.
        """
        v = next((v for v in self.vs if isinstance(v, cls)), None)
        return self.vs.index(v) if v is not None else None

    def _last_vidx(self, cls: type[Validator]) -> Optional[int]:
        v = next((v for v in self.vs[::-1] if isinstance(v, cls)), None)
        return self.vs.index(v) if v is not None else None

    @property
    def _levidx(self) -> Optional[int]:
        return self._last_vidx(EagerValidator)

    @property
    def _fpvidx(self) -> Optional[int]:
        return self._first_vidx(PreserializeValidator)

    @property
    def _tvs(self) -> list[Validator]:
        """The validators which should be perform eager validation on.

        This is from the beginning to the last eager validator before the first
        preserialize validator.
        """
        # TODO: accounting into e and p
        return self.vs[:self._levidx] if self._levidx is not None else []

    @property
    def _pvs(self) -> list[Validator]:
        """
        """
        return self.vs[self._fpvidx:] if self._fpvidx is not None else []

    @property
    def _nvs(self) -> list[Validator]:
        """Validators between last eager validator and first preserialize
        validator. These validators should be performed in normal validation
        process.
        """
        return self.vs[self._levidx:self._fpvidx]

    def _vt(self, v: Validator, ctx: Ctx) -> Any:
        """Validate as transform."""
        retval = v.transform(ctx)
        v.validate(ctx.nval(retval))
        return retval

    def _sv(self, v: Validator, ctx: Ctx) -> Any:
        """Serialize as validate."""
        val = v.serialize(ctx)
        v.validate(ctx.nval(val))
        return val

    def validate(self, ctx: Ctx) -> None:
        keypath_messages: dict[str, str] = {}
        for validator in self._nvs:
            try:
                validator.validate(ctx)
            except ValidationException as exception:
                keypath_messages.update(exception.keypath_messages)
                if not ctx.ctxcfg.all_fields:
                    break
        if len(keypath_messages) > 0:
            raise ValidationException(keypath_messages, ctx.root)

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
