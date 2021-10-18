from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SuperPrefix:
    s_hp: Optional[str] = types.str.hasprefix('un')
    loi_hp: Optional[list[int]] = types.listof(int).hasprefix([1, 4, 5])
    los_hp: Optional[list[str]] = types.listof(str).hasprefix(['a', 'd'])

    cs_hp: Optional[str] = types.str.hasprefix(lambda: 'un')
    ts_hp: Optional[str] = types.str.hasprefix(types.default('un'))

    s_ipo: Optional[str] = types.str.isprefixof('unhappy')
    loi_ipo: Optional[list[int]] = types.listof(int).isprefixof([1, 4, 5, 3, 2, 8])
    los_ipo: Optional[list[str]] = types.listof(str).isprefixof(['a', 'd', 'f', 'g'])
