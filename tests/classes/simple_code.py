from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SimpleCode:
    code: Optional[str] = types.str.length(4)
    min_code: Optional[str] = types.str.minlength(4)
    max_code: Optional[str] = types.str.maxlength(8)

    l_code: Optional[list[int]] = types.listof(int).length(4)
    l_min_code: Optional[list[int]] = types.listof(int).minlength(4)
    l_max_code: Optional[list[int]] = types.listof(int).maxlength(8)
