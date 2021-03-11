from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class TypedRecord:
    name: Optional[str]
    dict_record: dict[str, str] = types.nonnull.dictof(types.str)
