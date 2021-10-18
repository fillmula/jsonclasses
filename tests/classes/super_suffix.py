from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SuperSuffix:
    s_hs: Optional[str] = types.str.hassuffix('python')
    l_hs: Optional[list[str]] = types.listof(str).hassuffix(['dd', 'ee', 'ff'])
    c_hs: Optional[str] = types.str.hassuffix(lambda: 'python')
    c_l_hs: Optional[list[str]] = types.listof(str).hassuffix(lambda: ['dd', 'ee', 'ff'])
    t_hs: Optional[str] = types.str.hassuffix(types.default('python'))
    t_l_hs: Optional[list[str]] = types.listof(str).hassuffix(types.default(['dd', 'ee', 'ff']))

    s_iso: Optional[str] = types.str.issuffixof('python')
    l_iso: Optional[list[str]] = types.listof(str).issuffixof(['ee', 'ff'])
    c_iso: Optional[str] = types.str.issuffixof(lambda: 'python')
    c_l_iso: Optional[list[str]] = types.listof(str).issuffixof(lambda: ['ee', 'ff'])
    t_iso: Optional[str] = types.str.issuffixof(types.default('python'))
    t_l_iso: Optional[list[str]] = types.listof(str).issuffixof(types.default(['ee', 'ff']))
