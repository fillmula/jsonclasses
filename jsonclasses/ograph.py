"""This module defineds the JSON Class object mapping graph."""
from __future__ import annotations
from typing import Iterator, NamedTuple, Union, TYPE_CHECKING
from .isjsonclass import isjsonobject
from .excs import (UnlinkableJSONClassException,
                         JSONClassGraphMergeConflictException)
if TYPE_CHECKING:
    from .jobject import JObject


class CompareResult(NamedTuple):
    """When merging object graph, conflicted objects will be compared. One will
    be kept and one will be outdated.
    """
    kept: JObject
    """The updated one to keep."""
    outdated: JObject
    """The obsolete one to remove."""


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

    def compare(self: OGraph,
                obj1: JObject,
                obj2: JObject) -> CompareResult:
        if obj1.is_new and obj2.is_new:
            raise JSONClassGraphMergeConflictException('both objects are new')
        elif obj1.is_new or obj2.is_new:
            raise JSONClassGraphMergeConflictException('1 object is new')
        if obj1._updated_at == obj2._updated_at:
            if obj1.is_modified and obj2.is_modified:
                raise JSONClassGraphMergeConflictException('both objects are '
                                                           'modified')
            elif obj2.is_modified:
                return CompareResult(kept=obj2, outdated=obj1)
            else:
                return CompareResult(kept=obj1, outdated=obj2)
        elif obj1._updated_at is None:
            return CompareResult(kept=obj2, outdated=obj1)
        elif obj2._updated_at is None:
            return CompareResult(kept=obj1, outdated=obj2)
        elif obj1._updated_at > obj2._updated_at:
            return CompareResult(kept=obj1, outdated=obj2)
        else:
            return CompareResult(kept=obj2, outdated=obj1)

    def merged_graph(self: OGraph, graph2: OGraph) -> OGraph:
        """Get a new graph which is a combination of two graphs.
        """
        if self is graph2:
            return self
        pool: list[CompareResult] = []
        graph = self.copy()
        for object in graph2:
            if not graph.has(object):
                graph.put(object)
            elif graph.get(object) is object:
                graph.put(object)
            else:
                result = self.compare(graph.get(object), object)
                graph.put(result.kept)
                if result not in pool:
                    pool.append(result)
        for result in pool:
            self.alter_links(result)
        for object in graph:
            object._graph = graph
        return graph

    def alter_links(self: OGraph, result: CompareResult) -> None:
        """Alter all linked objects reference to the new object.
        """
        for field in result.outdated.__class__.cdef.fields:
            if not field.fdef.is_ref:
                continue
            item_or_items = getattr(result.outdated, field.name)
            items: list[JObject] = []
            if isjsonobject(item_or_items):
                items = [item_or_items]
            elif isinstance(item_or_items, list):
                items = item_or_items
            for item in items:
                item_field = field.foreign_field
                item_value = getattr(item, item_field.name)
                if item_value is result.outdated:
                    setattr(item, item_field.name, result.kept)
                elif isinstance(item_value, list):
                    index = item_value.index(result.outdated)
                    item_value[index] = result.kept
            if result.outdated._unlinked_objects.get(field.name) is not None:
                outdated_items = result.outdated._unlinked_objects. \
                    get(field.name)
                for item in outdated_items:
                    result.kept._add_unlinked_object(field.name, item)
                del result.outdated._unlinked_objects[field.name]
        result.outdated._is_outdated = True
