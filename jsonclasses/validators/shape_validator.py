from typing import Dict, Any
from ..exceptions import ValidationException
from .validator import Validator
from ..utils import default_validator_for_type, keypath

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
    retval = {}
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
        retval[k] = validator.transform(value_at_key, camelize_keys)
      else:
        [retval][k] = value_at_key
    return retval

  def tojson(self, value, camelize_keys: bool):
    if value is None:
      return None
    if type(value) is not dict:
      return value
    retval = {}
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
        retval[k] = validator.tojson(value_at_key, camelize_keys)
      else:
        [retval][k] = value_at_key
    return retval
