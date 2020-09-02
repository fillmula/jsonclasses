from ..types import types, Types
from ..validators import RequiredValidator

def is_required_type(types: Types) -> bool:
  '''Use this method to test if given types has required marker inside. You
  mainly use this when implementing jsonclasses ORM integration.

  Args:
    types (Types): A jsonclasses types object.

  Returns:
    bool: Return True if the given type definition has required marker inside
    else False.
  '''
  vs = types.validator.validators
  try:
    next(v for v in vs if type(v) is RequiredValidator)
    return True
  except StopIteration:
    return False
