"""This module defineds the JSON Class object mapping graph."""
from __future__ import annotations
from .fields import pk_field
from typing import TypeVar, cast, TYPE_CHECKING
if TYPE_CHECKING:
    from .json_object import JSONObject
    T = TypeVar('T', bound=JSONObject)


class ClassTable:

    def __init__(self):
        self._primary_key_table = {}
        self._memory_id_table = {}

    def put(self, object: T) -> None:
        try:
            pk = pk_field(object).field_name
            pk_value = getattr(object, cast(str, pk))
        except AttributeError:
            pk_value = None
        if pk_value is None:
            memory_id = hex(id(object))
            self._memory_id_table[memory_id] = object
        else:
            self._primary_key_table[pk_value] = object

    def has(self, object: T) -> bool:
        try:
            pk = pk_field(object).field_name
            pk_value = getattr(object, cast(str, pk))
        except AttributeError:
            pk_value = None
        if pk_value is not None:
            if self._primary_key_table.get(pk_value) is not None:
                return True
        memory_id = hex(id(object))
        if self._memory_id_table.get(memory_id) is not None:
            return True
        return False


class ObjectGraph:

    def __init__(self):
        self._class_tables: dict[str, ClassTable] = {}

    def class_table(self, cls: type[T]) -> ClassTable[T]:
        if self._class_tables.get(cls.__name__) is None:
            self._class_tables[cls.__name__] = ClassTable()
        return self._class_tables[cls.__name__]

    def put(self, object: T) -> None:
        self.class_table(object.__class__).put(object)

    def has(self, object: T) -> bool:
        return self.class_table(object.__class__).has(object)
