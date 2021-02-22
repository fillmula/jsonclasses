from __future__ import annotations
from typing import Annotated, Final

Link = Annotated

linkto: Final[str] = 'linkto'


def linkedby(key: str) -> str:
    return f"linkedby('{key}')"


def linkedthru(key: str) -> str:
    return f"linkedthru('{key}')"
