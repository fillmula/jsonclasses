from __future__ import annotations
from jsonclasses import jsonclass


@jsonclass(validate_all_fields=True)
class SimpleLanguage:
    name: str
    code: str
