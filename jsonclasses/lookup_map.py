"""This module defines JSON Class lookup maps."""
from __future__ import annotations
from typing import Optional, TypeVar, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from .json_object import JSONObject
    T = TypeVar('T', bound=JSONObject)
    ItemMap = dict[str, T]
    ClassMap = dict[str, ItemMap]


class LookupMap:
    """The lookup map provides defined objects query functionalities.

    When transforming from raw input to JSON Class object, data referenced to
    same object are fetched from this lookup map and reused. In a object graph,
    only one object can represent one entity.

    When validating an object graph, same object is not validated twice.
    """

    def __init__(self) -> None:
        self.cls_map: ClassMap = {}

    def fetch(self, cls_name: str, id: Union[str, int]) -> Optional[T]:
        """Get an item on map by `cls_name` and `id`."""
        item_map = self.cls_map.get(cls_name)
        if item_map is None:
            return None
        return item_map.get(str(id))

    def put(self, cls_name: str, id: Union[str, int], item: T) -> None:
        """Put an item on map."""
        if self.cls_map.get(cls_name) is None:
            self.cls_map[cls_name] = {}
        item_map = self.cls_map.get(cls_name)
        assert item_map is not None
        item_map[str(id)] = item
