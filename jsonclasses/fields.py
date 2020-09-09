from __future__ import annotations
from typing import List, Any, get_origin, get_args
from datetime import date, datetime
from re import match
from dataclasses import fields as dataclass_fields, Field as DataclassField
from inflection import camelize
from .config import Config
from .reference_map import resolve_class
from .graph import get_registered_class
from .field import Field

def string_type_to_default_types(type: str, graph_sibling: Any = None) -> 'Types':
  Types = resolve_class('Types')
  types = Types()
  if type == 'str':
    return types.str
  elif type == 'int':
    return types.int
  elif type == 'float':
    return types.float
  elif type == 'bool':
    return types.bool
  elif type == 'date':
    return types.date
  elif type == 'datetime':
    return types.datetime
  elif type.startswith('List['):
    item_type = match('List\\[(.*)\\]', type).group(1)
    return types.listof(string_type_to_default_types(item_type, graph_sibling))
  elif type.startswith('Dict['):
    item_type = match('Dict\\[.+, ?(.*)\\]', type).group(1)
    return types.dictof(string_type_to_default_types(item_type, graph_sibling))
  else:
    return types.instanceof(get_registered_class(type, sibling=graph_sibling))

def type_to_default_types(type: Any, graph_sibling: Any = None) -> 'Types':
  JSONObject = resolve_class('JSONObject')
  Types = resolve_class('Types')
  types = Types()
  if isinstance(type, str):
    return string_type_to_default_types(type, graph_sibling)
  elif type is str:
    return types.str
  elif type is int:
    return types.int
  elif type is float:
    return types.float
  elif type is bool:
    return types.bool
  elif type is date:
    return types.date
  elif type is datetime:
    return types.datetime
  elif get_origin(type) is list:
    return types.listof(get_args(type)[0])
  elif get_origin(type) is dict:
    return types.dictof(get_args(type)[1])
  elif issubclass(type, JSONObject):
    return types.instanceof(type)
  else:
    return None

def dataclass_field_to_types(field: DataclassField, graph_sibling: Any = None) -> 'Types':
  Types = resolve_class('Types')
  if isinstance(field.default, Types):
    return field.default
  else:
    return type_to_default_types(field.type, graph_sibling)

def collection_argument_type_to_types(type: Any, graph_sibling: Any = None) -> 'Types':
  Types = resolve_class('Types')
  if isinstance(type, Types):
    return type
  else:
    return type_to_default_types(type, graph_sibling)

def fields(class_or_instance: Any) -> List[Field]:
  Types = resolve_class('Types')
  JSONObject = resolve_class('JSONObject')
  if isinstance(class_or_instance, JSONObject):
    config: Config = class_or_instance.__class__.config
  elif issubclass(class_or_instance, JSONObject):
    config: Config = class_or_instance.config
  retval = []
  for field in dataclass_fields(class_or_instance):
    field_name = field.name
    json_field_name = camelize(field_name, False) if config.camelize_json_keys else field_name
    db_field_name = camelize(field_name, False) if config.camelize_db_keys else field_name
    field_types = dataclass_field_to_types(field, config.linked_class)
    assigned_default_value = None if isinstance(field.default, Types) else field.default
    if field.default == field.default_factory:
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
