from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SuperPrepend:
    s: Optional[str] = types.str.prepend('3432')
    l: Optional[list[str]] = types.listof(str).prepend('7788')

    cs: Optional[str] = types.str.prepend(lambda: '3432')
    cl: Optional[list[str]] = types.listof(str).prepend(lambda: '7788')

    ts: Optional[str] = types.str.prepend(types.default('3432'))
    tl: Optional[list[str]] = types.listof(str).prepend(types.default('7788'))
