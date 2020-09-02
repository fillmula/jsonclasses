from ..types import types, Types
from ..validators import ReadonlyValidator

def is_readonly_type(types: Types) -> bool:
  '''Use this method to test if given types has readonly marker inside.

  Args:
    types (Types): A jsonclasses types object.

  Returns:
    bool: Return True if the given type definition has readonly marker inside
    else False.
  '''
  vs = types.validator.validators
  try:
    next(v for v in vs if type(v) is ReadonlyValidator)
    return True
  except StopIteration:
    return False
