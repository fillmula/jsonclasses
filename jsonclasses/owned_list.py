"""The owner observable list."""
from __future__ import annotations
from typing import (Generic, Iterable, Any, Optional, Protocol, TypeVar,
                    overload)

T_contra = TypeVar('T_contra', contravariant=True)
T = TypeVar('T')


class ListOwner(Protocol[T_contra]):

    def __olist_add__(self,
                      olist: OwnedList,
                      val: T_contra,
                      index: int) -> None: ...

    def __olist_del__(self,
                      olist: OwnedList,
                      val: T_contra,
                      index: int) -> None: ...


def is_list_owner(obj: Any):
    return hasattr(obj, '__olist_add__') and hasattr(obj, '__olist_del__')


class OwnedList(list, Generic[T]):

    @overload
    def __init__(self, owner: ListOwner) -> None: ...

    @overload
    def __init__(self, iterable: Iterable[T], owner: ListOwner) -> None: ...

    def __init__(self, *args, **kwargs) -> None:
        owner: Optional[ListOwner[T]] = kwargs.get('owner')
        iterable: Optional[Iterable[T]] = kwargs.get('iterable')
        for arg in args:
            if is_list_owner(arg):
                owner = arg
            else:
                iterable = arg
        if iterable is not None:
            super().__init__(iterable)
        else:
            super().__init__()
        self.owner = owner

# owner: list did add object at index
# owner: list did remove object at index
