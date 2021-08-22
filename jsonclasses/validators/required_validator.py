"""module for required validator."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..fdef import Fdef
from ..exceptions import ValidationException
from .validator import Validator
from ..fdef import FieldStorage
from ..jconf import JConf
from ..isjsonclass import isjsonobject
if TYPE_CHECKING:
    from ..ctx import Ctx


class RequiredValidator(Validator):
    """Mark a field as required."""

    def define(self, fdef: Fdef) -> None:
        fdef._required = True

    def validate(self, ctx: Ctx) -> None:
        storage = FieldStorage.EMBEDDED
        if ctx.fdef is not None:
            storage = ctx.fdef.field_storage
        if storage == FieldStorage.FOREIGN_KEY:  # we don't check foreign key
            return
        if storage == FieldStorage.LOCAL_KEY:
            if ctx.value is None:  # check key presence
                jconf: JConf = ctx.owner.__class__.cdef.jconf
                ko = str(ctx.keypatho[0])
                field = ctx.owner.__class__.cdef.field_named(ko)
                local_key = jconf.key_transformer(field)
                if isinstance(ctx.parent, dict):
                    if ctx.parent.get(local_key) is None:
                        kp = '.'.join([str(k) for k in ctx.keypathr])
                        raise ValidationException(
                            {kp: f'Value at \'{kp}\' should not be None.'},
                            ctx.root
                        )
                elif isjsonobject(ctx.parent):
                    try:
                        local_key_value = getattr(ctx.parent, local_key)
                    except AttributeError:
                        kp = '.'.join([str(k) for k in ctx.keypathr])
                        raise ValidationException(
                            {kp: f'Value at \'{kp}\' should not be None.'},
                            ctx.root
                        )
                    if local_key_value is None:
                        kp = '.'.join([str(k) for k in ctx.keypathr])
                        raise ValidationException(
                            {kp: f'Value at \'{kp}\' should not be None.'},
                            ctx.root
                        )
            return
        if ctx.value is None:
            kp = '.'.join([str(k) for k in ctx.keypathr])
            raise ValidationException(
                {kp: f'Value at \'{kp}\' should not be None.'},
                ctx.root
            )
