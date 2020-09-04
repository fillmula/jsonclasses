from ..validators.readonly_validator import ReadonlyValidator
from ..validators.chained_validator import ChainedValidator

def is_readonly_type(validator: ChainedValidator) -> bool:
  '''Use this method to test if given types has readonly marker inside.

  Args:
    types (Types): A jsonclasses types object.

  Returns:
    bool: Return True if the given type definition has readonly marker inside
    else False.
  '''
  vs = validator.validators
  try:
    next(v for v in vs if type(v) is ReadonlyValidator)
    return True
  except StopIteration:
    return False
