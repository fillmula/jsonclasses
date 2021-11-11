from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class SuperFilter:
    list1: list[int] | None = types.listof(int).filter(lambda i: i % 2 == 0)
    list2: list[int] | None = types.listof(int).filter(types.mod(2).eq(0))
