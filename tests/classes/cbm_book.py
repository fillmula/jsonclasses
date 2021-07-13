from __future__ import annotations
from jsonclasses import jsonclass


def increase_updated_count(book: CBMBook) -> None:
    book.updated_count += 1


@jsonclass(on_save=[increase_updated_count, increase_updated_count])
class CBMBook:
    name: str
    content: str
    updated_count: int = 0
