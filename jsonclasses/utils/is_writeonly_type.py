from ..validators.writeonly_validator import WriteonlyValidator
from ..validators.chained_validator import ChainedValidator

def is_writeonly_type(validator: ChainedValidator) -> bool:
  '''Use this method to test if given types has writeonly marker inside.

  Args:
    validator (ChainedValidator): A jsonclasses types object's chained validator.

  Returns:
    bool: Return True if the given type definition has writeonly marker inside
    else False.
  '''
  vs = validator.validators
  try:
    next(v for v in vs if type(v) is WriteonlyValidator)
    return True
  except StopIteration:
    return False
