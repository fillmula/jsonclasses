"""This is an internal module."""
from __future__ import annotations
from typing import List, Any, Union, Type, TYPE_CHECKING
from dataclasses import fields as dataclass_fields, Field as DataclassField
from inflection import camelize
from .config import Config
from .field import Field
from .types_resolver import to_types
if TYPE_CHECKING:
    from .types import Types
    from .json_object import JSONObject


def dataclass_field_get_types(
    field: DataclassField, graph_sibling: Any = None
) -> Types:
    """Get JSON Class types from a dataclass field."""
    from .types import Types
    if isinstance(field.default, Types):
        return field.default
    else:
        return to_types(field.type, graph_sibling)


def fields(
    class_or_instance: Union[JSONObject, Type[JSONObject]]
) -> List[Field]:
    """Iterate through a JSON Class or JSON Class instance's fields."""
    from .types import Types
    from .json_object import JSONObject
    if isinstance(class_or_instance, JSONObject):
        config = class_or_instance.__class__.config
    elif issubclass(class_or_instance, JSONObject):
        config = class_or_instance.config
    else:
        config = Config()
    retval = []
    for field in dataclass_fields(class_or_instance):
        field_name = field.name
        json_field_name = camelize(field_name, False) if config.camelize_json_keys else field_name
        db_field_name = camelize(field_name, False) if config.camelize_db_keys else field_name
        field_types = dataclass_field_get_types(field, config.linked_class)
        assigned_default_value = None if isinstance(field.default, Types) else field.default
        if field.default == field.default_factory:  # type: ignore
            assigned_default_value = None
        retval.append(
            Field(field_name=field_name,
                  json_field_name=json_field_name,
                  db_field_name=db_field_name,
                  field_types=field_types,
                  assigned_default_value=assigned_default_value,
                  field_description=field_types.field_description,
                  field_validator=field_types.validator))
    return retval
