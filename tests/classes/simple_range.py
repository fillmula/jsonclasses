from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SimpleRange:
    i: Optional[int] = types.int.range(1, 10)
    ic: Optional[int] = types.int.range(lambda: 1, lambda: 10)
    it: Optional[int] = types.int.range(types.default(1), types.default(10))
