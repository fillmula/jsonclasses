from typing import Optional
from dataclasses import dataclass
from .json_object import JSONObject
from .graph import register_class
from .config import Config

def jsonclass(
  *args,
  graph: Optional[str] = 'default',
  camelize_json_keys: Optional[bool] = None,
  camelize_db_keys: Optional[bool] = None
):
  '''The jsonclass object class decorator. To declare a jsonclass class, use
  this syntax:

    @jsonclass
    class MyObject(JSONObject):
      my_field_one: str
      my_field_two: bool
  '''
  if len(args) == 1:
    cls = args[0]
    if not isinstance(cls, type):
      raise ValueError('@jsonclass should be used to decorate a class.')
    elif not issubclass(cls, JSONObject):
      raise ValueError('@jsonclass should be used to decorate subclasses of JSONObject.')
    else:
      config = Config(graph=graph, camelize_json_keys=camelize_json_keys, camelize_db_keys=camelize_db_keys)
      config.install_on_class(cls)
      return register_class(dataclass(cls, init=False), graph=graph)
  else:
    def parametered_jsonclass(cls):
      return jsonclass(
        cls,
        graph=graph,
        camelize_json_keys=camelize_json_keys,
        camelize_db_keys=camelize_db_keys
      )
    return parametered_jsonclass
