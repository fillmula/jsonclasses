from ..exceptions import ValidationException
from .validator import Validator
from ..types import Types

class ListOfValidator:

  types: Types

  def __init__(self, types: Types):
    self.types = types

  def validate(self, value, key_path, root, all_fields):
    if value is not None and type(value) is not list:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should be list.' },
        root
      )
    for v in value:
      self.types.validator.validate(v, key_path, root, all_fields)
