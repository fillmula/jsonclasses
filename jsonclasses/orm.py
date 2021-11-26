"""This module defines ORM protocols, the protocols that objects of JSONClasses
ORM integrations should implement.
"""
from __future__ import annotations
from typing import (
    Protocol, Optional, TypeVar, Union, Any, Generator, Iterator
)
from .jobject import JObject


T = TypeVar('T', bound='ORMObject', covariant=True)
U = TypeVar('U', bound='BaseQuery')
V = TypeVar('V', bound='BaseListQuery')


class Subquery(Protocol[U]):
    name: str
    query: Optional[U]


class BaseQuery(Protocol[T]):

    def __init__(self: U, cls: type[T]) -> None:
        ...

    def include(self: U, name: str, query: Optional[BaseQuery] = None) -> U:
        ...


class BaseListQuery(BaseQuery[T]):

    def __init__(self: V,
                 cls: type[T],
                 filter: Union[dict[str, Any], str, None] = None) -> None:
        ...

    def order(self: V, field: str, sort: Optional[int] = None) -> V:
        ...

    def skip(self: V, n: int) -> V:
        ...

    def limit(self: V, n: int) -> V:
        ...

    def page_number(self: V, n: int) -> V:
        ...

    def page_no(self: V, n: int) -> V:
        ...

    def page_size(self: V, n: int) -> V:
        ...

    def pick(self: V, fields: list[str]) -> V:
        ...

    def omit(self: V, fields: list[str]) -> V:
        ...


class ListQuery(BaseListQuery[T]):

    def exec(self) -> list[T]:
        ...

    def __await__(self) -> Generator[None, None, list[T]]:
        ...


class SingleQuery(BaseListQuery[T]):

    def exec(self) -> T:
        ...

    def __await__(self) -> Generator[None, None, T]:
        ...

    @property
    def optional(self) -> OptionalSingleQuery:
        ...


class OptionalSingleQuery(BaseListQuery[T]):

    def exec(self) -> Optional[T]:
        ...

    def __await__(self) -> Generator[None, None, Optional[T]]:
        ...



class BaseIDQuery(BaseQuery[T]):

    def __init__(self: U, cls: type[T], id: Union[str, int]) -> None:
        ...


class IDQuery(BaseIDQuery[T]):

    def exec(self) -> T:
        ...

    def __await__(self) -> Generator[None, None, T]:
        ...

    @property
    def optional(self) -> OptionalIDQuery:
        ...


class OptionalIDQuery(BaseIDQuery[T]):

    def exec(self) -> Optional[T]:
        ...

    def __await__(self) -> Generator[None, None, Optional[T]]:
        ...


class IDSQuery(BaseQuery[T]):

    def exec(self) -> list[T]:
        ...

    def __await__(self) -> Generator[None, None, list[T]]:
        ...


class ExistQuery(BaseListQuery[T]):

    def exec(self) -> bool:
        ...

    def __await__(self) -> Generator[None, None, bool]:
        ...


class IterateQuery(BaseListQuery[T]):

    def exec(self) -> Iterator[T]:
        ...

    def __await__(self) -> Generator[None, None, Iterator[T]]:
        ...


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
    def ids(cls: type[T], ids: list[Any], *args, **kwargs) -> IDSQuery[T]:
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
