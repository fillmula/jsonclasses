from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SuperAppend:
    s: Optional[str] = types.str.append('3432')
    l: Optional[list[str]] = types.listof(str).append('7788')

    cs: Optional[str] = types.str.append(lambda: '3432')
    cl: Optional[list[str]] = types.listof(str).append(lambda: '7788')

    ts: Optional[str] = types.str.append(types.default('3432'))
    tl: Optional[list[str]] = types.listof(str).append(types.default('7788'))
