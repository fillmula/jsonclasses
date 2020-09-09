from __future__ import annotations
from typing import Any
from ..field_description import FieldDescription, FieldType
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator
from .required_validator import RequiredValidator
from ..utils.keypath import keypath
from ..reference_map import referenced, resolve_class
from inflection import underscore, camelize
from ..utils.nonnull_note import NonnullNote
from ..fields import collection_argument_type_to_types
from ..field_description import CollectionNullability

@referenced
class DictOfValidator(Validator):

  def __init__(self, types: Any):
    self.types = types

  def define(self, field_description: FieldDescription):
    field_description.field_type = FieldType.DICT

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    if value is None:
      return
    if type(value) is not dict:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should be a dict.' },
        root
      )
    types = collection_argument_type_to_types(self.types, config.linked_class)
    if types:
      if types.field_description.collection_nullability == CollectionNullability.UNDEFINED:
        types = types.required
      keypath_messages = {}
      for k, v in value.items():
        try:
          types.validator.validate(v, keypath(key_path, k), root, all_fields, config)
        except ValidationException as exception:
          if all_fields:
            keypath_messages.update(exception.keypath_messages)
          else:
            raise exception
      if len(keypath_messages) > 0:
        raise ValidationException(keypath_messages=keypath_messages, root=root)

  def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    if value is None:
      return None
    elif isinstance(value, NonnullNote):
      value = {}
    elif type(value) is not dict:
      return value
    types = collection_argument_type_to_types(self.types, config.linked_class)
    if types:
      retval = {}
      for k, v in value.items():
        new_key = underscore(k) if config.camelize_json_keys else k
        new_value = types.validator.transform(v, keypath(key_path, new_key), root, all_fields, config)
        retval[new_key] = new_value
      return retval
    else:
      return value

  def tojson(self, value: Any, config: Config):
    if value is None:
      return None
    if type(value) is not dict:
      return value
    types = collection_argument_type_to_types(self.types, config.linked_class)
    if types:
      return { camelize(k, False) if config.camelize_json_keys else k: types.validator.tojson(v, config) for k, v in value.items() }
    else:
      return value
