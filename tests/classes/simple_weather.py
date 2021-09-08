from __future__ import annotations
from jsonclasses import jsonclass, types
from jsonclasses.keypath import camelize_key, identical_key, underscore_key


@jsonclass(key_encoding_strategy=camelize_key,
           key_decoding_strategy=underscore_key)
class CamelizedWeather:
    data: dict[str, str] = types.dictof(str)


@jsonclass(key_encoding_strategy=identical_key,
           key_decoding_strategy=identical_key)
class UncamelizedWeather:
    data: dict[str, str] = types.dictof(str)
