from ..exceptions import ValidationException
from .validator import Validator

class TruncateValidator(Validator):

  max_length: int

  def __init__(self, max_length):
    self.max_length = max_length

  def validate(self, value, key_path, root, all_fields):
    pass

  def transform(self, value):
    if value is not None and value.__len__() > self.max_length:
      return value[:self.max_length]
    else:
      return value
