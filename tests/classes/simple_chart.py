from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SimpleChart:
    name: Optional[str]
    partitions: dict[str, float] = types.dictof(types.float.max(1)).required
