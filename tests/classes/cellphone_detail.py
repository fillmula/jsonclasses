from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class CellphoneDetail:
    cellphone_name: str = types.str.required
    cellphone_detail: str = types.str.toupper.required

