from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class SimpleOrder:
    name: str
    quantity: int = types.int.default(1)
