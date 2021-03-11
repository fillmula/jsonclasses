from __future__ import annotations
from typing import Optional, Union
from jsonclasses import jsonclass, types


@jsonclass
class SimpleMixed:
    name: Optional[str]
    mixed: Optional[Union[int, str]] = types.oneoftype([str, int])
