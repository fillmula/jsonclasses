from ..types import types, Types
from ..validators import WriteonceValidator

def is_writeonce_type(types: Types) -> bool:
  '''Use this method to test if given types has writeonce marker inside.

  Args:
    types (Types): A jsonclasses types object.

  Returns:
    bool: Return True if the given type definition has writeonce marker inside
    else False.
  '''
  vs = types.validator.validators
  try:
    next(v for v in vs if type(v) is WriteonceValidator)
    return True
  except StopIteration:
    return False
