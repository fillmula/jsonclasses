from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SimpleContact:
    email: Optional[str] = types.str.presentwithout(['phone_no', 'address'])
    phone_no: Optional[str] = types.str.presentwithout(['email', 'address'])
    address: Optional[str] = types.str.presentwithout(['phone_no', 'email'])
