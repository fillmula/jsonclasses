from __future__ import annotations
from jsonclasses import jsonclass, types


def check_author(book: GSBook, operator: GSBookAuthor) -> bool:
    return book.author.id == operator.id and operator.paid_user


@jsonclass
class GSBookAuthor:
    id: str
    name: str
    paid_user: bool
    books: list[GSBook] = types.nonnull.listof('GSBook').linkedby('author')


@jsonclass(can_update=check_author)
class GSBook:
    name: str
    author: GSBookAuthor = types.instanceof('GSBookAuthor').linkto.required
