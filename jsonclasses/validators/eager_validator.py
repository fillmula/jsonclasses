from .validator import Validator

class EagerValidator(Validator):
  '''An EagerValidator marks fields for initialization and set stage validation.
  This is used usually before heavy transforming validators.
  '''

  def validate(self, value, key_path, root, all_fields):
    pass
