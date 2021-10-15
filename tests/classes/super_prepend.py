from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SuperPrepend:
    s: Optional[str] = types.str.prepend('3432')
    l: Optional[str] = types.str.prepend('7788')
