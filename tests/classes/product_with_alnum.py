from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class AlnumProductCode:
    product_name: str
    product_code: str = types.str.alnum.required

