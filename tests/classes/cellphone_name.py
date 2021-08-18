from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class CellphoneName:
    cellphone_name: str = types.str.tocap.required
    cellphone_title: str = types.str.required

