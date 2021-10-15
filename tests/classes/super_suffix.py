from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SuperSuffix:
    s_hs: Optional[str] = types.str.hassuffix('python')
    l_hs: Optional[list[str]] = types.listof(str).hassuffix(['dd', 'ee', 'ff'])

    s_iso: Optional[str] = types.str.hassuffix('python')
    l_iso: Optional[list[str]] = types.listof(str).hassuffix(['ee', 'ff'])
