"""This is an internal module."""
from __future__ import annotations
from typing import List, Any, Union, Type, get_origin, get_args, TYPE_CHECKING
from datetime import date, datetime
from re import match
from dataclasses import fields as dataclass_fields, Field as DataclassField
from inflection import camelize
from .config import Config
from .graph import get_registered_class
from .field import Field
if TYPE_CHECKING:
    from .types import Types
    from .json_object import JSONObject


def string_type_to_default_types(
    argtype: str, graph_sibling: Any = None
) -> Types:
    """Convert string type to Types object."""
    from .types import types
    if argtype == 'str':
        return types.str
    elif argtype == 'int':
        return types.int
    elif argtype == 'float':
        return types.float
    elif argtype == 'bool':
        return types.bool
    elif argtype == 'date':
        return types.date
    elif argtype == 'datetime':
        return types.datetime
    elif argtype.startswith('List['):
        match_data = match('List\\[(.*)\\]', argtype)
        assert match_data is not None
        item_type = match_data.group(1)
        return types.listof(string_type_to_default_types(item_type, graph_sibling))
    elif argtype.startswith('Dict['):
        match_data = match('Dict\\[.+, ?(.*)\\]', argtype)
        assert match_data is not None
        item_type = match_data.group(1)
        return types.dictof(string_type_to_default_types(item_type, graph_sibling))
    else:
        return types.instanceof(get_registered_class(argtype, sibling=graph_sibling))


def type_to_default_types(argtype: Any, graph_sibling: Any = None) -> Types:
    """Convert arbitrary type to Types object."""
    from .json_object import JSONObject
    from .types import types
    if isinstance(argtype, str):
        return string_type_to_default_types(argtype, graph_sibling)
    elif argtype is str:
        return types.str
    elif argtype is int:
        return types.int
    elif argtype is float:
        return types.float
    elif argtype is bool:
        return types.bool
    elif argtype is date:
        return types.date
    elif argtype is datetime:
        return types.datetime
    elif get_origin(argtype) is list:
        return types.listof(get_args(argtype)[0])
    elif get_origin(argtype) is dict:
        return types.dictof(get_args(argtype)[1])
    elif issubclass(argtype, JSONObject):
        return types.instanceof(argtype)
    else:
        raise ValueError(f'{argtype} is not a valid JSON Class type.')


def dataclass_field_to_types(
    field: DataclassField, graph_sibling: Any = None
) -> Types:
    """Get JSON Class types from a dataclass field."""
    from .types import Types
    if isinstance(field.default, Types):
        return field.default
    else:
        return type_to_default_types(field.type, graph_sibling)


def collection_argument_type_to_types(
    argtype: Any, graph_sibling: Any = None
) -> Types:
    """Get desired JSON Class types from collection marker argument."""
    from .types import Types
    if isinstance(argtype, Types):
        return argtype
    else:
        return type_to_default_types(argtype, graph_sibling)


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
        field_types = dataclass_field_to_types(field, config.linked_class)
        assigned_default_value = None if isinstance(field.default, Types) else field.default
        if field.default == field.default_factory:  # type: ignore
            assigned_default_value = None
        retval.append(
            Field(
                field_name=field_name,
                json_field_name=json_field_name,
                db_field_name=db_field_name,
                field_types=field_types,
                assigned_default_value=assigned_default_value
            )
        )
    return retval
