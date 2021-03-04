from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class SimpleAccount:
    username: str
    password: str = types.str.writeonly.required
