from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class TypedList:
    name: Optional[str]
    list: list[int] = types.listof(types.int).required
