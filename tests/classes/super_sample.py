from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SuperSample:
    digits: Optional[str] = types.str.randomdigits(8)
    alnums: Optional[str] = types.str.randomalnums(8)
    alnumpunc: Optional[str] = types.str.randomalnumpuncs(8)
