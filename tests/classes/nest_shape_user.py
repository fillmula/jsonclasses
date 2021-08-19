from __future__ import annotations
from typing import TypedDict
from jsonclasses import jsonclass, jsondict

@jsondict
class GroupedInner(TypedDict):
    on: bool
    off: bool


@jsondict
class Grouped(TypedDict):
    ios: GroupedInner
    android: GroupedInner


@jsonclass
class NestShapeUser:
    name: str
    grouped: Grouped

