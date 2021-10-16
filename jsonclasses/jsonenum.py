"""
This module contains `jsonenum`, the decorator for enums used with jsonclasses.
"""
from typing import Optional, Union, Callable, TypeVar, overload
from enum import Enum
from .cgraph import CGraph


T = TypeVar('T', bound=type[Enum])

@overload
def jsonenum(cls: T) -> T: ...


@overload
def jsonenum(
    cls: None,
    class_graph: Optional[str] = 'default'
) -> Callable[[T], T]: ...


@overload
def jsonenum(
    cls: type,
    class_graph: Optional[str] = 'default'
) -> T: ...


def jsonenum(
    cls: Optional[type] = None,
    class_graph: Optional[str] = 'default',
) -> Union[Callable[[T], T], T]:
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
        cgraph = CGraph(class_graph)
        cgraph.put_enum(cls)
        return cls
    else:
        def parametered_jsonenum(cls):
            return jsonenum(
                cls,
                class_graph=class_graph)
        return parametered_jsonenum
