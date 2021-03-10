from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class SimpleAuthcode:
    name: str = types.str.required
    code: str = types.str.temp.required
