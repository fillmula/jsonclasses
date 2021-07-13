from __future__ import annotations
from jsonclasses import jsonclass, types


def check_owner(book: GMBook, operator: GMBookAuthor) -> bool:
    return book.author.id == operator.id


def check_tier(book: GMBook, operator: GMBookAuthor) -> bool:
    return operator.paid_user


@jsonclass
class GMBookAuthor:
    id: str
    name: str
    paid_user: bool
    books: list[GMBook] = types.nonnull.listof('GMBook').linkedby('author')


@jsonclass(can_update=[check_owner, check_tier])
class GMBook:
    name: str
    author: GMBookAuthor = types.instanceof('GMBookAuthor').linkto.required
