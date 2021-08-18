from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class CellphoneTitle:
    cellphone_name: str = types.str.required
    cellphone_title: str = types.str.totitle.required

