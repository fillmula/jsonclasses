from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SimpleList:
    name: Optional[str]
    list: list[int] = types.listof(int).required
