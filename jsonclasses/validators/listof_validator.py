from typing import Any
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator
from .required_validator import RequiredValidator
from ..utils import default_validator_for_type, keypath, is_nullable_type

class ListOfValidator(Validator):

  def __init__(self, types: Any):
    self.types = types

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool):
    if value is not None and type(value) is not list:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should be a list.' },
        root
      )
    validator = None
    if hasattr(self.types, 'validator'):
      validator = self.types.validator
    else:
      validator = default_validator_for_type(self.types)
    if validator:
      if not is_nullable_type(validator):
        validator = validator.append(RequiredValidator())
      keypath_messages = {}
      for i, v in enumerate(value):
        try:
          validator.validate(v, keypath(key_path, i), root, all_fields)
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
    if type(value) is not list:
      return value
    if hasattr(self.types, 'validator'):
      validator = self.types.validator
    else:
      validator = default_validator_for_type(self.types)
    if validator:
      return [ validator.transform(v, keypath(key_path, i), root, all_fields, config) for i, v in enumerate(value) ]
    else:
      return value

  def tojson(self, value, config: Config):
    if value is None:
      return None
    if type(value) is not list:
      return value
    if hasattr(self.types, 'validator'):
      validator = self.types.validator
    else:
      validator = default_validator_for_type(self.types)
    if validator:
      return [ validator.tojson(v, config) for v in value ]
    else:
      return value
