from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class Format:
    color1: str = types.str.fmt(types.prepend('#'))
    color2: str = types.str.fmt(lambda color: '#' + color)
