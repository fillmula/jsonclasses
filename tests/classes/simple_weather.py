from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass(camelize_json_keys=True)
class CamelizedWeather:
    data: dict[str, str] = types.dictof(str)


@jsonclass(camelize_json_keys=False)
class UncamelizedWeather:
    data: dict[str, str] = types.dictof(str)
