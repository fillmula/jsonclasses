from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SuperAppend:
    s: Optional[str] = types.str.append('3432')
    l: Optional[list[str]] = types.listof(str).append('7788')
