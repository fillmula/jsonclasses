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

    fcf_gt: Optional[float] = types.float.gt(lambda: 5.5)
    ftf_gt: Optional[float] = types.float.gt(types.default(5.5))

    c_lt: Optional[int] = types.int.lt(lambda: 5)
    t_lt: Optional[int] = types.int.lt(types.default(5))

    c_gte: Optional[int] = types.int.gte(lambda: 5)
    t_gte: Optional[int] = types.int.gte(types.default(5))

    c_lte: Optional[int] = types.int.lte(lambda: 5)
    t_lte: Optional[int] = types.int.lte(types.default(5))

    c_min: Optional[int] = types.int.min(lambda: 5)
    t_min: Optional[int] = types.int.min(types.default(5))

    c_max: Optional[int] = types.int.max(lambda: 5)
    t_max: Optional[int] = types.int.max(types.default(5))
