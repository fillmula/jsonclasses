from datetime import date
from ..exceptions import ValidationException
from .validator import Validator

class DateValidator(Validator):

  def validate(self, value, key_path, root, all):
    if value is not None and type(value) is not date:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at {key_path} should be date.' },
        root
      )

  def transform(self, value):
    if value is not None:
      return date.fromisoformat(value)

  def to_json(self, value):
    if value is not None:
      return value.isoformat()
