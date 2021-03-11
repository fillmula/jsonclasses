from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class NullableList:
    name: Optional[str]
    list: list[int] = types.listof(types.nullable.int).required
