from __future__ import annotations
from typing import Optional, Union
from datetime import datetime
from jsonclasses import jsonclass, types


@jsonclass
class SimpleMixed:
    name: Optional[str]
    mixed: Optional[Union[int, str]] = types.union([str, int])


@jsonclass
class SimpleMixedT:
    value: int | str = types.union([
        types.str.append('123'),
        types.int.add(123)
    ])


@jsonclass
class SimpleMixedU:
    value: datetime | str
