from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SimpleOrder:
    name: Optional[str]
    quantity: Optional[int] = types.int.default(1)
