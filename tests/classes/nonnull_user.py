from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class NonnullUser:
    name: str = types.str.writenonnull.required
    nickname: str = types.str.writenonnull.default('KuiPêkBvang').required
