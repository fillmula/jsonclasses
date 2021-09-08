from __future__ import annotations
from jsonclasses import jsonclass


@jsonclass(strict_input=False)
class SimpleTenant:
    name: str
    age: int
