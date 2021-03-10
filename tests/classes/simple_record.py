from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SimpleRecord:
    name: Optional[str]
    dict_record: dict[str, str] = types.nonnull.dictof(str)
    shape_record: dict[str, str] = types.nonnull.shape({
        'a': types.str,
        'b': types.str
    })
