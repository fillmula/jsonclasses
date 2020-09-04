from typing import List, Dict, Any

class ObjectNotFoundException(Exception):
  '''ObjectNotFoundException is designed to be raised by jsonclasses ORM
  integration implementations. Server authors and jsonclasses server integration
  authors should catch this to present error to frontend clients.
  '''
  def __init__(self, message: str):
    self.message = message
    super().__init__(self.message)

class UniqueFieldException(Exception):
  def __init__(self, value: Any, field: str, obj: Any):
    self.message = f'Value \'{value}\' of field \'{field}\' of object {obj} exists in database.'
    super().__init__(self.message)

class ValidationException(Exception):
  '''ValidationException is throwed on jsonclass object validation or on eager
  validation. Server authors and jsonclasses server integration authors should
  catch this to present error to frontend clients.
  '''

  def __init__(self, keypath_messages: Dict[str, str], root: Any):
    self.keypath_messages = keypath_messages
    self.message = self.formatted_keypath_messages()
    self.root = root
    super().__init__(self.message)

  def formatted_keypath_messages(self):
    retval = 'Json classes validation failed:\n'
    for k, v in self.keypath_messages.items():
      retval += f'  \'{k}\': {v}\n'
    return retval
