"""
This module contains `jsonenum`, the decorator for enums used with jsonclasses.
"""
from typing import Optional, Union, Callable, overload
from .cgraph import CGraph


@overload
def jsonenum(cls: type) -> type: ...


@overload
def jsonenum(
    cls: None,
    cgraph: Optional[str] = 'default'
) -> Callable[[type], type[dict]]: ...


@overload
def jsonenum(
    cls: type,
    cgraph: Optional[str] = 'default'
) -> type[dict]: ...


def jsonenum(
    cls: Optional[type] = None,
    cgraph: Optional[str] = 'default',
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
        cgraph = CGraph(cgraph)
        cgraph.put_enum(cls)
        return cls
    else:
        def parametered_jsonenum(cls):
            return jsonenum(
                cls,
                cgraph=cgraph)
        return parametered_jsonenum
