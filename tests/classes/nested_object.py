from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass


@jsonclass
class NestedList:
    id: Optional[str]
    value: dict[str, list[str]]


@jsonclass
class NestedDict:
    id: Optional[str]
    value: list[dict[str, str]]
