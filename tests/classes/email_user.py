from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass(validate_all_fields=True)
class EmailUserAnalysis:
    username: str
    email: str = types.str.email.required
