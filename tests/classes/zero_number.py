from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types

@jsonclass
class ZeroNumber:
    inegative: Optional[int] = types.int.negative
    ipositive: Optional[int] = types.int.positive
    inonnegative: Optional[int] = types.int.nonnegative
    inonpositive: Optional[int] = types.int.nonpositive
    fnegative: Optional[float] = types.float.negative
    fpositive: Optional[float] = types.float.positive
    fnonnegative: Optional[float] = types.float.nonnegative
    fnonpositive: Optional[float] = types.float.nonpositive
