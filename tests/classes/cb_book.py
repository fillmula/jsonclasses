from __future__ import annotations
from jsonclasses import jsonclass


def increase_updated_count(book: CBBook) -> None:
    book.updated_count += 1


@jsonclass(on_save=increase_updated_count)
class CBBook:
    name: str
    content: str
    updated_count: int = 0
