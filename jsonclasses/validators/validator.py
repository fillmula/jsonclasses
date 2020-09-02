from ..exceptions import ValidationException

class Validator:

  def validate(self, value, key_path, root, all_fields):
    raise ValidationException(
      { key_path: f'Value \'{value}\' at \'{key_path}\' is invalid.' },
      root
    )

  def transform(self, value):
    return value

  def tojson(self, value):
    return value
