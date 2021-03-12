from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass(camelize_json_keys=False)
class SimpleNode:
    name: Optional[str] = types.str
    config: dict[str, bool] = types.shape({
        'display_size': types.bool.required,
        'display_date': types.bool.required
    }).required
