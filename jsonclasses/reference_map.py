from typing import Dict

class_reference_map: Dict[str, type] = {}

def referenced(cls: type):
  class_reference_map[cls.__name__] = cls
  return cls

def resolve_class(name: str) -> type:
  return class_reference_map[name]
