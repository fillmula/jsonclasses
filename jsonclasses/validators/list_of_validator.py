from typing import Any
from ..exceptions import ValidationException
from .validator import Validator
from .required_validator import RequiredValidator
from ..utils import default_validator_for_type, keypath, is_nullable_type

class ListOfValidator(Validator):

  def __init__(self, types: Any):
    self.types = types

  def validate(self, value, key_path, root, all_fields):
    if value is not None and type(value) is not list:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should be a list.' },
        root
      )
    for i, v in enumerate(value):
      validator = None
      if hasattr(self.types, 'validator'):
        validator = self.types.validator
      else:
        validator = default_validator_for_type(self.types)
      if validator:
        if not is_nullable_type(validator):
          validator = validator.append(RequiredValidator())
        validator.validate(v, keypath(key_path, i), root, all_fields)

  def transform(self, value):
    if value is None:
      return None
    if type(value) is not list:
      return value
    if hasattr(self.types, 'validator'):
      validator = self.types.validator
    else:
      validator = default_validator_for_type(self.types)
    if validator:
      return [ validator.transform(v) for v in value ]
    else:
      return value

  def tojson(self, value):
    if value is None:
      return None
    if type(value) is not list:
      return value
    if hasattr(self.types, 'validator'):
      validator = self.types.validator
    else:
      validator = default_validator_for_type(self.types)
    if validator:
      return [ validator.tojson(v) for v in value ]
    else:
      return value
