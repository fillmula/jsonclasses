from __future__ import annotations
from typing import Any, Optional
from jsonclasses import jsonclass, types


@jsonclass
class SimpleAt:
    a: Optional[Any] = types.any.at("name")
    ca: Optional[Any] = types.any.at(lambda: "name")
    ta: Optional[Any] = types.any.at(types.default("name"))
