from ..validators.required_validator import RequiredValidator
from ..validators.chained_validator import ChainedValidator

def is_required_type(validator: ChainedValidator) -> bool:
  '''Use this method to test if given types has required marker inside. You
  mainly use this when implementing jsonclasses ORM integration.

  Args:
    validator (ChainedValidator): A jsonclasses types object's chained validator.

  Returns:
    bool: Return True if the given type definition has required marker inside
    else False.
  '''
  vs = validator.validators
  try:
    next(v for v in vs if type(v) is RequiredValidator)
    return True
  except StopIteration:
    return False
