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
