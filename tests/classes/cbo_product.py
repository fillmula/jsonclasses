from __future__ import annotations
from jsonclasses import jsonclass


def set_deleted(p: CBOProduct, o: int) -> None:
    p.deleted_count = p.deleted_count - o


@jsonclass(on_delete=set_deleted)
class CBOProduct:
    name: str
    deleted_count: int = 100
