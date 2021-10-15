from __future__ import annotations
from typing import Any, Optional
from jsonclasses import jsonclass, types


def callback_l(i: int) -> list:
    return  i+1

def callback_t(i: int) -> tuple:
    return  i+1

@jsonclass
class SuperMap:
    l_m: Optional[list[int]] = types.listof(int).map(callback_l)
