from ..types import types, Types
from ..validators import WriteonlyValidator

def is_writeonly_type(types: Types) -> bool:
  '''Use this method to test if given types has writeonly marker inside.

  Args:
    types (Types): A jsonclasses types object.

  Returns:
    bool: Return True if the given type definition has writeonly marker inside
    else False.
  '''
  vs = types.validator.validators
  try:
    next(v for v in vs if type(v) is WriteonlyValidator)
    return True
  except StopIteration:
    return False
