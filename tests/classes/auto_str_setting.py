from __future__ import annotations
from typing import Optional, TypedDict
from jsonclasses import jsonclass, jsondict


@jsondict
class Preference(TypedDict):
    ios: bool
    android: bool


@jsonclass
class AutoStrSetting:
    user: Optional[str]
    preference: Preference
