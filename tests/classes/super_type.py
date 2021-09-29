from __future__ import annotations
from typing import Optional, Any
from jsonclasses import jsonclass, types


@jsonclass
class SuperType:
    tl: Optional[list[Any]] = types.tolist.listof(Any)
    tb: Optional[bool] = types.tobool.bool
    ti: Optional[int] = types.toint.int
    tf: Optional[float] = types.tofloat.float
    ts: Optional[str] = types.tostr.str
