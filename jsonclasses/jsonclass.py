from dataclasses import dataclass

def jsonclass(original_class):
  '''The jsonclass object class decorator. To declare a jsonclass class, use
  this syntax:

    @jsonclass
    class MyObject(JSONObject):
      my_field_one: str
      my_field_two: bool
  '''
  return dataclass(original_class, init=False)
