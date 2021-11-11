from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class SuperMap:
    list1: list[int] | None = types.listof(int).map(lambda i: i + 1)
    list2: list[int] | None = types.listof(int).map(types.add(1))
