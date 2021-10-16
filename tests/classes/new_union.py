from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class NewUnion:
    name: str | None
    code: str | int | None


@jsonclass
class NewRUnion:
    code: str | int
    items: dict[str, str | int] | list[str]


@jsonclass
class NewOUnion:
    items: dict[str, str | int] | list[str] | None
