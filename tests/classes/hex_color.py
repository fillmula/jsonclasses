from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass(validate_all_fields=True)
class HexColor:
    hex_color: str = types.str.hexcolor.required