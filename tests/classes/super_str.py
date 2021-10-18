from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SuperStr:
    password: Optional[str] = types.str.salt
    pads: Optional[str] = types.str.padstart("s", 10)
    padis: Optional[int] = types.int.padstart("s", 10)
    pade: Optional[str] = types.str.padend("e", 10)
    padie: Optional[int] = types.int.padend("e", 10)

    padce: Optional[str] = types.str.padend(lambda: "e", lambda: 10)
    padte: Optional[str] = types.str.padend(types.default("e"), types.default(10))

    c_pads: Optional[str] = types.str.padstart(lambda: "s", lambda: 10)
    t_pads: Optional[str] = types.str.padstart(types.default("s"), types.default(10))
