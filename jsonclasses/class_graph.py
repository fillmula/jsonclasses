"""This module defineds the JSON Class class mapping graph."""
from __future__ import annotations
from typing import Optional, TypeVar, TYPE_CHECKING
from inspect import getmodule
if TYPE_CHECKING:
    from .json_object import JSONObject
    from .fields import Field
    T = TypeVar('T', bound=JSONObject)


class JSONClassRedefinitionError(Exception):
    """This error is raised when you define a JSON Class with a name that
    exists before.
    """

    def __init__(self, new_cls: type[JSONObject], exist_cls: type[JSONObject]):
        name = new_cls.__name__
        original_module = getmodule(exist_cls)
        assert original_module is not None
        original_file = original_module.__file__
        new_module = getmodule(new_cls)
        assert new_module is not None
        new_file = new_module.__file__
        graph = exist_cls.config.class_graph
        message = (f'Existing JSON Class \'{name}\' in graph \'{graph}\' is '
                   f'defined at \'{original_file}\'. Cannot define new JSON '
                   f'Class with same name in same graph \'{graph}\' at '
                   f'\'{new_file}\'.')
        super().__init__(message)


class JSONClassNotFoundError(Exception):
    """This exception is raised when a specified JSON Class is not found on a
    graph.
    """
    def __init__(self, name: str, graph: str = 'default'):
        message = (f'JSON Class with name \'{name}\' in graph \'{graph}\' is '
                   'not found.')
        super().__init__(message)


class ClassGraph:

    def __init__(self, graph_name: str):
        self._graph_name = graph_name
        self._map: dict[str, type[JSONObject]] = {}
        self._fields_map: dict[str, list[Field]] = {}
        self._dict_fields_map: dict[str, dict[str, Field]] = {}

    def add(self, cls: type[T]) -> type[T]:
        """Add a JSON Class to the graph."""
        if self._map.get(cls.__name__) is not None:
            raise JSONClassRedefinitionError(cls, self._map[cls.__name__])
        self._map[cls.__name__] = cls
        return cls

    def get(self, cls_name: str) -> type[JSONObject]:
        try:
            return self._map[cls_name]
        except KeyError:
            raise JSONClassNotFoundError(name=cls_name, graph=self._graph_name)

    def set_fields(self, cls: type[T], fields: list[Field]) -> None:
        name = cls.__name__
        if self._map.get(name) is None:
            raise JSONClassNotFoundError(name=name, graph=self._graph_name)
        self._fields_map[name] = fields

    def get_fields(self, cls: type[T]) -> Optional[list[Field]]:
        name = cls.__name__
        if self._map.get(name) is None:
            raise JSONClassNotFoundError(name=name, graph=self._graph_name)
        return self._fields_map.get(name)

    def set_dict_fields(self, cls: type[T], fields: dict[str, Field]) -> None:
        name = cls.__name__
        if self._map.get(name) is None:
            raise JSONClassNotFoundError(name=name, graph=self._graph_name)
        self._dict_fields_map[name] = fields

    def get_dict_fields(self, cls: type[T]) -> Optional[dict[str, Field]]:
        name = cls.__name__
        if self._map.get(name) is None:
            raise JSONClassNotFoundError(name=name, graph=self._graph_name)
        return self._dict_fields_map.get(name)


class ClassGraphMap:

    def __init__(self):
        self._map: dict[str, ClassGraph] = {}

    def graph(self, graph_name: str) -> ClassGraph:
        if self._map.get(graph_name) is None:
            self._map[graph_name] = ClassGraph(graph_name=graph_name)
        return self._map[graph_name]


class_graph_map = ClassGraphMap()
