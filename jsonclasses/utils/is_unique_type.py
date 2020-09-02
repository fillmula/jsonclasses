from ..types import types, Types
from ..validators import UniqueValidator

def is_unique_type(types: Types) -> bool:
  '''Use this method to test if given types has unique marker inside. You mainly
  use this when implementing jsonclasses ORM integration.

  Args:
    types (Types): A jsonclasses types object.

  Returns:
    bool: Return True if the given type definition has unique marker inside
    else False.
  '''
  vs = types.validator.validators
  try:
    next(v for v in vs if type(v) is UniqueValidator)
    return True
  except StopIteration:
    return False
