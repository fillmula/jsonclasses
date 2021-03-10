from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class SimpleCode:
    code: str = types.str.length(4).required
