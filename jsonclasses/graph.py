"""This module defineds the internal JSON Class mapping graph."""
from __future__ import annotations
from typing import Dict, Optional, Type, TypeVar, Any, TYPE_CHECKING
from inspect import getmodule
if TYPE_CHECKING:
    from .json_object import JSONObject
    T = TypeVar('T', bound=JSONObject)


register_table: Dict[str, Dict[str, Any]] = {}


def __graph_table(graph: str = 'default') -> Dict[str, Type[T]]:
    """Returns the graph table containing map graphs."""
    if register_table.get(graph) is None:
        register_table[graph] = {}
    return register_table[graph]


class JSONClassRedefinitionError(Exception):
    """This error is raised when you define a JSON Class with a name that
    exists before.
    """

    def __init__(self, new_cls: Type[T], exist_cls: Type[T]):
        name = new_cls.__name__
        original_module = getmodule(exist_cls)
        assert original_module is not None
        original_file = original_module.__file__
        new_module = getmodule(new_cls)
        assert new_module is not None
        new_file = new_module.__file__
        graph = exist_cls.config.graph
        message = (f'Existing JSON Class \'{name}\' in graph \'{graph}\' is '
                   f'defined at \'{original_file}\'. Cannot define new JSON Class '
                   f'with same name in same graph \'{graph}\' at \'{new_file}\'.')
        super().__init__(message)


class JSONClassNotFoundError(Exception):
    """This exception is raised when a specified JSON Class is not found on a
    graph.
    """
    def __init__(self, name: str, graph: str = 'default'):
        message = (f'JSON Class with name \'{name}\' in graph \'{graph}\' is '
                   'not found.')
        super().__init__(message)


def register_class(
    cls: Type[T],
    graph: str = 'default'
) -> Type[T]:
    """Register a JSON Class on the graph."""
    name = cls.__name__
    graph_table = __graph_table(graph)  # type: Dict[str, Type[T]]
    exist_cls = graph_table.get(name)
    if exist_cls is not None:
        raise JSONClassRedefinitionError(cls, exist_cls)
    graph_table[name] = cls
    return cls


def get_registered_class(
    name: str,
    graph: str = 'default',
    sibling: Optional[Type[T]] = None
) -> Type[T]:
    """Get a JSON Class on graph for name."""
    if sibling is not None:
        graph = sibling.config.graph
    graph_table: Dict[str, Type[T]] = __graph_table(graph)
    if graph_table is not None:
        cls: Optional[Type[T]] = graph_table.get(name)
        if cls is None:
            raise JSONClassNotFoundError(name=name, graph=graph)
        return cls
    raise JSONClassNotFoundError(name=name, graph=graph)
