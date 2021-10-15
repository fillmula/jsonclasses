from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SuperInsertAt:
    s: Optional[str] = types.str.insertat(432, 3)
    l: Optional[list[str]] = types.listof(str).insertat('E', 1)
