from typing import Dict, TypeVar

class_reference_map: Dict[str, type] = {}

T = TypeVar('T')

def referenced(cls: T) -> T:
  class_reference_map[cls.__name__] = cls
  return cls

def resolve_class(name: str) -> type:
  return class_reference_map[name]
