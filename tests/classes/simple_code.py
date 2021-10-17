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

    c_code: Optional[str] = types.str.length(lambda: 4)
    c_min_code: Optional[str] = types.str.minlength(lambda: 4)
    c_max_code: Optional[str] = types.str.maxlength(lambda: 8)

    cl_code: Optional[list[int]] = types.listof(int).length(lambda: 4)
    cl_min_code: Optional[list[int]] = types.listof(int).minlength(lambda: 4)
    cl_max_code: Optional[list[int]] = types.listof(int).maxlength(lambda: 8)

    t_code: Optional[str] = types.str.length(types.default(4))
    t_min_code: Optional[str] = types.str.minlength(types.default(4))
    t_max_code: Optional[str] = types.str.maxlength(types.default(8))

    tl_code: Optional[list[int]] = types.listof(int).length(types.default(4))
    tl_min_code: Optional[list[int]] = types.listof(int).minlength(types.default(4))
    tl_max_code: Optional[list[int]] = types.listof(int).maxlength(types.default(8))

    cd_code: Optional[str] = types.str.length(lambda: 4, lambda: 5)
    td_code: Optional[str] = types.str.length(types.default(4), types.default(4).add(1))
