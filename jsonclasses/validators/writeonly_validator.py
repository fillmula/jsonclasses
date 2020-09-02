from ..exceptions import ValidationException
from .validator import Validator

class WriteonlyValidator(Validator):

  def validate(self, value, key_path, root, all_fields):
    pass
