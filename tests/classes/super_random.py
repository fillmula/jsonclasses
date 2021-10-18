from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types

@jsonclass
class SuperRandom:
    random_digits: Optional[int] = types.int.randomdigits(1)
    random_alnums: Optional[int] = types.int.randomalnums(1)
    random_alnumpuncs: Optional[int] = types.int.randomalnumpuncs(1)
    random_int: Optional[int] = types.int.randomint(10, 11)
    random_float: Optional[float] = types.float.randomfloat(10.0, 10.0)

    random_cfloat: Optional[float] = types.float.randomfloat(lambda: 10.0, lambda: 10.0)
    random_tfloat: Optional[float] = types.float.randomfloat(types.default(10.0), types.default(10.0))
