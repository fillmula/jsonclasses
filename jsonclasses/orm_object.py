"""This module defines `ORMObject`, the protocol that objects of JSONClasses
ORM integrations should implement.
"""
from __future__ import annotations
from typing import TypeVar, Any, TYPE_CHECKING
from .jobject import JObject
if TYPE_CHECKING:
    from .orm_query import (
        BaseQuery, ListQuery, IDQuery, SingleQuery, ExistQuery, IterateQuery
    )


T = TypeVar('T', bound='ORMObject')


class ORMObject(JObject):
    """The `ORMObject` protocol defines methods that JSONClasses ORM
    integrations should implement.
    """


    @classmethod
    def find(cls: type[T], *args, **kwargs: Any) -> ListQuery[T]:
        ...

    @classmethod
    def one(cls: type[T], *args, **kwargs: Any) -> SingleQuery[T]:
        ...

    @classmethod
    def id(cls: type[T], id: Any, *args, **kwargs) -> IDQuery[T]:
        ...

    @classmethod
    def linked(cls: type[T], *args, **kwargs: Any) -> BaseQuery[T]:
        ...

    @classmethod
    def exist(cls: type[T], **kwargs: Any) -> ExistQuery[T]:
        ...

    @classmethod
    def iterate(cls: type[T], **kwargs: Any) -> IterateQuery[T]:
        ...

    def _orm_delete(self: T, no_raise: bool = False) -> None:
        ...

    def _orm_restore(self: T) -> None:
        ...
