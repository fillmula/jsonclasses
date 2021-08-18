from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass(validate_all_fields=True)
class EmailUser:
    username: str
    email: str = types.str.email.required
