from __future__ import annotations
from jsonclasses import jsonclass, types
from jsonclasses.keypath import camelize_key, identical_key, underscore_key


@jsonclass(input_key_strategy='camelize',
           output_key_strategy='underscore')
class CamelizedWeather:
    data_data: dict[str, str] = types.dictof(str)


@jsonclass(input_key_strategy='identical',
           output_key_strategy='identical')
class UncamelizedWeather:
    data_data: dict[str, str] = types.dictof(str)
