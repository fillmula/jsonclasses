from __future__ import annotations
from typing import Any, Container, Optional
from jsonclasses import jsonclass, types
from tests.classes.onwrite import callback


def callback_l(i: int) -> list:
    return i % 2

def callback_t(i: int) -> tuple:
    return  i % 2

def callback_s(i: int) -> set:
    return  i % 2

@jsonclass
class SuperFilter:
    l_fil: Optional[list[int]] = types.listof(int).filter(callback_l)
