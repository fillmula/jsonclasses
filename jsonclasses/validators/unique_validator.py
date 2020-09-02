from ..exceptions import ValidationException
from .validator import Validator

class UniqueValidator(Validator):

  def validate(self, value, key_path, root, all_fields):
    pass
