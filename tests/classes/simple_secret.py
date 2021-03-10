from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SimpleSecret:
    name: Optional[str]
    message: Optional[str] = types.str.internal
