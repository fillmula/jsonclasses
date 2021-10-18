from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SimpleMath:
    i_pow: Optional[int] = types.int.pow(2)
    f_pow: Optional[float] = types.float.pow(2.5)
    c_pow: Optional[float] = types.float.pow(lambda: 2.5)
    t_pow: Optional[float] = types.float.pow(types.default(2.5))


    i_sqrt: Optional[int] = types.int.sqrt
    f_sqrt: Optional[float] = types.float.sqrt
