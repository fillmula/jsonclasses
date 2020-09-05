from typing import Any
from ..exceptions import ValidationException
from .validator import Validator
from .required_validator import RequiredValidator
from ..utils import default_validator_for_type, keypath, is_nullable_type
from inflection import underscore, camelize

class DictOfValidator(Validator):

  def __init__(self, types: Any):
    self.types = types

  def validate(self, value, key_path, root, all_fields):
    if value is not None and type(value) is not dict:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should be a dict.' },
        root
      )
    for k, v in value.items():
      validator = None
      if hasattr(self.types, 'validator'):
        validator = self.types.validator
      else:
        validator = default_validator_for_type(self.types)
      if validator:
        if not is_nullable_type(validator):
          validator = validator.append(RequiredValidator())
        validator.validate(v, keypath(key_path, k), root, all_fields)

  def transform(self, value, camelize_keys: bool, key: str = ''):
    if value is None:
      return None
    if type(value) is not dict:
      return value
    if hasattr(self.types, 'validator'):
      validator = self.types.validator
    else:
      validator = default_validator_for_type(self.types)
    if validator:
      retval = {}
      for k, v in value.items():
        new_key = underscore(k) if camelize_keys else k
        new_value = validator.transform(v, camelize_keys, keypath(key, new_key))
        retval[new_key] = new_value
      return retval
    else:
      return value

  def tojson(self, value, camelize_keys: bool):
    if value is None:
      return None
    if type(value) is not dict:
      return value
    if hasattr(self.types, 'validator'):
      validator = self.types.validator
    else:
      validator = default_validator_for_type(self.types)
    if validator:
      return { camelize(k, False) if camelize_keys else k: validator.tojson(v, camelize_keys) for k, v in value.items() }
    else:
      return value
