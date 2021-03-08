from __future__ import annotations
from typing import TypedDict
from jsonclasses import jsonclass, types


class EmailSetting(TypedDict):
    auto_send: bool
    receive_promotion: bool


@jsonclass
class SimpleSetting:
    user: str
    email: EmailSetting = types.shape({
        'auto_send': types.bool.required,
        'receive_promotion': types.bool.required
    })
