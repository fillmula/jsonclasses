"""
This module contains `jsonenum`, the decorator for enums used with jsonclasses.
"""
from typing import Optional, Union, Callable, overload
from .jsonclass_graph import JSONClassGraph


@overload
def jsonenum(cls: type) -> type: ...


@overload
def jsonenum(
    cls: None,
    class_graph: Optional[str] = 'default'
) -> Callable[[type], type[dict]]: ...


@overload
def jsonenum(
    cls: type,
    class_graph: Optional[str] = 'default'
) -> type[dict]: ...


def jsonenum(
    cls: Optional[type] = None,
    class_graph: Optional[str] = 'default',
) -> Union[Callable[[type], type[dict]], type[dict]]:
    """The jsonclass enum decorator. To declare a jsonclass enum, use this
    syntax:

      @jsonenum
      class MyColor(Enum):
        RED = 1
        GREEN = 2
        BLUE = 3
    """
    if cls is not None:
        if not isinstance(cls, type):
            raise ValueError('@jsonenum should be used to decorate a class.')
        class_graph = JSONClassGraph(class_graph)
        class_graph.put_enum(cls)
        return cls
    else:
        def parametered_jsonenum(cls):
            return jsonenum(
                cls,
                class_graph=class_graph)
        return parametered_jsonenum
