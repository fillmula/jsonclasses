from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass


@jsonclass
class SimpleUser:
    name: Optional[str]
    age: Optional[int]
