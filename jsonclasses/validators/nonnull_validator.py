from ..exceptions import ValidationException
from .validator import Validator

class NonnullValidator(Validator):

  def validate(self, value, key_path, root, all_fields):
    pass

  def transform(self, value, camelize_keys: bool):
    return {} if value is None else value
