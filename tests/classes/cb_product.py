from __future__ import annotations
from jsonclasses import jsonclass


def set_deleted(p: CBProduct) -> None:
    p.deleted_count = p.deleted_count - 1


@jsonclass(on_delete=set_deleted)
class CBProduct:
    name: str
    deleted_count: int = 100
