"""This is an internal module."""
from __future__ import annotations
from typing import (List, Any, Union, Type, Optional, get_origin, get_args,
                    TYPE_CHECKING)
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


def string_type_to_default_types(argtype: str,
                                 graph_sibling: Any = None,
                                 optional: bool = False) -> Types:
    """Convert string type to Types object."""
    from .types import types
    if argtype == 'str':
        return types.str if optional else types.str.required
    elif argtype == 'int':
        return types.int if optional else types.int.required
    elif argtype == 'float':
        return types.float if optional else types.float.required
    elif argtype == 'bool':
        return types.bool if optional else types.bool.required
    elif argtype == 'date':
        return types.date if optional else types.date.required
    elif argtype == 'datetime':
        return types.datetime if optional else types.datetime.required
    elif argtype.startswith('Optional['):
        match_data = match('Optional\\[(.*)\\]', argtype)
        assert match_data is not None
        item_type = match_data.group(1)
        return string_type_to_default_types(item_type, graph_sibling, True)
    elif argtype.startswith('List['):
        match_data = match('List\\[(.*)\\]', argtype)
        assert match_data is not None
        item_type = match_data.group(1)
        list_type = types.listof(string_type_to_default_types(item_type, graph_sibling))
        return list_type if optional else list_type.required
    elif argtype.startswith('Dict['):
        match_data = match('Dict\\[.+, ?(.*)\\]', argtype)
        assert match_data is not None
        item_type = match_data.group(1)
        dict_type = types.dictof(string_type_to_default_types(item_type, graph_sibling))
        return dict_type if optional else dict_type.required
    else:
        instance_type = types.instanceof(get_registered_class(argtype, sibling=graph_sibling))
        return instance_type if optional else instance_type.required


def type_to_default_types(argtype: Any,
                          graph_sibling: Any = None,
                          optional: bool = False) -> Types:
    """Convert arbitrary type to Types object."""
    from .json_object import JSONObject
    from .types import types
    if isinstance(argtype, str):
        return string_type_to_default_types(argtype, graph_sibling)
    elif argtype is str:
        return types.str if optional else types.str.required
    elif argtype is int:
        return types.int if optional else types.int.required
    elif argtype is float:
        return types.float if optional else types.float.required
    elif argtype is bool:
        return types.bool if optional else types.bool.required
    elif argtype is date:
        return types.date if optional else types.date.required
    elif argtype is datetime:
        return types.datetime if optional else types.datetime.required
    elif get_origin(argtype) == Union and len(get_args(argtype)) == 2:
        return type_to_default_types(get_args(argtype)[0], graph_sibling, True)
    elif get_origin(argtype) is list:
        list_type = types.listof(get_args(argtype)[0])
        return list_type if optional else list_type.required
    elif get_origin(argtype) is dict:
        dict_type = types.dictof(get_args(argtype)[1])
        return dict_type if optional else dict_type.required
    elif issubclass(argtype, JSONObject):
        instance_type = types.instanceof(argtype)
        return instance_type if optional else instance_type.required
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
