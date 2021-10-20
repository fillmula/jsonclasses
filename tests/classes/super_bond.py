from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SuperBond:
    i_ub: Optional[int] = types.int.upperbond(150)
    f_ub: Optional[float] = types.float.upperbond(150.0)
    c_ub: Optional[int] = types.int.upperbond(lambda: 150)
    t_ub: Optional[int] = types.int.upperbond(types.default(150))

    i_lb: Optional[int] = types.int.lowerbond(1)
    f_lb: Optional[float] = types.float.lowerbond(1.0)
    c_lb: Optional[int] = types.int.lowerbond(lambda: 1)
    t_lb: Optional[int] = types.float.lowerbond(types.default(1))
