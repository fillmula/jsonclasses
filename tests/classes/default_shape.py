from typing import TypedDict
from jsonclasses import jsonclass, types


class Settings(TypedDict):
    ios: bool
    android: bool
    name: str


@jsonclass
class DefaultShape:
    settings: Settings = types.nonnull.shape({
        'ios': types.bool.default(True).required,
        'android': types.bool.default(True).required,
        'name': types.str.default('unnamed').required
    })
