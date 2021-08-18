from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class CellphoneDescription:
    cellphone_name: str = types.str.required
    cellphone_description: str = types.str.tolower.required

