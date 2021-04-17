from typing import Optional, TypedDict
from jsonclasses import jsonclass


class Preference(TypedDict):
    ios: bool
    android: bool


@jsonclass
class AutoSetting:
    user: Optional[str]
    preference: Preference
