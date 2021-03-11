from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class PasswordUser:
    name: str = types.str.required
    password: str = types.str.writeonly.required
