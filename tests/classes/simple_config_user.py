from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SimpleConfigUser:
    email: Optional[str] = types.str
    config: dict[str, bool] = types.shape({
        'ios': types.bool.required,
        'android': types.bool.required
    }).required
