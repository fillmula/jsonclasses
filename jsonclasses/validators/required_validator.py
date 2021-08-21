"""module for required validator."""
from ..fdef import Fdef
from ..exceptions import ValidationException
from .validator import Validator
from ..ctx import Ctx
from ..fdef import FieldStorage, FieldType
from ..jconf import JConf
from ..isjsonclass import isjsonobject


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
                ko = ctx.keypath_owner
                field = ctx.owner.__class__.cdef.field_named(ko)
                local_key = jconf.key_transformer(field)
                if isinstance(ctx.parent, dict):
                    if ctx.parent.get(local_key) is None:
                        raise ValidationException(
                            {ctx.keypath_root: f'Value at \'{ctx.keypath_root}\' should not be None.'},
                            ctx.root
                        )
                elif isjsonobject(ctx.parent):
                    try:
                        local_key_value = getattr(ctx.parent, local_key)
                    except AttributeError:
                        raise ValidationException(
                            {ctx.keypath_root: f'Value at \'{ctx.keypath_root}\' should not be None.'},
                            ctx.root
                        )
                    if local_key_value is None:
                        raise ValidationException(
                            {ctx.keypath_root: f'Value at \'{ctx.keypath_root}\' should not be None.'},
                            ctx.root
                        )
            return
        if ctx.value is None:
            raise ValidationException(
                {ctx.keypath_root: f'Value at \'{ctx.keypath_root}\' should not be None.'},
                ctx.root
            )
