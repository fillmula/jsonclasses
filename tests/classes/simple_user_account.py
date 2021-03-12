from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SimpleUserAccount:
    email: Optional[str] = types.str.presentwithout('phone_number')
    phone_number: Optional[str] = types.str.presentwithout('email')
