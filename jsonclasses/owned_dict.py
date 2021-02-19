"""The owner observable dict."""
from __future__ import annotations
from typing import Generic, Any, Protocol, TypeVar, Union, MutableMapping
from collections.abc import Mapping, Iterable

KT_contra = TypeVar('KT_contra', contravariant=True)
VT_contra = TypeVar('VT_contra', contravariant=True)
_KT = TypeVar('_KT')
_VT = TypeVar('_VT')
_T = TypeVar('_T')


class DictOwner(Protocol[KT_contra, VT_contra]):

    def __odict_add__(self,
                      odict: OwnedDict,
                      key: KT_contra,
                      val: VT_contra) -> None: ...

    def __odict_del__(self, odict: OwnedDict, val: VT_contra) -> None: ...

    def __odict_will_change__(self, olist: OwnedDict) -> None: ...


def is_dict_owner(obj: Any):
    has_add = hasattr(obj, '__odict_add__')
    has_del = hasattr(obj, '__odict_del__')
    has_change = hasattr(obj, '__odict_will_change__')
    return has_add and has_del and has_change


class OwnedDict(dict, MutableMapping[_KT, _VT], Generic[_KT, _VT]):

    @property
    def owner(self) -> DictOwner:
        return self._owner

    @owner.setter
    def owner(self, val: DictOwner) -> None:
        self._owner = val

    @property
    def keypath(self) -> str:
        return self._keypath

    @keypath.setter
    def keypath(self, val: str) -> None:
        self._keypath = val

    def clear(self) -> None:
        values = [value for value in self.values()]
        self.owner.__odict_will_change__(self)
        super().clear()
        for value in values:
            self.owner.__odict_del__(self, value)

    def pop(self, *args) -> Union[_VT, _T]:
        len_args = len(args)
        if not (1 <= len_args <= 2):
            super().pop(*args)
        try:
            self.owner.__odict_will_change__(self)
            retval = super().pop(args[0])
            self.owner.__odict_del__(self, retval)
            return retval
        except KeyError as e:
            if len_args > 1:
                return args[1]
            raise e

    def popitem(self) -> tuple[_KT, _VT]:
        self.owner.__odict_will_change__(self)
        result = super().popitem()
        self.owner.__odict_del__(self, result[1])
        return result

    def setdefault(self, *args) -> _VT:
        will_set = False
        len_args = len(args)
        if len_args == 2:
            try:
                self[args[0]]
            except KeyError:
                will_set = True
        if will_set:
            self.owner.__odict_will_change__(self)
        retval = super().setdefault(*args)
        if will_set:
            self.owner.__odict_add__(self, args[0], args[1])
        return retval

    def update(self, *args, **kwargs: _VT) -> None:
        len_args = len(args)
        if not (0 <= len_args <= 1):
            return super().update(*args, **kwargs)
        if len_args == 0:
            new_dict = kwargs
        elif isinstance(args[0], Mapping):
            new_dict = dict(args[0], **kwargs)
        elif isinstance(args[0], Iterable):
            new_dict = dict(args[0], **kwargs)
        else:
            new_dict = {}
        items_to_del = [i[1] for i in self.items() if i[0] in new_dict.keys()]
        self.owner.__odict_will_change__(self)
        super().update(*args, **kwargs)
        for v in items_to_del:
            self.owner.__odict_del__(self, v)
        for k, v in new_dict.items():
            self.owner.__odict_add__(self, k, v)

    def __setitem__(self, k: _KT, v: _VT) -> None:
        remove_callback = False
        removed = None
        try:
            removed = self[k]
            remove_callback = True
        except KeyError:
            pass
        self.owner.__odict_will_change__(self)
        super().__setitem__(k, v)
        if remove_callback:
            self.owner.__odict_del__(self, removed)
        self.owner.__odict_add__(self, k, v)

    def __delitem__(self, k: _KT) -> None:
        try:
            removed = self[k]
        except KeyError:
            removed = None
        self.owner.__odict_will_change__(self)
        super().__delitem__(k)
        self.owner.__odict_del__(self, removed)

    def __ior__(self, rhs: Iterable) -> OwnedDict[_KT, _VT]:
        new_dict = dict(rhs)
        items_to_del = [i[1] for i in self.items() if i[0] in new_dict.keys()]
        self.owner.__odict_will_change__(self)
        retval = super().__ior__(rhs)
        for v in items_to_del:
            self.owner.__odict_del__(self, v)
        for k, v in new_dict.items():
            self.owner.__odict_add__(self, k, v)
        return retval
