from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SuperAffix:
    hp: Optional[str] = types.str.hasprefix('unhappy')
