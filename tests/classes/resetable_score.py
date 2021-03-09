from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass


@jsonclass(reset_all_fields=True)
class ResetableScore:
    name: str
    total: Optional[int]
    scores: list[float]
    history: dict[str, float]
