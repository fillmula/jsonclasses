from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass(camelize_json_keys=True)
class SimpleFolder:
    name: Optional[str] = types.str
    config: dict[str, bool] = types.strict.shape({
        'display_size': types.bool.required,
        'display_date': types.bool.required
    }).required
