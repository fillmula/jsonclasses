"""This module defineds the JSON Class object mapping graph."""
from __future__ import annotations
from typing import Iterator, TypeVar, Union, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .json_object import JSONObject
    T = TypeVar('T', bound=JSONObject)


class ClassTable:

    def __init__(self):
        self._primary_key_table = {}
        self._memory_id_table = {}

    def put(self, object: T) -> None:
        pk = object._id
        if pk is None:
            memory_id = hex(id(object))
            self._memory_id_table[memory_id] = object
        else:
            self.putp(pk, object)

    def putp(self, pk: Union[str, int], object: T) -> None:
        """Put object to this class table when designated primary key. This is
        useful when transforming and the values are not set yet.
        """
        self._primary_key_table[str(pk)] = object

    def has(self, object: T) -> bool:
        pk = object._id
        if pk is not None:
            if self._primary_key_table.get(str(pk)) is not None:
                return True
        memory_id = hex(id(object))
        if self._memory_id_table.get(memory_id) is not None:
            return True
        return False

    def get(self, object: T) -> Optional[T]:
        pk = object._id
        if pk is not None:
            if self._primary_key_table.get(str(pk)) is not None:
                return self._primary_key_table.get(str(pk))
        memory_id = hex(id(object))
        if self._memory_id_table.get(memory_id) is not None:
            return self._memory_id_table.get(memory_id)
        return None

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
        self._detached_table: dict[str, list[T]] = {}

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

    def get(self, object: T) -> T:
        return self.class_table(object.__class__).get(object)

    def getp(self, cls: type[T], pk: Union[str, int]) -> Optional[T]:
        return self.class_table(cls).getp(pk)

    def getm(self, cls: type[T], memid: int) -> Optional[T]:
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

    def put_detached(self, owner: type[T], detached: type[T]) -> None:
        oid: str = ''
        oid = owner._id
        if oid is None:
            oid = hex(id(owner))
        if self._detached_table.get(oid) is None:
            self._detached_table[oid] = []
        if detached not in self._detached_table[oid]:
            self._detached_table[oid].append(detached)

    def all_detached(self, owner: type[T]) -> list[type[T]]:
        oid: str = owner._id
        if oid is None:
            oid = hex(id(owner))
        retval = self._detached_table.get(oid)
        if retval is None:
            return []
        return retval

    def del_detached(self, owner: type[T], detached: type[T]) -> None:
        lst = self.all_detached(owner)
        if detached in lst:
            lst.remove(detached)
