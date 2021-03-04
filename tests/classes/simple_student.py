from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass


@jsonclass
class SimpleStudent:
    age: Optional[int] = 20
    graduated: bool = False
