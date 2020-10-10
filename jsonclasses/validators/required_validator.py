"""module for required validator."""
from ..fields import FieldDescription
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext
from ..fields import FieldStorage, FieldType
from ..config import Config


class RequiredValidator(Validator):
    """Mark a field as required."""

    def define(self, fdesc: FieldDescription) -> None:
        fdesc.required = True

    def validate(self, context: ValidatingContext) -> None:
        storage = FieldStorage.EMBEDDED
        list_field = False
        if context.fdesc is not None:
            storage = context.fdesc.field_storage
            list_field = context.fdesc.field_type == FieldType.LIST
        if storage == FieldStorage.FOREIGN_KEY:  # we don't check foreign key
            return
        if storage == FieldStorage.LOCAL_KEY:
            if context.value is None:  # check key presence
                config: Config = context.root.__class__.config
                assert config.local_key is not None
                local_key = config.local_key(
                    context.keypath_root,
                    FieldType.LIST if list_field else FieldType.INSTANCE)
                from ..json_object import JSONObject
                if isinstance(context.parent, dict):
                    if context.parent.get(local_key) is None:
                        raise ValidationException(
                            {context.keypath_root: f'Value at \'{context.keypath_root}\' should not be None.'},
                            context.root
                        )
                elif isinstance(context.parent, JSONObject):
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
