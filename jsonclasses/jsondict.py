"""
This module contains `jsondict`, the decorator for typed dicts used with
jsonclasses.
"""
from typing import Optional, Union, Callable, overload
from .jsonclass_graph import JSONClassGraph


@overload
def jsondict(cls: type) -> type: ...


@overload
def jsondict(
    cls: None,
    class_graph: Optional[str] = 'default'
) -> Callable[[type], type[dict]]: ...


@overload
def jsondict(
    cls: type,
    class_graph: Optional[str] = 'default'
) -> type[dict]: ...


def jsondict(
    cls: Optional[type] = None,
    class_graph: Optional[str] = 'default',
) -> Union[Callable[[type], type[dict]], type[dict]]:
    """The jsondict typed dict class decorator. To declare a jsonclass typed
    dict, use this syntax:

      @jsondict
      class MyDict(TypedDict):
        my_field_one: str
        my_field_two: bool
    """
    if cls is not None:
        if not isinstance(cls, type):
            raise ValueError('@jsondict should be used to decorate a class.')
        class_graph = JSONClassGraph(class_graph)
        class_graph.put_dict(cls)
        return cls
    else:
        def parametered_jsondict(cls):
            return jsondict(
                cls,
                class_graph=class_graph)
        return parametered_jsondict
