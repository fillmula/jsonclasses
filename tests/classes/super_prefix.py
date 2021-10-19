from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SuperPrefix:
    s_hp: Optional[str] = types.str.hasprefix('un')
    loi_hp: Optional[list[int]] = types.listof(int).hasprefix([1, 4, 5])
    los_hp: Optional[list[str]] = types.listof(str).hasprefix(['a', 'd'])
    c_hp: Optional[str] = types.str.hasprefix(lambda: 'un')
    c_loi_hp: Optional[list[int]] = types.listof(int).hasprefix(lambda: [1, 4, 5])
    c_los_hp: Optional[list[str]] = types.listof(str).hasprefix(lambda: ['a', 'd'])
    t_hp: Optional[str] = types.str.hasprefix(types.default('un'))
    t_loi_hp: Optional[list[int]] = types.listof(int).hasprefix(types.default([1, 4, 5]))
    t_los_hp: Optional[list[str]] = types.listof(str).hasprefix(types.default(['a', 'd']))
    cs_hp: Optional[str] = types.str.hasprefix(lambda: 'un')
    ts_hp: Optional[str] = types.str.hasprefix(types.default('un'))


@jsonclass
class IsPrefixOf:
    s_ipo: Optional[str] = types.str.isprefixof('unhappy')
    loi_ipo: Optional[list[int]] = types.listof(int).isprefixof([1, 4, 5, 3, 2, 8])
    los_ipo: Optional[list[str]] = types.listof(str).isprefixof(['a', 'd', 'f', 'g'])
    c_ipo: Optional[str] = types.str.isprefixof(lambda: 'unhappy')
    c_loi_ipo: Optional[list[int]] = types.listof(int).isprefixof(lambda: [1, 4, 5, 3, 2, 8])
    c_los_ipo: Optional[list[str]] = types.listof(str).isprefixof(lambda: ['a', 'd', 'f', 'g'])
    t_ipo: Optional[str] = types.str.isprefixof(types.default('unhappy'))
    t_loi_ipo: Optional[list[int]] = types.listof(int).isprefixof(types.default([1, 4, 5, 3, 2, 8]))
    t_los_ipo: Optional[list[str]] = types.listof(str).isprefixof(types.default(['a', 'd', 'f', 'g']))
