from __future__ import annotations
from typing import Any, Optional
from jsonclasses import jsonclass, types

@jsonclass
class SimpleEq:
    eq_value: Optional[Any] = types.any.eq("dsadsa")
    neq_value: Optional[Any] = types.any.neq("dsadsa")
