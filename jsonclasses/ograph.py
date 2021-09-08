"""This module defineds the JSON Class object mapping graph."""
from __future__ import annotations
from typing import Iterator, NamedTuple, Union, TYPE_CHECKING
from .isjsonclass import isjsonobject
from .excs import (UnlinkableJSONClassException,
                         JSONClassGraphMergeConflictException)
if TYPE_CHECKING:
    from .jobject import JObject


class OGraph:
    """The object graph is a graph containing JSON Class objects. It has two
    main usages. First, it's used for tracking and referencing objects within
    the same objects from a query result. Second, it's used for marking objects
    as handled when performing validating and serializing.
    """

    def __init__(self: OGraph,
                 objects: Union[list[JObject],
                                JObject, None] = None) -> None:
        self._maps: dict[str, dict[str, JObject]] = {}
        try:
            if isinstance(objects, list):
                for object in objects:
                    self.put(object)
            if isjsonobject(objects):
                self.put(objects)
        except UnlinkableJSONClassException:
            return

    def __iter__(self) -> Iterator[JObject]:
        lst: list[JObject] = []
        for table in self._maps.values():
            for obj in table.values():
                lst.append(obj)
        return lst.__iter__()

    def _object_map(self: OGraph,
                    name: str) -> dict[str, JObject]:
        if self._maps.get(name) is None:
            self._maps[name] = {}
        return self._maps[name]

    def _check_get_str_id(self: OGraph, object: JObject) -> str:
        primary_value = object._id
        if primary_value is None:
            if object.__class__.cdef.primary_field:
                has_field = True
            else:
                has_field = False
            raise UnlinkableJSONClassException(type(object), has_field)
        return str(primary_value)

    def put(self: OGraph, object: JObject) -> None:
        """Put an object into object graph. When conflict, this object
        overrides the existing one on the graph.
        """
        primary_value = self._check_get_str_id(object)
        class_name = object.__class__.__name__
        object_map = self._object_map(class_name)
        object_map[primary_value] = object

    def has(self: OGraph, object: JObject) -> bool:
        """Check whether an object is existing in the object graph.
        """
        return self.get(object) is not None

    def get(self: OGraph, object: JObject) -> JObject:
        """Get an object from the graph which matches the provided object.
        """
        primary_value = self._check_get_str_id(object)
        class_name = object.__class__.__name__
        object_map = self._object_map(class_name)
        return object_map.get(primary_value)

    def copy(self: OGraph) -> OGraph:
        """Get a copy of this object graph.
        """
        new_graph = OGraph()
        for key, map in self._maps.items():
            new_graph._maps[key] = {}
            for name, obj in map.items():
                new_graph._maps[key][name] = obj
        return new_graph


    def merged_graph(self: OGraph, graph2: OGraph) -> OGraph:
        """Get a new graph which is a combination of two graphs.
        """
        if self is graph2:
            return self
        graph = self.copy()
        for object in graph2:
            if not graph.has(object):
                graph.put(object)
            elif graph.get(object) is object:
                graph.put(object)
            else:
                raise JSONClassGraphMergeConflictException(
                    'multiple objects represent same object: ', object)
        for object in graph:
            object._graph = graph
        return graph
