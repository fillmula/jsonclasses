from typing import Dict, Any
from ..exceptions import ValidationException
from .validator import Validator
from ..utils import default_validator_for_type, keypath
from inflection import underscore, camelize

class ShapeValidator(Validator):

  def __init__(self, types):
    if type(types) is not dict:
      raise ValueError('argument passed to ShapeValidator should be dict')
    self.types = types

  def validate(self, value, key_path, root, all_fields):
    if value is not None and type(value) is not dict:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should be a dict.' },
        root
      )
    for k, t in self.types.items():
      try:
        value_at_key = value[k]
      except KeyError:
        value_at_key = None
      if hasattr(t, 'validator'):
        validator = t.validator
      else:
        validator = default_validator_for_type(t)
      if validator:
        validator.validate(value_at_key, keypath(key_path, k), root, all_fields)

  def transform(self, value, camelize_keys: bool):
    if value is None:
      return None
    if type(value) is not dict:
      return value
    unused_keys = list(self.types.keys())
    retval = {}
    for k, field_value in value.items():
      key = underscore(k) if camelize_keys else k
      if key in unused_keys:
        t = self.types[key]
        if hasattr(t, 'validator'):
          validator = t.validator
        else:
          validator = default_validator_for_type(t)
        if validator:
          retval[key] = validator.transform(field_value, camelize_keys)
        else:
          retval[key] = field_value
        unused_keys.remove(key)
    for k in unused_keys:
      retval[k] = None
    return retval

  def tojson(self, value, camelize_keys: bool):
    if value is None:
      return None
    if type(value) is not dict:
      return value
    retval = {}
    for k, t in self.types.items():
      key = camelize(k, False) if camelize_keys else k
      try:
        value_at_key = value[k]
      except KeyError:
        value_at_key = None
      if hasattr(t, 'validator'):
        validator = t.validator
      else:
        validator = default_validator_for_type(t)
      if validator:
        retval[key] = validator.tojson(value_at_key, camelize_keys)
      else:
        retval[key] = value_at_key
    return retval
