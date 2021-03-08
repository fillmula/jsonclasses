from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SimpleProject:
    name: Optional[str]
    attendees: list[str] = types.listof(types.str.minlength(2)).required
