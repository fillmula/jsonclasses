from __future__ import annotations
from jsonclasses.keypath import camelize_key, underscore_key
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass(key_encoding_strategy=camelize_key,
           key_decoding_strategy=underscore_key)
class SimpleFolder:
    name: Optional[str] = types.str
    config: dict[str, bool] = types.strict.shape({
        'display_size': types.bool.required,
        'display_date': types.bool.required
    }).required
