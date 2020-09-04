from ..validators.unique_validator import UniqueValidator
from ..validators.chained_validator import ChainedValidator

def is_unique_type(validator: ChainedValidator) -> bool:
  '''Use this method to test if given types has unique marker inside. You mainly
  use this when implementing jsonclasses ORM integration.

  Args:
    validator (ChainedValidator): A jsonclasses types object's chained validator.

  Returns:
    bool: Return True if the given type definition has unique marker inside
    else False.
  '''
  vs = validator.validators
  try:
    next(v for v in vs if type(v) is UniqueValidator)
    return True
  except StopIteration:
    return False
