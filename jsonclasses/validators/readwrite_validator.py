from ..exceptions import ValidationException
from .validator import Validator

class ReadwriteValidator(Validator):

  def validate(self, value, key_path, root, all_fields):
    pass
