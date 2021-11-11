from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class SuperOneOf:
    const: list[str] = types.listof(str).default(['abc', 'def', 'ghi']).required
    valconst: str | None = types.str.oneof(['abc', 'def', 'ghi'])
    valcallable: str | None = types.str.oneof(lambda o: o.const)
    valtypes: str | None = types.str.oneof(types.this.fval('const'))
