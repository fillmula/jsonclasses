from datetime import datetime
from ..exceptions import ValidationException
from .validator import Validator

class DatetimeValidator(Validator):

  def validate(self, value, key_path, root, all):
    if value is not None and type(value) is not datetime:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at {key_path} should be datetime.' },
        root
      )

  def transform(self, value):
    if value is not None:
      return datetime.fromisoformat(value)

  def to_json(self, value):
    if value is not None:
      return value.isoformat()
