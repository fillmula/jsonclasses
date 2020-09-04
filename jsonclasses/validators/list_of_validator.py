from typing import Any
from ..exceptions import ValidationException
from .validator import Validator
from .utils import keypath

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
      if hasattr(self.types, 'validator'):
        self.types.validator.validate(v, keypath(key_path, i), root, all_fields)
      else:
        # it's good to synthesis a validator here, however, cannot overcome
        # Python's circular import issue
        pass
