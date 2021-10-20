from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types

@jsonclass
class SuperInverse:
    iv: Optional[bool] = types.bool.inverse
