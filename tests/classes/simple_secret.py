from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SimpleSecret:
    name: Optional[str] = types.str.trim
    message: Optional[str] = types.str.internal
