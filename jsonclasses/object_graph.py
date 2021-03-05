"""This module defineds the JSON Class object mapping graph."""
from __future__ import annotations
from typing import Iterator, Union, Optional, TYPE_CHECKING
from .isjsonclass import isjsonobject
from .exceptions import UnlinkableJSONClassException
if TYPE_CHECKING:
    from .jsonclass_object import JSONClassObject


class ObjectGraph:
    """The object graph is a graph containing JSON Class objects. It has two
    main usages. First, it's used for tracking and referencing objects within
    the same objects from a query result. Second, it's used for marking objects
    as handled when performing validating and serializing.
    """

    def __init__(self: ObjectGraph,
                 objects: Union[list[JSONClassObject],
                                JSONClassObject, None] = None) -> None:
        self._maps: dict[str, dict[str, JSONClassObject]] = {}
        try:
            if isinstance(objects, list):
                for object in objects:
                    self.put(object)
            if isjsonobject(objects):
                self.put(objects)
        except UnlinkableJSONClassException:
            return

    def __iter__(self) -> Iterator[JSONClassObject]:
        lst: list[JSONClassObject] = []
        for table in self._maps.values():
            for obj in table.values():
                lst.append(obj)
        return lst.__iter__()

    def _object_map(self: ObjectGraph,
                    name: str) -> dict[str, JSONClassObject]:
        if self._maps.get(name) is None:
            self._maps[name] = {}
        return self._maps[name]

    def _check_get_str_id(self: ObjectGraph, object: JSONClassObject) -> str:
        primary_value = object._id
        if primary_value is None:
            if object.__class__.definition.primary_field:
                has_field = True
            else:
                has_field = False
            raise UnlinkableJSONClassException(type(object), has_field)
        return str(primary_value)

    def put(self: ObjectGraph, object: JSONClassObject) -> None:
        """Put an object into object graph. When conflict, this object
        overrides the existing one on the graph.
        """
        primary_value = self._check_get_str_id(object)
        class_name = object.__class__.__name__
        object_map = self._object_map(class_name)
        object_map[primary_value] = object

    def has(self: ObjectGraph, object: JSONClassObject) -> bool:
        """Check whether an object is existing in the object graph.
        """
        return self.get(object) is not None

    def get(self: ObjectGraph, object: JSONClassObject) -> JSONClassObject:
        """Get an object from the graph which matches the provided object.
        """
        primary_value = self._check_get_str_id(object)
        class_name = object.__class__.__name__
        object_map = self._object_map(class_name)
        return object_map.get(primary_value)

    def copy(self: ObjectGraph) -> ObjectGraph:
        """Get a copy of this object graph.
        """
        new_graph = ObjectGraph()
        for key, map in self._maps.items():
            new_graph._maps[key] = {}
            for name, obj in map.items():
                new_graph._maps[key][name] = obj
        return new_graph
