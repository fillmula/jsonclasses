from __future__ import annotations
from jsonclasses import jsonclass


@jsonclass
class SimpleAddress:
    line_one: str
    line_two: str
