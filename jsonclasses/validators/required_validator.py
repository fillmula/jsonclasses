"""module for required validator."""
from ..field_definition import FieldDefinition
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext
from ..field_definition import FieldStorage, FieldType
from ..config import Config
from ..isjsonclass import isjsonobject


class RequiredValidator(Validator):
    """Mark a field as required."""

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.required = True

    def validate(self, context: ValidatingContext) -> None:
        storage = FieldStorage.EMBEDDED
        if context.definition is not None:
            storage = context.definition.field_storage
        if storage == FieldStorage.FOREIGN_KEY:  # we don't check foreign key
            return
        if storage == FieldStorage.LOCAL_KEY:
            if context.value is None:  # check key presence
                config: Config = context.owner.__class__.definition.config
                ko = context.keypath_owner
                field = context.owner.__class__.definition.field_named(ko)
                local_key = config.key_transformer(field)
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
