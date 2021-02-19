"""The owner observable list."""
from __future__ import annotations
from typing import Generic, Iterable, Any, Protocol, TypeVar, MutableSequence

T_contra = TypeVar('T_contra', contravariant=True)
_T = TypeVar('_T')


class ListOwner(Protocol[T_contra]):

    def __olist_add__(self,
                      olist: OwnedList,
                      idx: int,
                      val: T_contra) -> None: ...

    def __olist_del__(self, olist: OwnedList, val: T_contra) -> None: ...

    def __olist_sor__(self, olist: OwnedList) -> None: ...

    def __olist_will_change__(self, olist: OwnedList) -> None: ...


def is_list_owner(obj: Any):
    has_add = hasattr(obj, '__olist_add__')
    has_del = hasattr(obj, '__olist_del__')
    has_sor = hasattr(obj, '__olist_sor__')
    has_change = hasattr(obj, '__olist_will_change__')
    return has_add and has_del and has_sor and has_change


class OwnedList(list, MutableSequence[_T], Generic[_T]):

    @property
    def owner(self) -> ListOwner:
        return self._owner

    @owner.setter
    def owner(self, val: ListOwner) -> None:
        self._owner = val

    @property
    def keypath(self) -> str:
        return self._keypath

    @keypath.setter
    def keypath(self, val: str) -> None:
        self._keypath = val

    def append(self, value: _T) -> None:
        self.owner.__olist_will_change__(self)
        super().append(value)
        self.owner.__olist_add__(self, len(self) - 1, value)

    def extend(self, values: Iterable[_T]) -> None:
        curlen = len(self)
        if len(values) > 0:
            self.owner.__olist_will_change__(self)
        super().extend(values)
        for v in values:
            self.owner.__olist_add__(self, curlen, v)
            curlen += 1

    def insert(self, index: int, value: _T) -> None:
        curlen = len(self)
        self.owner.__olist_will_change__(self)
        super().insert(index, value)
        idx = min(curlen, index)
        self.owner.__olist_add__(self, idx, value)

    def remove(self, value: _T) -> None:
        self.owner.__olist_will_change__(self)
        super().remove(value)
        self.owner.__olist_del__(self, value)

    def sort(self, **kwargs) -> None:  # TODO: fix argument type hint
        self.owner.__olist_will_change__(self)
        super().sort(**kwargs)
        self.owner.__olist_sor__(self)

    def clear(self) -> None:
        items = [item for item in self]
        self.owner.__olist_will_change__(self)
        super().clear()
        for item in items:
            self.owner.__olist_del__(self, item)

    def pop(self, *args) -> _T:  # TODO: fix argument type hint
        self.owner.__olist_will_change__(self)
        retval = super().pop(*args)
        self.owner.__olist_del__(self, retval)
        return retval

    def reverse(self) -> None:
        self.owner.__olist_will_change__(self)
        super().reverse()
        self.owner.__olist_sor__(self)

    def __add__(self, x: list[_T]) -> list[_T]:
        return super().__add__(x)

    def __iadd__(self, x: Iterable[_T]) -> OwnedList[_T]:
        if len(x) > 0:
            self.owner.__olist_will_change__(self)
        curlen = len(self)
        retval = super().__iadd__(x)
        for v in x:
            self.owner.__olist_add__(self, curlen, v)
            curlen += 1
        return retval

    def __imul__(self, n: int) -> OwnedList[_T]:
        len_self = 0
        if n <= 0:
            remove_list = list(self)
            add_list: list[_T] = []
        elif n == 1:
            remove_list = []
            add_list = []
        else:
            remove_list = []
            ran = range(0, n - 1)
            add_list = []
            for i in ran:
                for item in self:
                    add_list.append(item)
            len_self = len(self)
        if len(remove_list) > 0 or len(add_list) > 0:
            self.owner.__olist_will_change__(self)
        retval = super().__imul__(n)
        for item in remove_list:
            self.owner.__olist_del__(self, item)
        for item in add_list:
            self.owner.__olist_add__(self, len_self, item)
            len_self += 1
        return retval

    def __setitem__(self, *args) -> None:
        len_self = len(self)
        if isinstance(args[0], int):
            idx: int = args[0]
            if idx < 0:
                idx = len_self + idx
            val = self[idx] if 0 <= idx < len_self else None
            self.owner.__olist_will_change__(self)
            super().__setitem__(*args)
            self.owner.__olist_del__(self, val)
            self.owner.__olist_add__(self, idx, args[1])
        elif isinstance(args[0], slice):
            slc: slice = args[0]
            remove_list = self[slc]
            start = slc.start or 0
            step = slc.step or 1
            if start < 0:
                start = len_self + start
            start = min(max(0, start), len_self)
            self.owner.__olist_will_change__(self)
            super().__setitem__(*args)
            for item in remove_list:
                self.owner.__olist_del__(self, item)
            for item in args[1]:
                self.owner.__olist_add__(self, start, item)
                start += step
        else:
            super().__setitem__(*args)

    def __delitem__(self, *args) -> None:
        if isinstance(args[0], int):
            len_self = len(self)
            idx: int = args[0]
            if idx < 0:
                idx = len_self + idx
            val = self[idx] if 0 <= idx < len_self else None
            self.owner.__olist_will_change__(self)
            super().__delitem__(*args)
            self.owner.__olist_del__(self, val)
        elif isinstance(args[0], slice):
            slc: slice = args[0]
            remove_list = self[slc]
            self.owner.__olist_will_change__(self)
            super().__delitem__(*args)
            for item in remove_list:
                self.owner.__olist_del__(self, item)
        else:
            super().__delitem__(*args)
