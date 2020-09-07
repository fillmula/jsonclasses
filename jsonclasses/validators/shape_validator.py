from typing import Dict, Any
from inflection import underscore, camelize
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator
from ..utils.default_validator_for_type import default_validator_for_type
from ..utils.keypath import keypath
from ..utils.reference_map import referenced, resolve_class

@referenced
class ShapeValidator(Validator):

  def __init__(self, types):
    if type(types) is not dict:
      raise ValueError('argument passed to ShapeValidator should be dict')
    self.types = types

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    if value is not None and type(value) is not dict:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should be a dict.' },
        root
      )
    keypath_messages = {}
    for k, t in self.types.items():
      try:
        value_at_key = value[k]
      except KeyError:
        value_at_key = None
      if isinstance(t, resolve_class('Types')):
        validator = t.validator
      else:
        validator = default_validator_for_type(t, graph_sibling=config.linked_class)
      if validator:
        try:
          validator.validate(value_at_key, keypath(key_path, k), root, all_fields, config)
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
    if type(value) is not dict:
      return value
    unused_keys = list(self.types.keys())
    retval = {}
    for k, field_value in value.items():
      new_key = underscore(k) if config.camelize_json_keys else k
      if new_key in unused_keys:
        t = self.types[new_key]
        if isinstance(t, resolve_class('Types')):
          validator = t.validator
        else:
          validator = default_validator_for_type(t, graph_sibling=config.linked_class)
        if validator:
          retval[new_key] = validator.transform(field_value, keypath(key_path, new_key), root, all_fields, config)
        else:
          retval[new_key] = field_value
        unused_keys.remove(new_key)
    for k in unused_keys:
      retval[k] = None
    return retval

  def tojson(self, value: Any, config: Config):
    if value is None:
      return None
    if type(value) is not dict:
      return value
    retval = {}
    for k, t in self.types.items():
      key = camelize(k, False) if config.camelize_json_keys else k
      try:
        value_at_key = value[k]
      except KeyError:
        value_at_key = None
      if isinstance(t, resolve_class('Types')):
        validator = t.validator
      else:
        validator = default_validator_for_type(t, graph_sibling=config.linked_class)
      if validator:
        retval[key] = validator.tojson(value_at_key, config)
      else:
        retval[key] = value_at_key
    return retval
