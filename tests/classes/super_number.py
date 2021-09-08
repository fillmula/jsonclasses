from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SuperNumber:
    if_min: Optional[int] = types.int.min(5)
    if_max: Optional[int] = types.int.max(5)
    if_gte: Optional[int] = types.int.gte(5)
    if_lte: Optional[int] = types.int.lte(5)
    if_gt: Optional[int] = types.int.gt(5)
    if_lt: Optional[int] = types.int.lt(5)
    ff_min: Optional[float] = types.float.min(5.5)
    ff_max: Optional[float] = types.float.max(5.5)
    ff_gte: Optional[float] = types.float.gte(5.5)
    ff_lte: Optional[float] = types.float.lte(5.5)
    ff_gt: Optional[float] = types.float.gt(5.5)
    ff_lt: Optional[float] = types.float.lt(5.5)
