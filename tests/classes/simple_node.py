from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types
from jsonclasses.keypath import identical_key


@jsonclass(key_encoding_strategy=identical_key,
           key_decoding_strategy=identical_key)
class SimpleNode:
    name: Optional[str] = types.str
    config: dict[str, bool] = types.shape({
        'display_size': types.bool.required,
        'display_date': types.bool.required
    }).required
