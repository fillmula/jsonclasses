from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class OpUser:
    name: str = types.str.required
    owned_teams: list[OpTeam] = types.nonnull.listof('OpTeam')


@jsonclass
class OpTeam:
    name: str = types.str.op(lambda o, t: o == t.owner).required
    owner: OpUser = types.instanceof('OpUser').required
