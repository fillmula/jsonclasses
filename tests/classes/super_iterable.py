from __future__ import annotations
from typing import Optional, Any
from jsonclasses import jsonclass, types


@jsonclass
class SuperIterable:
    itsrp: Optional[str] = types.str.replace("abc", "ABC")
    itsr: Optional[str] = types.str.reverse()
    itl: Optional[list[Any]] = types.listof(types.any).reverse()
