"""This module defines ORM queries. These are used in conjuction with ORM
objects.
"""
from __future__ import annotations
from typing import (
    Protocol, Optional, TypeVar, Union, Any, Generator, Iterator, TYPE_CHECKING
)
if TYPE_CHECKING:
    from .orm_object import ORMObject


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
