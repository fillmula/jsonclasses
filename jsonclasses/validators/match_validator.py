from re import search
from ..exceptions import ValidationException
from .validator import Validator

class MatchValidator(Validator):

  pattern: str

  def __init__(self, pattern):
    self.pattern = pattern

  def validate(self, value, key_path, root, all_fields):
    if value is not None and search(self.pattern, value) is None:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should match \'{self.pattern}\'.' },
        root
      )
