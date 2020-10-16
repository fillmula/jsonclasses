"""This module defineds the JSON Class object mapping graph."""
from __future__ import annotations
from typing import TypeVar, Union, Optional, TYPE_CHECKING
from .fields import pk_field
if TYPE_CHECKING:
    from .json_object import JSONObject
    T = TypeVar('T', bound=JSONObject)


class ClassTable:

    def __init__(self):
        self._primary_key_table = {}
        self._memory_id_table = {}

    def put(self, object: T) -> None:
        try:
            pkf = pk_field(object).field_name
            pk = getattr(object, pkf)
        except AttributeError:
            pk = None
        if pk is None:
            memory_id = hex(id(object))
            self._memory_id_table[memory_id] = object
        else:
            self.putp(pk, object)

    def putp(self, pk: Union[str, int], object: T) -> None:
        self._primary_key_table[str(pk)] = object

    def has(self, object: T) -> bool:
        try:
            pkf = pk_field(object).field_name
            pk = getattr(object, pkf)
        except AttributeError:
            pk = None
        if pk is not None:
            if self._primary_key_table.get(str(pk)) is not None:
                return True
        memory_id = hex(id(object))
        if self._memory_id_table.get(memory_id) is not None:
            return True
        return False

    def getp(self, pk: Union[str, int]) -> Optional[T]:
        return self._primary_key_table.get(str(pk))

    def getm(self, memid: int) -> Optional[T]:
        return self._memory_id_table.get(hex(memid))


class ObjectGraph:
    """The object graph is a graph containing JSON Class objects. It has two
    main usages. First, it's used for tracking and referencing objects within
    the same objects from a query result. Second, it's used for marking objects
    as handled when performing validating and serializing.
    """

    def __init__(self):
        self._class_tables: dict[str, ClassTable] = {}

    def class_table(self, cls: type[T]) -> ClassTable[T]:
        if self._class_tables.get(cls.__name__) is None:
            self._class_tables[cls.__name__] = ClassTable()
        return self._class_tables[cls.__name__]

    def put(self, object: T) -> None:
        self.class_table(object.__class__).put(object)

    def putp(self, pk: Union[str, int], object: T) -> None:
        self.class_table(object.__class__).putp(pk, object)

    def has(self, object: T) -> bool:
        return self.class_table(object.__class__).has(object)

    def getp(self, cls: type[T], pk: Union[str, int]) -> Optional[T]:
        return self.class_table(cls).getp(pk)

    def getm(self, cls: type[T], memid: int) -> Optional[T]:
        return self.class_table(cls).getm(memid)
