from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SimpleWordbook:
    name: Optional[str]
    words: list[str] = types.nonnull.listof(str)
