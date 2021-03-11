from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class RoleUser:
    username: str = types.str.required
    role: str = types.str.readonly.default('normal').required
