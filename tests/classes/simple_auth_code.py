from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SimpleAuthCode:
    calling_code: Optional[str] = types.str.presentwith('phone_number')
    phone_number: Optional[str] = types.str
    code: str = types.str.required
