from ..exceptions import ValidationException
from .validator import Validator

class ReadonlyValidator(Validator):

  def validate(self, value, key_path, root, all_fields):
    pass
