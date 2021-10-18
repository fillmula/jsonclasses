from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SimpleCalculation:

    i_add: Optional[int] = types.int.add(5)
    f_add: Optional[float] = types.float.add(2.5)
    c_add: Optional[float] = types.float.add(lambda: 2.5)
    t_add: Optional[float] = types.float.add(types.default(2.5))

    i_sub: Optional[int] = types.int.sub(5)
    f_sub: Optional[float] = types.float.sub(2.5)
    c_sub: Optional[float] = types.float.sub(lambda: 2.5)
    t_sub: Optional[float] = types.float.sub(types.default(2.5))

    i_mul: Optional[int] = types.int.mul(5)
    f_mul: Optional[float] = types.float.mul(2.5)
    c_mul: Optional[float] = types.float.mul(lambda: 2.5)
    t_mul: Optional[float] = types.float.mul(types.default(2.5))

    i_div: Optional[int] = types.int.div(5)
    f_div: Optional[float] = types.float.div(2.5)
    c_div: Optional[float] = types.float.div(lambda: 4.2)
    t_div: Optional[float] = types.float.div(types.default(4.2))

    i_mod: Optional[int] = types.int.mod(5)
    f_mod: Optional[float] = types.float.mod(2.5)
    c_mod: Optional[float] = types.float.mod(lambda: 3.5)
    t_mod: Optional[float] = types.float.mod(types.default(3.5))
