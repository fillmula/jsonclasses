from typing import Union

def keypath(*args: Union[str, int]):
  retval = ''
  for arg in args:
    if retval != '':
      retval += '.'
    retval += str(arg)
  return retval
