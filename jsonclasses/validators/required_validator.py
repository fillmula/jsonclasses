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
        if context.fdef is not None:
            storage = context.fdef.field_storage
        if storage == FieldStorage.FOREIGN_KEY:  # we don't check foreign key
            return
        if storage == FieldStorage.LOCAL_KEY:
            if context.value is None:  # check key presence
                jconf: JConf = context.owner.__class__.cdef.jconf
                ko = context.keypath_owner
                field = context.owner.__class__.cdef.field_named(ko)
                local_key = jconf.key_transformer(field)
                if isinstance(context.parent, dict):
                    if context.parent.get(local_key) is None:
                        raise ValidationException(
                            {context.keypath_root: f'Value at \'{context.keypath_root}\' should not be None.'},
                            context.root
                        )
                elif isjsonobject(context.parent):
                    try:
                        local_key_value = getattr(context.parent, local_key)
                    except AttributeError:
                        raise ValidationException(
                            {context.keypath_root: f'Value at \'{context.keypath_root}\' should not be None.'},
                            context.root
                        )
                    if local_key_value is None:
                        raise ValidationException(
                            {context.keypath_root: f'Value at \'{context.keypath_root}\' should not be None.'},
                            context.root
                        )
            return
        if context.value is None:
            raise ValidationException(
                {context.keypath_root: f'Value at \'{context.keypath_root}\' should not be None.'},
                context.root
            )
