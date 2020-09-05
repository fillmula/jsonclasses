from typing import Dict, Optional
from inspect import getmodule

register_table: Dict[str, Dict[str, type]] = {}

def __graph_table(graph: str = 'default'):
  if register_table.get(graph) is None:
    register_table[graph] = {}
  return register_table[graph]

class JSONClassRedefinitionError(Exception):
  def __init__(self, new_cls: type, exist_cls: type):
    name = new_cls.__name__
    original_file = getmodule(exist_cls).__file__
    new_file = getmodule(new_cls).__file__
    graph = exist_cls.config.graph
    message = f'Existing JSON Class \'{name}\' in graph \'{graph}\' is defined at \'{original_file}\'. Cannot define new JSON Class with same name in same graph \'{graph}\' at \'{new_file}\'.'
    super().__init__(message)

class JSONClassNotFoundError(Exception):
  def __init__(self, name: str, graph: str = 'default'):
    message = f'JSON Class with name \'{name}\' in graph \'{graph}\' is not found.'
    super().__init__(message)

def register_class(cls: type, graph: str = 'default'):
  name = cls.__name__
  graph_table = __graph_table(graph)
  exist_cls = graph_table.get(name)
  if exist_cls is not None:
    raise JSONClassRedefinitionError(cls, exist_cls)
  graph_table[name] = cls
  return cls

def get_registered_class(name: str, graph: str = 'default', sibling: Optional[type] = None):
  if sibling is not None:
    graph = sibling.config.graph
  cls = __graph_table(graph).get(name)
  if cls is None:
    raise JSONClassNotFoundError(name, graph)
  return cls
