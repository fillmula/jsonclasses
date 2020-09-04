from ..validators.writeonce_validator import WriteonceValidator
from ..validators.chained_validator import ChainedValidator

def is_writeonce_type(validator: ChainedValidator) -> bool:
  '''Use this method to test if given types has writeonce marker inside.

  Args:
    validator (ChainedValidator): A jsonclasses types object's chained validator.

  Returns:
    bool: Return True if the given type definition has writeonce marker inside
    else False.
  '''
  vs = validator.validators
  try:
    next(v for v in vs if type(v) is WriteonceValidator)
    return True
  except StopIteration:
    return False
