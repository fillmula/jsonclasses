from __future__ import annotations
from jsonclasses import jsonclass


def increase_updated_count(book: CBOBook, operator: int) -> None:
    book.updated_count += operator


@jsonclass(on_save=increase_updated_count)
class CBOBook:
    name: str
    content: str
    updated_count: int = 0
