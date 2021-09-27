from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SuperRound:
    round_value: Optional[int] = types.round.int
    ceil_value: Optional[int] = types.ceil.int
    floor_value: Optional[int] = types.floor.int
