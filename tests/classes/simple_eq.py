from __future__ import annotations
from typing import Any, Optional
from jsonclasses import jsonclass, types

@jsonclass
class SimpleEq:
    eq_value: Optional[Any] = types.any.eq("dsadsa")

    ceq_value: Optional[Any] = types.any.eq(lambda: "dsadsa")
    teq_value: Optional[Any] = types.any.eq(types.default("dsadsa"))

@jsonclass
class SimpleNeq:
    neq_value: Optional[Any] = types.any.neq("dsadsa")

    cneq_value: Optional[Any] = types.any.neq(lambda: "dsadsa")
    tneq_value: Optional[Any] = types.any.neq(types.default("dsadsa"))
