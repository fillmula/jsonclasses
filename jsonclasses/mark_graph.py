"""This module defineds the JSON Class object mapping graph."""
from __future__ import annotations
from typing import Iterator, Union, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .jsonclass_object import JSONClassObject


class MarkClassTable:

    def __init__(self):
        self._primary_key_table = {}
        self._memory_id_table = {}

    def put(self, object: JSONClassObject) -> None:
        pk = object._id
        if pk is None:
            memory_id = hex(id(object))
            self._memory_id_table[memory_id] = object
        else:
            self.putp(pk, object)

    def putp(self, pk: Union[str, int], object: JSONClassObject) -> None:
        """Put object to this class table when designated primary key. This is
        useful when transforming and the values are not set yet.
        """
        self._primary_key_table[str(pk)] = object

    def has(self, object: JSONClassObject) -> bool:
        pk = object._id
        if pk is not None:
            if self._primary_key_table.get(str(pk)) is not None:
                return True
        memory_id = hex(id(object))
        if self._memory_id_table.get(memory_id) is not None:
            return True
        return False

    def get(self, object: JSONClassObject) -> Optional[JSONClassObject]:
        pk = object._id
        if pk is not None:
            if self._primary_key_table.get(str(pk)) is not None:
                return self._primary_key_table.get(str(pk))
        memory_id = hex(id(object))
        if self._memory_id_table.get(memory_id) is not None:
            return self._memory_id_table.get(memory_id)
        return None

    def getp(self, pk: Union[str, int]) -> Optional[JSONClassObject]:
        return self._primary_key_table.get(str(pk))

    def getm(self, memid: int) -> Optional[JSONClassObject]:
        return self._memory_id_table.get(hex(memid))


class MarkGraph:
    """The mark graph is a graph containing JSON Class objects. It's used for
    marking objects as handled when performing validating and serializing.
    """

    def __init__(self):
        self._class_tables: dict[str, MarkClassTable] = {}

    def class_table(self, cls: type) -> MarkClassTable[JSONClassObject]:
        if self._class_tables.get(cls.__name__) is None:
            self._class_tables[cls.__name__] = MarkClassTable()
        return self._class_tables[cls.__name__]

    def put(self, object: JSONClassObject) -> None:
        self.class_table(object.__class__).put(object)

    def putp(self, pk: Union[str, int], object: JSONClassObject) -> None:
        self.class_table(object.__class__).putp(pk, object)

    def has(self, object: JSONClassObject) -> bool:
        return self.class_table(object.__class__).has(object)

    def get(self, object: JSONClassObject) -> JSONClassObject:
        return self.class_table(object.__class__).get(object)

    def getp(self, cls: type[JSONClassObject],
             pk: Union[str, int]) -> Optional[JSONClassObject]:
        return self.class_table(cls).getp(pk)

    def getm(self, cls: type[JSONClassObject],
             memid: int) -> Optional[JSONClassObject]:
        return self.class_table(cls).getm(memid)

    def __iter__(self) -> Iterator:
        lst = []
        for ct in self._class_tables.values():
            for obj in ct._primary_key_table.values():
                if obj not in lst:
                    lst.append(obj)
            for obj in ct._memory_id_table.values():
                if obj not in lst:
                    lst.append(obj)
        return lst.__iter__()
