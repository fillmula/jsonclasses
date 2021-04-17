from typing import TypedDict
from jsonclasses import jsonclass, types


class Settings(TypedDict):
    ios: bool
    android: bool
    name: str


@jsonclass
class DefaultShapeValue:
    settings: Settings = types.shape(Settings) \
        .default({'ios': False, 'android': True, 'name': 'set'})
