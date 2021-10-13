from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class CalcUser:
    name: str
    first_name: str = types.str.getter(lambda u: u.name.split(" ")[0])
    last_name: str = types.str.getter(types.this.fval('name').split(' ').at(1))
    base_score: float
    score: float = types.float.getter(types.this.fval('base_score').mul(2)).negative
