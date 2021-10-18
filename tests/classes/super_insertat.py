from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SuperInsertAt:
    s: Optional[str] = types.str.insertat(432, 3)
    l: Optional[list[str]] = types.listof(str).insertat('E', 1)

    cs: Optional[str] = types.str.insertat(lambda: 432, lambda: 3)
    ts: Optional[str] = types.str.insertat(types.default(432), types.default(3))
