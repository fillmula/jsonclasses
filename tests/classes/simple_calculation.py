from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SimpleCalculation:
    i_add: Optional[int] = types.int.add
    f_add: Optional[float] = types.float.add

    i_sub: Optional[int] = types.int.sub
    f_sub: Optional[float] = types.int.sub

    i_mul: Optional[int] = types.int.mul
    f_mul: Optional[float] = types.float.mul

    i_div: Optional[int] = types.int.div
    f_div: Optional[float] = types.float.div

    i_mod: Optional[int] = types.int.mod
    f_mod: Optional[float] = types.float.mod
