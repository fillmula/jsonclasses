from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SimpleLen:
    str: int = types.default("abcdefghoi").len.int.required
    list: int = types.default([1, 2, 3, 4, 5, 6]).len.int.required
