from typing import Optional, List
from ..validators import Validator, EagerValidator

def eager_validator_index_after_index(vs: List[Validator], index: int) -> Optional[int]:
  '''This function returns the first eager validator index after given index.

  Args:
    vs (List[Validator]): A list of validators usually from chained validator.
    index (int): The starting index to begin search with.

  Returns:
    Optional[int]: The found index or None.
  '''
  try:
    return vs.index(next(v for v in vs[index:] if type(v) is EagerValidator))
  except StopIteration:
    return None
