from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SuperInt:
    i_o: Optional[int] = types.int.odd
    i_e: Optional[int] = types.int.even
    i_a: Optional[int] = types.int.abs
