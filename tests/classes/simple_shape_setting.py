from __future__ import annotations
from typing import Optional, TypedDict
from jsonclasses import jsonclass, types


class EmailSetting(TypedDict):
    auto_send: bool
    receive_promotion: bool


@jsonclass
class SimpleShapeSetting:
    user: Optional[str]
    email: EmailSetting = types.nonnull.shape({
        'auto_send': bool,
        'receive_promotion': bool
    })
