from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SuperStr:
    password: Optional[str] = types.str.salt
