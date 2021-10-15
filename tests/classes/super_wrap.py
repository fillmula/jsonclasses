from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SuperWrap:
    s: list[str] = types.listof(str).wrapintolist
