from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SimpleMatch:
    m: Optional[str] = types.str.match('^a.*')
    cm: Optional[str] = types.str.match(lambda: '^a.*')
    tm: Optional[str] = types.str.match(types.default('^a.*'))
