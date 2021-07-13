from __future__ import annotations
from jsonclasses import jsonclass


def set_deleted(p: CBMProduct) -> None:
    p.deleted_count = p.deleted_count - 1


@jsonclass(on_delete=[set_deleted, set_deleted])
class CBMProduct:
    name: str
    deleted_count: int = 100
