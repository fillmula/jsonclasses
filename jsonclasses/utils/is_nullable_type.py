from ..validators.nullable_validator import NullableValidator
from ..validators.chained_validator import ChainedValidator

def is_nullable_type(validator: ChainedValidator) -> bool:
  '''Use this method to test if given types has nullable marker inside.

  Args:
    validator (ChainedValidator): A jsonclasses types object's chained validator.

  Returns:
    bool: Return True if the given type definition has readonly marker inside
    else False.
  '''
  vs = validator.validators
  try:
    next(v for v in vs if type(v) is NullableValidator)
    return True
  except StopIteration:
    return False
